# API Endpoints.


import json
import traceback

import arrow
import falcon
import redis
from loguru import logger

from app.modules.database import Database


class Ping(object):
    def __init__(self, redis_connection):
        self._redis = redis_connection

    def on_get(self, req, resp):
        unparsed = self._redis.get("lastUpdatedTimestamp")
        github_page = req.get_param("githubPage")
        if github_page:
            parsed = json.loads(unparsed.decode("utf-8"))
            resp.media = {
                "status": "Online",
                "lastUpdated": arrow.get(parsed["data"]["lastUpdatedISO"]).humanize(),
            }
        else:
            parsed = json.loads(unparsed.decode("utf-8"))
            parsed["status"] = "Online"
            resp.media = parsed


class LatestCases(object):
    def __init__(self, redis_connection, country_lists):
        self._redis = redis_connection
        self._countries = country_lists

    def on_get(self, req, resp):
        if req.get_param("filterByCountry"):
            countrySelected = req.get_param("filterByCountry")
            if self._countries.get(countrySelected):
                resp.body = self._countries.get(countrySelected).decode("utf-8-sig")
            else:
                resp.status = falcon.HTTP_404
                resp.media = {"data": []}
        else:
            resp.body = self._redis.get("latestFigures")


class LatestNumbers(object):
    def __init__(self, redis_connection):
        self._redis = redis_connection

    def on_get(self, req, resp):
        with self._redis.pipeline() as pipe:
            pipe.get("totalConfirmedNumbers")
            pipe.get("totalDeathNumbers")
            pipe.get("totalRecoveredNumbers")
            results = pipe.execute()

        for item in results:
            try:
                check_int = int(item)
            except Exception:
                logger.info("invalid information.")
                totalConfirmedNumbers = None
                totalDeathNumbers = None
                totalRecoveredNumbers = None
                break

            totalConfirmedNumbers = int(results[0])
            totalDeathNumbers = int(results[1])
            totalRecoveredNumbers = int(results[2])

        resp.media = {
            "data": {
                "totalConfirmedNumbers": totalConfirmedNumbers,
                "totalDeathNumbers": totalDeathNumbers,
                "totalRecoveredNumbers": totalRecoveredNumbers,
            }
        }


class LatestConfirmed(object):
    def __init__(self, redis_connection):
        self._redis = redis_connection

    def on_get(self, req, resp):

        try:
            number_count = self._redis.get("totalConfirmedNumbers")
            if isinstance(number_count, bytes):
                number_count = number_count.decode("utf-8")
            resp.media = {"data": {"totalConfirmedNumbers": int(number_count)}}
        except Exception:
            logger.error("Unable to get numbers")
            logger.debug(f"{traceback.format_exc()}")

            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": "Unable to get numbers."}


class LatestDeaths(object):
    def __init__(self, redis_connection):
        self._redis = redis_connection

    def on_get(self, req, resp):
        try:
            number_count = self._redis.get("totalDeathNumbers")
            if isinstance(number_count, bytes):
                number_count = number_count.decode("utf-8")
            resp.media = {"data": {"totalDeathNumbers": int(number_count)}}
        except Exception:
            logger.error("Unable to get numbers")
            logger.debug(f"{traceback.format_exc()}")

            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": "Unable to get numbers."}


class LatestRecovered(object):
    def __init__(self, redis_connection):
        self._redis = redis_connection

    def on_get(self, req, resp):
        try:
            number_count = self._redis.get("totalRecoveredNumbers")
            if isinstance(number_count, bytes):
                number_count = number_count.decode("utf-8")
            resp.media = {"data": {"totalRecoveredNumbers": int(number_count)}}
        except Exception:
            logger.error("Unable to get numbers")
            logger.debug(f"{traceback.format_exc()}")

            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": "Unable to get numbers."}


api = falcon.API()
database = Database()

redis_connection = database._redis
country_redis = database._countryRedis

api.add_route("/status", Ping(redis_connection))
api.add_route("/latest/cases", LatestCases(redis_connection, country_redis))
api.add_route("/latest/numbers", LatestNumbers(redis_connection))
api.add_route("/latest/numbers/confirmed", LatestConfirmed(redis_connection))
api.add_route("/latest/numbers/deaths", LatestDeaths(redis_connection))
api.add_route("/latest/numbers/recovered", LatestRecovered(redis_connection))
