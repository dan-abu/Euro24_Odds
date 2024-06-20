# UEFA EURO 2024 FIXTURE ODDS PIPELINE

## Overview

For context, the code in this repository gathers sports betting data for the
UEFA EURO 2024 Football championship. It gathers this code from the
Odds API sports betting API: https://the-odds-api.com.

I designed it as a self-motivated project in anticipation for a job role
I've applied for. As a result, this is a functioning **PROTOTYPE**.

## Context
This repository contains two scripts.

`odds_sports.py` allows you to see the full list of in-season sports
(i.e. see which sports bookmakers will allow you to place bets on).
The main benefit from this script is that it allows you to see the
sports name Odds API uses for your chosen sport, which you'll need for
the second script.

`odds_fixtures.py` allows you to see the odds different bookmakers are giving
for **ONE** team still in UEFA EURO 2024. The output of this script is a
CSV file per fixture for your chosen team.

Please note that the sport is already hard-coded in the script
as `soccer_uefa_european_championship` and that you'll need to run the script
via the command line. See examples below: one with some values and one with
just placeholders.

See an example command below.
```
python3 ./src/odds_fixtures.py <odds api key> uk h2h France Euro24_Odds/data

python3 ./src/odds_fixtures.py <odds api key> <regions> <markets> <country of interest> <storage dir>
```

## Useful Info

- Install technical dependencies as per the `requirements.txt` file.
- Remember that the names of countries used by the API are all in English. If the country name you choose
still doesn't work, you might need to play around with the GET request to see the full list of countries
still in the tournament.
- You'll need an API key from Odds API to run the script. You can get one **FOR FREE** from their
website. Use the link at the top of this document to find out more.
- If you want to see more of the options for the variable inputs for the GET request, please take a
look at Odds API's website (see link at top of this doc).

## Consideration
As I mentioned, at the start of this doc, this is a prototype and I am still getting familiar with
Odds' API.
From what I understand, it is very likely that odds will fluctuate throughout the day. Keep this in mind
if you use any odds you gather **AND**, if you decide to automate the pipeline and get reegular updates,
then it might be worth adding some sort of partitioning to your storage directory.