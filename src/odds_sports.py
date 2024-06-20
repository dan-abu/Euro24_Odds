import requests
import json
import sys
from datetime import datetime as dt


def getOddsSports(apiKey: str) -> str:
    """Prototype for pulling list of in-season Odds sports"""
    endPoint = f"/v4/sports/?apiKey={apiKey}"
    url = "https://api.the-odds-api.com"
    url = url + endPoint

    try:
        r = requests.get(url)

    except Exception as e:
        print(
            f"Unable to successfully complete Odds API GET in-season sports request.\nError occurred:\n{e}"
        )
        raise e

    else:
        print("Successfully completed Odds API GET odds request.")
        data = r.json()
        data = json.dumps(data, indent=4)

    return data


def stringToFile(filename: str, content: str) -> None:
    """Creates a .txt file from a string"""
    try:
        with open(filename, "w") as f:
            f.write(content)
        print(f"Content successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred:\n{e}")


def createFilename(dataDir: str) -> str:
    """Generates a filename"""
    execTime = dt.now().strftime("%Y-%m-%d_%H%M")
    newFilename = f"{dataDir}/inseason_sports{execTime}.txt"
    return newFilename


if __name__ == "__main__":
    api_key = sys.argv[1]
    storage_dir = sys.argv[2]
    sports = getOddsSports(apiKey=api_key)
    new_filename = createFilename(dataDir=storage_dir)
    stringToFile(filename=new_filename, content=sports)
