__author__ = 'mhillick'
import urllib
import json
from slackclient import SlackClient
import time
import re

day = time.strftime("%Y/%m/%d")

# Riot API Stuff
# Get the Level 30 info
#
def get_level(summoner):
    api_key = "xxxxx"
    base_url = "https://na.api.pvp.net/api/lol/na/v2.2/summoner/by-name/"
    url = base_url + str(summoner) + "?api_key=" + api_key # Creating the final URL to call
    input = urllib.urlopen(url).read()
    info = json.loads(input)
    level = info[summoner]['summonerLevel']
    return level
    
# Setting up the List of Summoners we are looking for
summoners = [ 'SECURITATEM', 'II uspdan II' , 'siosafoo' ] 
summoner_levels = {}
for s in summoners:
    level = get_level(s)
    summoner_levels[s] = level

# Slack Stuff
#
slack_token = "xxxx" # The Slack Bot token for API calls
sc = SlackClient(slack_token) # Create the slack bot instance with the token we created earlier:
def send_message(sc,channel_id,text):
    sc.api_call(
        "chat.postMessage",
        as_user="false",
        text=message,
        channel=channel_id,
        username="Level30Bot",
        icon_emoji=':robot_face:',
    )
    return None

try:
     message = ':boom: \nHey Summoners, here is the Level 30 Progress Report for today!!!\n :boom:'
    send_message(sc,"l30-progress",message)
#     send_message(sc,"ot-mh-testing",message)
except:
        print("Unable to connect to Slack!")

for n,l in summoner_levels.iteritems():
    message = "Summoner", n ,"is at Level", l
    print message
    try:
        send_message(sc,"l30-progress",message)
#        send_message(sc,"ot-mh-testing",message)
    except:
        print("Unable to connect to Slack!")
