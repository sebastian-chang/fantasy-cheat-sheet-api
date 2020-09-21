import pandas as pd
import math
import os
import dj_database_url
import base64
import requests

# from sqlalchemy import create_engine, MetaData, Table, and_
# from sqlalchemy.sql import select

from ..models.qb_stat import QBStat
apikey_token = os.getenv('MSF_API')

# Determine if we are on local or production
# if os.getenv('ENV') == 'development':
#     DB = 'postgresql://localhost:5432/' + os.getenv('DB_NAME_DEV')
# else:
#     DB = 'something else'
# engine = create_engine(DB)


# Gets player information from 3rd party API
def player_info_request(first_name, last_name, pos, team):
    pull_url = f'https://api.mysportsfeeds.com/v2.1/pull/nfl/players.json?player={first_name}-{last_name}&position={pos}&team={team}'

    # Attempt to get player info from My Sports Feed
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

    # Attempts to get player stats from My Sports Feed
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
def clean_player(api_player, user_player):
    # Creates an empty dictionary to store data into
    new_player = {}
    # Takes data from 3rd party data
    new_player['first_name'] = api_player['firstName']
    new_player['last_name'] = api_player['lastName']
    new_player['position'] = api_player['primaryPosition']
    new_player['current_team'] = api_player['currentTeam']['abbreviation']
    new_player['photo_url'] = api_player['officialImageSrc']
    new_player['MSF_PID'] = api_player['id']
    new_player['jersey_number'] = api_player['jerseyNumber']
    new_player['height'] = api_player['height']
    new_player['weight'] = api_player['weight']
    new_player['age'] = api_player['age']
    new_player['dob'] = api_player['birthDate']
    # Adds additional information from our database to obeject
    new_player['id'] = user_player['id']
    new_player['sheet'] = user_player['sheet']
    new_player['owner'] = user_player['owner']

    return new_player


# Calls 3rd party API and formats data for storage in our database
def player_input(user_player):
    # print(
    #     f"We've made it into the api function call with {user_player['first_name']} the {user_player['current_team']}")

    # Make connection to database and check to see if player already exists
    # connection = engine.connect()
    # metadata = MetaData(bind=None)
    # only qb stats working now
    # table = Table('api_qbstat', metadata, autoload=True, autoload_with=engine)

    # Creates a dictionary from the response data of 3rd party API
    api_player = player_info_request(
        user_player['first_name'], user_player['last_name'], user_player['position'], user_player['current_team'])
    # player_info = clean_player(player_info)
    # print(f"this is the player info from the api call {api_player['references']['teamReferences'][0]['city']}")
    # print(f"ength of request is {len(player_info['players'])}")

    # Checks to see if we found the player user was looking for
    if (len(api_player['players']) == 1):
        # Adds additional info not located in player response
        player_info = clean_player(
            api_player['players'][0]['player'], user_player)
        player_info['city_team'] = api_player['references']['teamReferences'][0]['city'] + \
            ' ' + api_player['references']['teamReferences'][0]['name']
        player_info['team_logo'] = api_player['references']['teamReferences'][0]['officialLogoImageSrc']
        # Checks to see if player has stats
        player_stats = list(QBStat.objects.filter(pid=player_info['MSF_PID']))
        # sel = select([table]).where(table.columns.pid == player_info['MSF_PID'])
        # results = connection.execute(sel).fetchall()
        if(len(player_stats) > 0):
            player_info['has_stats'] = True

        # Check to see if player stats are stored in our local database.  If not fetch data to store
        # query = select([table]).where()
        # results = connection.execute(query).fetchall()

        # Return player dictionary to be stored to local database through Django serializer
        return player_info

    # If player isn't located remove or blank out data from 3rd party API
    else:
        user_player['photo_url'] = 'https://www.oseyo.co.uk/wp-content/uploads/2020/05/empty-profile-picture-png-2.png'
        user_player['MSF_PID'] = 0
        user_player['jersey_number'] = 0
        user_player['height'] = ''
        user_player['weight'] = 0
        user_player['age'] = 0
        user_player['dob'] = ''
        user_player['city_team'] = ''
        user_player['team_logo'] = ''
        user_player['has_stats'] = False
        return user_player
