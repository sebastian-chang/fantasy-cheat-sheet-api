import pandas as pd
import math
import os
import base64
import requests

from ..models.qb_stat import QBStat
apikey_token = os.getenv('MSF_API')

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
def player_stats_request(pid, year):
    pull_url = f'https://api.mysportsfeeds.com/v2.1/pull/nfl/{year}-regular/player_gamelogs.json?player={pid}'

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
def clean_stats(data, season, msf_pid):
    # Create a blank array for player season stats
    new_data = []

    # Go through each week of the season player played
    for i in range(len(data)):
        new_dict = {}
        player_team = data[i]['team']['abbreviation']
        new_dict['pid'] = msf_pid
        new_dict['week'] = data[i]['game']['week']
        new_dict['season'] = season

        # Check to see if player was home or away team.  Also set the opponent played
        if(player_team == data[i]['game']['homeTeamAbbreviation']):
            new_dict['homeoraway'] = 'HOME'
            new_dict['opponent'] = data[i]['game']['awayTeamAbbreviation']
        else:
            new_dict['homeoraway'] = 'AWAY'
            new_dict['opponent'] = data[i]['game']['homeTeamAbbreviation']

        # Add passing stats to QB object
        for stat, value in data[i]['stats']['passing'].items():
            # Must use lowercase lettering for django models
            new_dict[stat.lower()] = value

        # Add the week's data into the seasons array
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


# Calls 3rd party API for player info and formats data for storage in our database
def player_input(user_player):
    # Creates a dictionary from the response data of 3rd party API
    api_player = player_info_request(
        user_player['first_name'], user_player['last_name'], user_player['position'], user_player['current_team'])

    # Checks to see if we found the player user was looking for
    if (len(api_player['players']) == 1):
        # Adds additional info not located in player response
        player_info = clean_player(
            api_player['players'][0]['player'], user_player)
        player_info['city_team'] = api_player['references']['teamReferences'][0]['city'] + \
            ' ' + api_player['references']['teamReferences'][0]['name']
        player_info['team_logo'] = api_player['references']['teamReferences'][0]['officialLogoImageSrc']
        # Check to see if player stats are stored in our local database.  If not fetch data to store
        player_stats = list(QBStat.objects.filter(pid=player_info['MSF_PID']))
        if(len(player_stats) > 0):
            player_info['has_stats'] = True
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

# Calls 3rd party API for player stats and formats data for storage in database
def player_stat_input(pid, year):
    player_response = player_stats_request(pid, year)
    player_stats = clean_stats(player_response['gamelogs'], year, pid)
    return(player_stats)
