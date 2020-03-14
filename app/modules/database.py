# All communcation with Redis

import json

import arrow
import redis
from loguru import logger


class Database(object):
    def __init__(self):
        self._redis = redis.Redis(port=4032)
        self._countryRedis = redis.Redis(db=1, port=4032)

    def _updateTotalConfirmed(self, new_data):
        current_numbers = 0

        for item in new_data["data"]:
            if item["Confirmed"] == "":
                continue
            current_numbers += int(item["Confirmed"])

        self._redis.set("totalConfirmedNumbers", current_numbers)

    def _updateTotalDeaths(self, new_data):
        current_numbers = 0

        for item in new_data["data"]:
            if item["Deaths"] == "":
                continue

            current_numbers += int(item["Deaths"])

        self._redis.set("totalDeathNumbers", current_numbers)

    def _updateTotalRecovered(self, new_data):
        current_numbers = 0

        for item in new_data["data"]:
            if item["Recovered"] == "":
                continue

            current_numbers += int(item["Recovered"])

        self._redis.set("totalRecoveredNumbers", current_numbers)

    def _updateEachCountry(self, new_data):
        for item in new_data["data"]:
            if self._countryRedis.get(item["Country/Region"]):
                load_country = json.loads(
                    self._countryRedis.get(item["Country/Region"])
                )
                load_country["data"].append(item)
                self._countryRedis.set(item["Country/Region"], json.dumps(load_country))
            else:
                load_country = {"data": [item]}
                self._countryRedis.set(item["Country/Region"], json.dumps(load_country))

    def update_data(self, new_data_update):
        # Move previous data to historical key.

        current_data = self._redis.get("latestFigures")
        if current_data:
            read_current_data = json.loads(current_data.decode("utf-8"))
            # set historical data.
            if read_current_data["apiInformation"].get("lastUpdated", False) == False:
                logger.error("Invalid data structure present in redis.")
                logger.debug(f"InvalidDataStructure: {read_current_data}")
            else:
                self._redis.rename(
                    "latestFigures", read_current_data["apiInformation"]["lastUpdated"]
                )
                logger.info(
                    f"Moved figures for {read_current_data['apiInformation']['lastUpdated']} to history."
                )

        self._redis.set("latestFigures", json.dumps(new_data_update))
        self._updateTotalConfirmed(new_data_update)
        self._updateTotalDeaths(new_data_update)
        self._updateTotalRecovered(new_data_update)
        self._updateEachCountry(new_data_update)
