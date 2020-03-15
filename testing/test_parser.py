import pytest
from app.modules.parser import Parser


def test_correct_parsing():

    parse_file = Parser("testing/sample.csv", useDatabase=False)
    result = parse_file.parse()

    assert isinstance(result, dict) == True

    for item in result["meta-data"]["countriesInfected"]:
        assert item == "Mainland China"

    for item in result["data"]:
        assert item["Country/Region"] == "Mainland China"

    assert result["data"][0]["Country/Region"] != "Country/Region"

    for item in list(result["data"][0].keys()):
        for letter in item:
            assert letter == "/" or letter.isalpha() == True

