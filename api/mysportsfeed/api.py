import pandas as pd
import math
import os
import base64
import requests

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select

# Determine if we are on local or production
if os.getenv('ENV') == 'development':
    DB = 'postgresql://localhost:5432/' + os.getenv('DB_NAME_DEV')
else:
    DB = 'something else'
apikey_token = os.getenv('MSF_API')

engine = create_engine(DB)

def player_info_request(first_name, last_name):
    pull_url = f'https://api.mysportsfeeds.com/v2.1/pull/nfl/players.json?player={first_name}-{last_name}'

    try:
        response = requests.get(
            url=pull_url,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{apikey_token}:MYSPORTSFEEDS'.encode('utf-8')).decode('ascii')
            }
        )
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed getting player info')

def player_stats_request(first_name, last_name, year):
    pull_url = f'https://api.mysportsfeeds.com/v2.1/pull/nfl/{year}-regular/player_gamelogs.json?player={first_name}-{last_name}'

    try:
        response = requests.get(
            url=pull_url,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{apikey_token}:MYSPORTSFEEDS'.encode('utf-8')).decode('ascii')
            }
        )
        return response.json()
    except requests.exceptions.RequestException:
        print('HTTP Request failed getting player stats')


def clean_data(data, season):
    new_data = []

    # Go through each week of the season player played
    for i in range(len(data)):
        new_dict = {}
        player_team = data[i]['team']['abbreviation']
        new_dict['week'] = data[i]['game']['week']
        new_dict['season'] = season

        # Check to see if player was home or away team.  Also set the opponent played
        if(player_team == data[i]['game']['homeTeamAbbreviation']):
            new_dict['HomeOrAway'] = 'HOME'
            new_dict['Opponent'] = data[i]['game']['awayTeamAbbreviation']
        else:
            new_dict['HomeOrAway'] = 'AWAY'
            new_dict['Opponent'] = data[i]['game']['homeTeamAbbreviation']

        # Add passing stats to QB object
        for stat, value in data[i]['stats']['passing'].items():
            new_dict[stat] = value

        new_data.append(new_dict)

    return new_data

def player_input(first_name, last_name):