"""Gives odds for your favourite country's remaining games in Euro 2024"""
import requests
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime as dt


def commaConcatList(itemList) -> str:
    """Concatenates string into a list with items separated by commas"""
    itemList = ",".join(itemList)
    return itemList


def getEuroOdds(sport: str, apiKey: str, **kwargs) -> list:
    """Prototype for pulling odds from odds api"""
    regions = kwargs["regions"]
    if isinstance(regions, list):
        regions = commaConcatList(regions)
    else:
        pass

    markets = kwargs["markets"]
    if isinstance(markets, list):
        markets = commaConcatList(markets)
    else:
        pass

    endPoint = (
        f"/v4/sports/{sport}/odds/?apiKey={apiKey}&regions={regions}&markets={markets}"
    )
    url = "https://api.the-odds-api.com"
    url = url + endPoint

    try:
        r = requests.get(url)

    except Exception as e:
        print(
            f"Unable to successfully complete Odds API GET odds request.\nError occurred:\n{e}"
        )
        raise e

    else:
        print("Successfully completed Odds API GET odds request.")
        data = r.json()

    return data


def getSimplifiedFixtures(fixturesList: list) -> list:
    """Get shorter and more readable version of fixture list from payload"""
    fixture_list = []

    for fixture in fixturesList:
        match = []
        match.append(fixture["id"])
        match.append(fixture["home_team"])
        match.append(fixture["away_team"])
        fixture_list.append(match)

    return fixture_list


def getSimplifiedCountryFixtures(simplifiedFixtureList: list, country: str) -> list:
    """Get fixtures for a specific country"""
    country_fixture_list = []
    for fixture in simplifiedFixtureList:
        if country in fixture:
            country_fixture_list.append(fixture)

    return country_fixture_list


def getCountryFixtureIDs(simplifiedCountryFixtures: list) -> list:
    """Gets list of fixture IDs for your preferred country"""
    country_fixture_list_ids = []
    for fixture in simplifiedCountryFixtures:
        country_fixture_list_ids.append(fixture[0])

    return country_fixture_list_ids


def getCountryFixtureOdds(countryFixtureIDs: list, fixturesList: list) -> list:
    """Get odss from different bookmakers for preferred country's fixtures"""
    country_fixture_odds = []
    for fixture in fixturesList:
        if fixture["id"] in countryFixtureIDs:
            country_fixture_odds.append(fixture)

    return country_fixture_odds


def cleanBookmakerDict(bookmaker: dict, prefCountry: str) -> dict:
    """Cleans dictionary as per requirements for this script"""
    del bookmaker["key"]
    bookmaker["Bookmaker"] = bookmaker["title"]
    del bookmaker["title"]
    bookmaker["last_update"] = bookmaker["markets"][0]["last_update"]
    bookmaker["market"] = bookmaker["markets"][0]["key"]

    some_outcomes = [prefCountry, "Draw"]
    for outcome in bookmaker["markets"][0]["outcomes"]:
        if prefCountry in outcome.values():
            indexVal = bookmaker["markets"][0]["outcomes"].index(outcome)
            prefCountry = bookmaker["markets"][0]["outcomes"][indexVal]["name"]
            prefCountryPrice = bookmaker["markets"][0]["outcomes"][indexVal]["price"]
    for outcome in bookmaker["markets"][0]["outcomes"]:
        if "Draw" in outcome.values():
            indexVal = bookmaker["markets"][0]["outcomes"].index(outcome)
            draw = bookmaker["markets"][0]["outcomes"][indexVal]["name"]
            drawPrice = bookmaker["markets"][0]["outcomes"][indexVal]["price"]
    for outcome in bookmaker["markets"][0]["outcomes"]:
        if outcome["name"] not in some_outcomes:
            indexVal = bookmaker["markets"][0]["outcomes"].index(outcome)
            otherCountry = bookmaker["markets"][0]["outcomes"][indexVal]["name"]
            otherCountryPrice = bookmaker["markets"][0]["outcomes"][indexVal]["price"]

    bookmaker[prefCountry] = prefCountryPrice
    bookmaker[otherCountry] = otherCountryPrice
    bookmaker[draw] = drawPrice
    del bookmaker["markets"]

    return bookmaker


def getSimplifiedFixtureOdds(countryFixtureOdds: list, prefCountry: str) -> list:
    """Get a dataframe per fixture where each dataframe contains the h2h odds
    for your preferred country from several bookmakers"""
    simplifiedFixtureOdds = []
    for fixture in countryFixtureOdds:
        fixtureData = []
        for bookie in fixture["bookmakers"]:  # list of bookmakers' odds for one fixture
            bookie = cleanBookmakerDict(bookie, prefCountry=prefCountry)
            fixtureData.append(bookie)
        fixtureData = pd.DataFrame(fixtureData)
        simplifiedFixtureOdds.append(fixtureData)

    return simplifiedFixtureOdds


def createMultiCSVs(
    tableList: list, storageDir: str, execTime: str, prefCountry: str
) -> None:
    """Creates CSVs from list of dataframes"""
    counter = 0
    for table in tableList:
        counter += 1
        baseTableName = f"{prefCountry}_fixture{counter}_odds{exec_time}"
        suffix = ".csv"
        filepath = Path(storageDir, baseTableName).with_suffix(suffix)
        table.to_csv(filepath, index=False)
        print(f"Successfully wrote file to {filepath}")


if __name__ == "__main__":
    api_key = sys.argv[1]
    Regions = sys.argv[2]
    Markets = sys.argv[3]
    pref_country = sys.argv[4]
    storage_dir = sys.argv[5]
    exec_time = dt.now().strftime("%Y-%m-%d_%H%M")
    fixture_list = getEuroOdds(
        sport="soccer_uefa_european_championship",
        apiKey=api_key,
        regions=Regions,
        markets=Markets,
    )
    simplified_fixtures = getSimplifiedFixtures(fixture_list)
    country_fixtures = getSimplifiedCountryFixtures(simplified_fixtures, pref_country)
    country_fixture_ids = getCountryFixtureIDs(country_fixtures)
    country_fixture_odds = getCountryFixtureOdds(country_fixture_ids, fixture_list)
    simplified_fixture_odds = getSimplifiedFixtureOdds(
        country_fixture_odds, pref_country
    )
    createMultiCSVs(simplified_fixture_odds, storage_dir, exec_time, pref_country)
