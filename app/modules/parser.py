# Main Parser.

import traceback
import arrow


import pathlib
import csv
import json

from loguru import logger

from app.modules.database import Database


class Parser(object):
    def __init__(self, saved_file_name):
        if pathlib.Path(saved_file_name).exists() == True:
            self._name = saved_file_name
        else:
            logger.error(f"File provided {saved_file_name} does not exist.")
            raise Exception("File does not exist.")

        self._db = Database()

    def _get_key(self):
        try:
            current_csv = open(self._name, "r")
            read_csv = csv.reader(current_csv)

            field_headers = []

            for x in read_csv:
                field_headers.append(x)
                break

            return tuple(field_headers[0])
        except Exception:
            logger.error("Unable to get headers for file.")
            logger.debug(f"HeaderFail: {traceback.format_exc()}")
            raise

    def parse(self):
        # Open the file
        try:
            current_headers = self._get_key()
        except Exception:
            raise

        current_file = open(self._name, "r", encoding="utf-8-sig")
        csv_reader = csv.DictReader(current_file, current_headers)

        current_info = {
            "data": [],
            "meta-data": {"countriesInfected": []},
            "apiInformation": {"lastUpdated": arrow.now().format("MM-DD-YYYY")},
        }

        for row in csv_reader:
            if row["Country/Region"] == "Country/Region":
                continue

            if (
                row["Country/Region"]
                not in current_info["meta-data"]["countriesInfected"]
            ):
                current_info["meta-data"]["countriesInfected"].append(
                    row["Country/Region"]
                )

            current_info["data"].append(row)

        self._db.update_data(current_info)
        return True
