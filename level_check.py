#!/usr/bin/env python

"""level_check

Usage:
    level_check.py

    level_check.py is a small bit of python code intended for fun to retrieve some information relating to LoL performance for friends :)
    Options:
      -h --help                   Show this screen
      -v --version                Show the version\n\n
"""

__author__ = 'mhillick'

#TODO :: Like shitloads tbh

import urllib
import json
from slackclient import SlackClient
import datetime

#day = datetime.date.today.strftime("%Y-%m-%d")
# Riot API Stuff
api_key = "xxxx"
# Slack Stuff
slack_token = "xxxx" # The Slack Bot token for API calls
sc = SlackClient(slack_token) # Create the slack bot instance with the token we created earlier:


def get_level(summoner):
    """Gets the level of a given summoner"""
    #base_url = "https://", region, ".api.pvp.net/api/lol/", region, "/v2.2/summoner/by-name/"
    base_url = "https://na.api.pvp.net/api/lol/na/v2.2/summoner/by-name/"
    url = base_url + str(summoner) + "?api_key=" + api_key # Creating the final URL to call
    input = urllib.urlopen(url).read()
    info = json.loads(input)
    level = info[summoner]['summonerLevel']
    return level

def get_game(summoner_id):
    """Gets the stats on recent games of a given summoner"""
    #base_url = "https://", region, ".api.pvp.net/api/lol/", region, "/v2.2/game/by-summoner/"
    base_url = "https://na.api.pvp.net/api/lol/na/v2.2/game/by-summoner/"
    url = base_url + str(summoner_id) + "/recent?api_key=" + api_key # Creating the final URL to call
    input = urllib.urlopen(url).read()
    info = json.loads(input)
    timestamp = info[0]["gameInfo"]["gameStartTimestamp"]
    game_mode = info[0]["gameInfo"]["gameMode"]
    champ_id = info[0]["participants"][0]["championId"]
    winner = info[0]["participants"][0]["stats"]["winner"]
    kills = info[0]["participants"][0]["stats"]["kills"]
    deaths = info[0]["participants"][0]["stats"]["deaths"]
    assists = info[0]["participants"][0]["stats"]["assists"]
    damage_dealt = info[0]["participants"][0]["stats"]["totalDamageDealt"]
    damage_taken = info[0]["participants"][0]["stats"]["totalDamageTaken"]
    pentakills = info[0]["participants"][0]["stats"]["pentaKills"]
    return champ_id, timestamp, game_mode, winner, kills, deaths, assists, damage_dealt, damage_taken, pentakills

def get_champ_name(champ_id):
    """Gets the Champion Name from the Champion ID"""
    base_url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"
    url = base_url + str(champ_id) + "?api_key=" + api_key # Creating the final URL to call
    input = urllib.urlopen(url).read()
    info = json.loads(input)
    champ_name = info["name"]
    return champ_name

def send_message(sc,channel_id,text):
    """Sends a message to Slack"""
    sc.api_call(
        "chat.postMessage",
        as_user="false",
        text=message,
        channel=channel_id,
        username="Level30Bot",
        icon_emoji=':robot_face:',
    )
    return None

def update_l30(message):
    """Updates the Level 30 Channel with messages"""
    try:
        #send_message(sc,"l30-progress",message)
        send_message(sc,"ot-mh-testing",message)
    except:
        print("Unable to connect to Slack!")
    return None

if __name__ == '__main__':
    from docopt import docopt

    arguments = docopt(__doc__, version='level_check 0.2')

    # Setting up the list of tuple of summoners and summoner ids
    summoners = [('SECURITATEM', '68520962'), ('II uspdan II', '77402230') , ('siosafoo', '64399216') , ('Stelks', '79761554')]
    summoner_data = []

    message = ':boom: Hey Summoners, here is the *Level 30* :newspaper: for this morning!!! :boom:'
    update_l30(message)

    for (summoner, summoner_id) in summoners:
        try:
            level = get_level(summoner)
            message = "Yo *{}*, you are at level {}".format(summoner,level)
            if level == 30:
                message += "Jeez, this is fucking incredible, :ggez: {}, you have won the :summonerscup:. Onwards and upwards to the toxic world of Ranked for you :thumbsup:".format(summoner)
            update_l30(message)
            try:
                (champ_id, timestamp, game_mode, winner, kills, deaths, assists, damage_dealt, damage_taken, pentakills) = get_game(summoner_id)
                lastplay_date = datetime.datetime.fromtimestamp(timestamp/1000)
                lastplay_day = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')
                champ_name = get_champ_name(champ_id)
                if game_mode == "CLASSIC":
                    game_mode = "SUMMONER'S RIFT"
                if winner == True:
                    winner = 'winner'
                else:
                    winner = 'big f**king loser'
                message = "```In your last game with {}, on {}, you played {} and were a {}. You had {} kills, {} deaths and {} assists! You dealt {} total damage and took {} total damage.```".format(champ_name, lastplay_day, game_mode, winner, kills, deaths, assists, damage_dealt, damage_taken)
                if game_mode == "ARAM":
                    message += "\n\n> WTF, srsly dude, ARAM??? You filthy casual :shit:"
                if damage_dealt < damage_taken:
                    message += "\n\n> Jesus dude, you got creamed :rekt: :lololol"
                if damage_dealt > (1.5 * damage_taken):
                    message += "\n\n> *ggwp* dude, you :rekt: :ggez:"
                if pentakills > 0:
                    message += "\n\nHOLY SHIT, you got a `pentakill` :fistbump:"
                if lastplay_date < datetime.datetime.now()-datetime.timedelta(days=4):
                    message += "\n\n*Sadness *{}*, you haven't played in ages! Come on, get back on the Rift!!! :sadbrewer:".format(summoner)
                update_l30(message)
            except Exception as e:
                print "Unknown Game Status"
        except Exception as e:
            print e
            raise e
    
