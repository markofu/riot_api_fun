#!/usr/bin/env python

"""level_check

Usage:
    level_check.py [-hv] --apikey=api_key --stoken=slack_token
    level_check.py [-hv] --apikey=GAPI-2332232-xxx-xxx-xxx --stoken=xoxp-323232-3232-322334-xxxxxxxxx
    level_check.py --version

    level_check.py is a small bit of python code intended for fun to retrieve some information relating to LoL performance for friends :)


    Arguments:
      --apikey=api_key            Riot API Key [Required Argument]
      --stoken=slack_token        Slack Token [Required Argument]
    
    
    Options:
      -h --help                   Show this screen and exit
      -v --version                Show the version and exit
"""

__author__ = 'mhillick'

#TODO :: Like shitloads tbh

import urllib
import json
from slackclient import SlackClient
import datetime

today = datetime.datetime.now().strftime('%Y-%m-%d')


def get_time(timestamp):
    """Converts the timestamp returned from the api into human readable format from epoch"""
    lastplay_date = datetime.datetime.fromtimestamp(timestamp/1000)
    lastplay_day = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')
    return lastplay_date, lastplay_day

def get_current_hour():
    """Gets the current hour and calculates if morning, afternoon or evening"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        period = "morning"
    elif hour < 17:
        period = "afternoon"
    else:
        period = "evening"
    return period

def send_message(sc,channel_id,text):
    """Sends a message to Slack"""
    sc.api_call(
        "chat.postMessage",
        as_user="false",
        text=message,
        channel=channel_id,
        username="TheGrumpyLoLBot",
        icon_emoji=':robot_face:',
    )
    return None

def update_l30(message):
    """Updates the Level 30 Channel with messages"""
    try:
        send_message(sc,"l30-progress",message)
        #send_message(sc,"ot-mh-testing",message)
    except Exception as e:
        print message
        print e
        print("What's going on, I am unable to connect to Slack! IRC anyone???")
    return None

def greeting():
    """Greeting for the summoners!"""
    global message
    period = get_current_hour()
    message = ":boom: Hey Summoners, here is the *Level 30* :newspaper: for the {} of *{}*!!! :boom:".format(period,today)
    update_l30(message)
    return None

def send_level(summoner_id, level):
    """Sending a level update Slack message for each friend :)"""
    global message
    if summoner_id == "68520962":
        real_name = "Dhalsim"
    elif summoner_id == "77402230":
        real_name = "Paul Hogan"
    elif summoner_id == "64399216":
        real_name = "Gordie Howe"
    elif summoner_id == "79761554":
        real_name = "Barbarossa"
    elif summoner_id == "78639170":
        real_name = "Grumpy Irishman"
    elif summoner_id == "56779115":
        real_name = "Diamond Dallas Page"
    elif summoner_id == "27721089":
        real_name = "Kim Jong's Nephew"
    message = "Yo *{}*, you are at level *{}*!!!".format(real_name, level)
    update_l30(message)
    return real_name

def get_game(summoner_id):
    """Gets the stats on recent games of a given summoner"""
    base_url = "https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"
    url = base_url + str(summoner_id) + "/recent?api_key=" + api_key # Creating the final URL to call
    input = urllib.urlopen(url).read()
    info = json.loads(input)
    timestamp = info["games"][0]["createDate"]
    game_mode = info["games"][0]["gameMode"]
    game_subType = info["games"][0]["subType"]
    if game_mode == "CLASSIC" or "ARAM":
        level = info["games"][0]["level"]
        champ_id = info["games"][0]["championId"]
        winner = info["games"][0]["stats"]["win"]
        try:
            kills = info["games"][0]["stats"]["championsKilled"]
        except:
            kills = 0
        try:
            deaths = info["games"][0]["stats"]["numDeaths"]
        except:
            deaths = 0
        try:
            assists = info["games"][0]["stats"]["assists"]
        except:
            assists = 0
        try:
            kda = float( (kills + assists) / deaths )
        except ZeroDivisionError:
            kda = float('infinity')
        damage_dealt = info["games"][0]["stats"]["totalDamageDealt"]
        damage_taken = info["games"][0]["stats"]["totalDamageTaken"]
    return timestamp, game_mode, game_subType, level, champ_id, winner, kda, damage_dealt, damage_taken

def get_champ_name(champ_id):
    """Gets the Champion Name from the Champion ID"""
    base_url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"
    url = base_url + str(champ_id) + "?api_key=" + api_key # Creating the final URL to call
    input = urllib.urlopen(url).read()
    info = json.loads(input)
    champ_name = info["name"]
    if champ_name == "Garen":
        champ_name = "Garen, the biggest spinner and most boring champion in the game"
    elif champ_name == "Tahm Kench":
        champ_name = "feelsbad_tahmkench" # bizarrely the Tahm emoji ain't the standard
    elif champ_name == "Teemo":
        champ_name = "devil_teemo3" # bizarrely the Tahm emoji ain't the standard
    return champ_name

def send_winner(game_mode, winner,kda, damage_dealt,damage_taken):
    global message
    if winner == True:
        winner = "winner"
    else:
        winner = "big f**king loser"
    if game_mode == "CLASSIC":
        game_mode = "SUMMONER'S RIFT"
        message = "```You played {} and were a {} with a kda of {}. You dealt {} total damage and took {} total damage.```".format(game_mode, winner, kda, damage_dealt, damage_taken)
    elif game_mode == "ARAM":
        message = "```WTF, srsly dude, ARAM??? That's shit, just shit! Filthy Casual!!! Anyway, you played {} and were a {} with a kda of {}. You dealt {} total damage and took {} total damage.```".format(game_mode, winner, kda, damage_dealt, damage_taken)
    update_l30(message)
    return None

def send_last_played_test(timestamp):
    global message
    (lastplay_date) = get_time(timestamp)[0]
    if lastplay_date < datetime.datetime.now()-datetime.timedelta(days=7):
        message = "\n> WTF, have you been on the :beach_with_umbrella: or summat?"
    elif lastplay_date < datetime.datetime.now()-datetime.timedelta(days=4):
        message = "\n> Yo, you haven't played in ages! Come on, get back on the Rift!!! :sadbrewer:"
    else:
        message = "\n> Good work, you are playing lots of LoL, keep it up :thumbsup:"
    update_l30(message)
    return None

def send_played_well(kda):
    """We work out whether or not the summoner has actually played well or not, most likely not"""
    global message
    if kda < 1:
        message = "`BTW, dude, you got creamed, you were` :rekt:"
    elif kda < 2:
        message = "`BTW` :suckit_trebek:"
    elif kda < 4:
        message = "`I suppose you kinda played ok` :medal:"
    else:
        message = "`In that last game dude...` :ggez:"
    update_l30(message)
    return None

def send_last_game(champ_id, timestamp):
    global message
    champ_name = get_champ_name(champ_id)
    (lastplay_day) = get_time(timestamp)[1]
    message = ">>> In your last game with :{}:, on {}.....".format(champ_name, lastplay_day)
    update_l30(message)
    return None

def send_abuse(summoner_id, champ_id):
    global message
    champ_name = get_champ_name(champ_id)
    if summoner_id == "79761554":
        if champ_name in ("Soraka", "Sona"):
            message = "\n > Holy Shit, there's a surprise you played {}, so boring :)".format(champ_name)
        else:
            message = "\n > Holy Shit, you played something other than Soraka or Sona, you played {}, that is :surprisinglylovely:".format(champ_name)
        update_l30(message)
    elif summoner_id == "68520962":
        if champ_name in ("Caitlyn"):
            message = "\n > Holy Shit, there's a surprise you played {}, yeah :caitlyn_sticker: ".format(champ_name)
            update_l30(message)
    elif summoner_id == "77402230":
        if champ_name in ("Veigar"):
            message = "\n > Holy Shit, there's a surprise you played {}. You think you're special with your Event Horizon bullshit, eh :)".format(champ_name)
            update_l30(message)
    return None

def send_messages(summoner_id):
    """Works out a bunch of things based on the summoner id for their last game"""
    try:
        global message
        (timestamp, game_mode, game_subType, level, champ_id, winner, kda, damage_dealt, damage_taken) = get_game(summoner_id)
        send_level(summoner_id, level)
        send_last_game(champ_id, timestamp)
        send_winner(game_mode, winner,kda, damage_dealt,damage_taken)
        send_last_played_test(timestamp)
        send_played_well(kda)
        send_abuse(summoner_id, champ_id)
    except Exception as e:
        print "Unknown Game Status, something failed with the Summoner ID API call, for ID {}!".format(summoner_id)
        print e
    return None

if __name__ == '__main__':
    from docopt import docopt

    try:
    # Parse arguments (from the cli), using file docstring as a parameter definition
        arguments = docopt(__doc__, version='level_check 0.3')
        api_key = str(arguments['--apikey'])
        slack_token = str(arguments['--stoken'])
        sc = SlackClient(slack_token) # Create the slack bot instance with the token we created earlier:
    # Handle invalid options with an exception
    except Exception as e:
        print e

    # Setting up the list of summoner ids
    summoner_ids = ['68520962', '77402230', '64399216', '79761554', '78639170', '56779115', '27721089']
    greeting()
    for id in summoner_ids:
        try:
            send_messages(id)
        except Exception as e:
            print e
