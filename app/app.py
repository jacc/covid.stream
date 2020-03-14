# API Endpoints.


import falcon
import json
import redis
from app.modules.database import Database

from loguru import logger


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


api = falcon.API()
database = Database()

redis_connection = database._redis
country_redis = database._countryRedis


api.add_route("/latest/cases", LatestCases(redis_connection, country_redis))
api.add_route("/latest/numbers", LatestNumbers(redis_connection))

