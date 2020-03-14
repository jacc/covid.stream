import csv
import json
import traceback
import uuid
import os

import arrow
import requests
from github import Github
from loguru import logger
from redis import Redis

from app.authorization import AppAuth
from app.modules.parser import Parser

# Celery worker for updating stats + pulling info.

from celery import Celery

application = Celery("worker", broker="redis://localhost:4032/5",)


@application.on_after_configure.connect
def setup_update_caches(sender, **kwargs):
    sender.add_periodic_task(10800, update_cases.s(), name="update Covid19 Cases")


@application.task
def update_cases():
    logger.remove()
    logger.add("logs.log")

    # Grab the latest infomration from the github repo and update the numbers in redis.

    current_time = arrow.get()
    auth_keys = AppAuth()

    logger.info(
        f"Updating Coronavirus Numbers for {current_time.format('MM-DD-YYYY')}."
    )

    # Connect to Github
    try:
        github = Github(auth_keys.GITHUB_KEY)
        logger.info("Connected to github successfully.")
    except Exception:
        logger.error("Unable to connect to github.")
        logger.debug(f"GithubFailure: {traceback.format_exc()}")
        raise

    # Get Hopkins Repo

    try:
        repo = github.get_repo("CSSEGISandData/COVID-19")
        daily_reports = repo.get_contents(
            "csse_covid_19_data/csse_covid_19_daily_reports"
        )
    except Exception:
        logger.info("Unable to get repo, or repo layout changed.")
        logger.debug(f"RepoFailure: {traceback.format_exc()}")
        raise

    # We're looking for today's date.
    # If today's date isn't there -> Grab yesterday
    # if we have yesterday, we just end it.

    try:
        current_time_formatted = current_time.format("MM-DD-YYYY")
        current_time_string = current_time_formatted + ".csv"
        found_file = False
    except Exception:
        logger.error("Unable to format current time.")
        logger.debug(f"TimeFormat: {traceback.format_exc()}")
        raise

    for item in daily_reports:
        item_id = str(uuid.uuid4())
        if item.name == current_time_string:
            logger.info("Found today's date.")
            # Great, today exists. -> download to file and parse it
            file_request = requests.get(item.download_url)
            with open(f"{item_id}.csv", "wb") as f:
                f.write(file_request.content)
            Parser(f"{item_id}.csv").parse()
            found_file = True

    while found_file == False:
        current_int = -48
        logger.info(f"Current Time Int: {current_int}")
        for item in daily_reports:
            item_id = str(uuid.uuid4())
            if (
                item.name
                == arrow.now().shift(hours=current_int).format("MM-DD-YYYY") + ".csv"
            ):
                file_request = requests.get(item.download_url)
                with open(f"{item_id}.csv", "wb") as f:
                    f.write(file_request.content)

                Parser(f"{item_id}.csv").parse()
                found_file = True
                break
        current_int -= 24

    os.system(f"rm {item_id}.csv")
    return True
