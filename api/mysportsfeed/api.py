import pandas as pd
import math
import os
import base64
import requests

from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import select

# Determine if we are on local or production
if os.getenv('ENV') == 'development':
    DB = 'postgresql://localhost:5432/' + os.getenv('DB_NAME_DEV')
else:
    DB = 'something else'
apikey_token = os.getenv('MSF_API')

engine = create_engine(DB)

# Gets player information from 3rd party API
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

# Gets player game stats from 3rd party API
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

# Cleans up response data from 3rd party API to fit database tables with stats needed for given player
def clean_stats(data, season):
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

# Cleans up response data from 3rd party API to fit database tables
def clean_player(player):
    new_player = {}
    new_player['first_name'] = player['firstName']
    new_player['last_name'] = player['lastName']
    new_player['position'] = player['primaryPosition']
    new_player['current_team'] = player['currentTeam']['abbreviation']
    new_player['photo_url'] = player['officialImageSrc']
    new_player['MSF_PID'] = player['id']

    return new_player


def player_input(first_name, last_name, pos, team):
    # Make connection to database and check to see if player already exists
    connection = engine.connect()
    metadata = MetaData(bind=None)
    table = ('api_player', metadata, autoload=True, autoload_with=engine)
    query = select([table]).where(and_(
        table.columns.first_name == first_name,
        table.columns.last_name == last_name,
        table.columns.position == pos,
        table.columns.current_team == team))
    results = connection.execute(query).fetchall()

    if len(results) > 0:
        # Player exists already add just add to user's sheet
        return
    else:
        # Player doesn't exist in our local database
        # Search for player in 3rd party API
        new_player_info = player_info_request(first_name, last_name)
        if len(new_player_info['players'] > 0):
            # Make sure its the correct player were looking for
        else:
            # Player isn't found on 3rd party API save user input
        return