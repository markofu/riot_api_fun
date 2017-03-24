#!/usr/bin/env python

'''level_check

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
'''

__author__ = 'mhillick'

#TODO :: Like shitloads tbh

from datetime import datetime

import requests
from docopt import docopt
from slackclient import SlackClient

class Champions(object):
    _instance = None
    class __Wrapped(object):
        def __init__(self, api_key):
            self.champions = {}
            url = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key={api_key}'.format(
                api_key=api_key
            )
            data = requests.get(url).json()['data']
            for name, info in list(data.items()):
                self.champions[name.lower()] = info

        def get_by_name(self, name):
            if name.lower() in self.champions:
                return self.champions[name.lower()]

        def get_name_by_id(self, champId):
            for champName, info in list(self.champions.items()):
                if info['id'] == champId:
                    return info['name']

    def __init__(self, api_key):
        if not Champions._instance:
            Champions._instance = Champions.__Wrapped(api_key)

    def __getattr__(self, name):
        return getattr(self._instance, name)

class SlackBot(object):
    def __init__(self, slack_token):
        self.token = slack_token
        self.slack = SlackClient(slack_token)

    def send_message(self, channel, message):
        self.slack.api_call(
            'chat.postMessage',
            as_user='false',
            text=message,
            channel=channel,
            username='Level30Bot',
            icon_emoji=':robot_face:',
        )
        

class Summoner(object):
    __SUMMONER_URL = 'https://{region}.api.pvp.net/api/lol/' \
                     '{region}/v2.2/summoner/by-name/{summoner}?api_key={api_key}'
    __GAME_URL = 'https://{region}.api.pvp.net/api/lol/' \
                 '{region}/v2.2/game/by-summoner/{summonerId}/recent?api_key={api_key}'
    
    def __init__(self, api_key, summoner_name, region='na'):
        self.api_key = api_key
        self.region = region
        self.name = summoner_name
        self.info = None

        self.get_info()

    def get_info(self):
        url = self.__SUMMONER_URL.format(region=self.region, summoner=self.name, api_key=self.api_key)
        info = requests.get(url).json()
        if self.name in info:
            self.info = info[self.name]
        else:
            raise Exception('Summoner {} not found on {}'.format(self.name, self.region))
        
    def get_level(self):
        """
        Gets the current level of the summoner
        :return: Integer level of the summoner
        """
        if not self.info:
            self.get_info()

        return self.info['summonerLevel']

    def get_game(self):
        """
        Gets the stats on recent games of a given summoner
        :return:
        """
        if not self.info:
            self.get_info()

        url = self.__GAME_URL.format(region=self.region, summonerId=self.info['summonerId'], api_key=self.api_key)
        __info = requests.get(url).json()
        __game = __info[0]

        timestamp = __game['gameInfo']['gameStartTimestamp']
        game_mode = __game['gameInfo']['gameMode']
        if game_mode == 'CLASSIC' or 'ARAM':
            for data in __game['participants']:
                s = data['summonerId']
                if s == self.info['summonerId']:
                    # Ensuring summoner ids are equal as people often play in the same game
                    output = {
                        'timestamp': timestamp,
                        'gameMode': game_mode,
                        'champId': data['championId'],
                        'highestRank': data['highestAchievedSeasonTier']
                    }

                    fields = (
                        'winner', 'kills', 'deaths', 'assists',
                        'totalDamageDealt', 'totalDamageTaken', 'pentaKills'
                    )
                    output.update({x: data['stats'][x] for x in data['stats'] if x in fields})
                    return output

        return None

    def get_champ_name(self, champ_id):
        """
        Gets the Champion Name from the Champion ID
        """
        __champions = Champions(self.api_key)
        champ_name = __champions.get_champ_by_id(champ_id)
        if champ_name == 'Garen':
            champ_name = 'Garen, the biggest spinner and most boring champion in the game'
        elif champ_name == 'Tahm Kench':
            champ_name = 'feelsbad_tahmkench'
        return champ_name


class Game(object):
    def __init__(self, api_key, summonerId):
        url = self.__GAME_URL.format(region=self.region, summonerId=summonerId, api_key=api_key)
        info = requests.get(url).json()
        self.game = info[0]
        self.player = None

        if game['gameInfo']['gameMode'] == 'CLASSIC' or 'ARAM':
            for data in self.game['participants']:
                s = data['summonerId']
                if s == self.info['summonerId']:
                    self.player = data

        if not self.player:
            raise Exception('Player not found in game: {}'.format(summonerId))

    @property
    def game_start_timestamp(self):
        return self.info['gameInfo']['gamestartTimestamp']

    @property
    def game_mode(self):
        return self.info['gameInfo']['gameMode']

    @property
    def champion_id(self):
        return self.player['championId']


class Utils(object):
    @staticmethod
    def get_time(timestamp):
        """
        Converts the timestamp returned from the api into human readable format from epoch
        """
        lastplay_date = datetime.fromtimestamp(timestamp / 1000)
        lastplay_day = lastplay_date.strftime('%Y-%m-%d')
        return lastplay_date, lastplay_day

    @staticmethod
    def get_current_hour():
        """
        Gets the current hour and calculates if morning, afternoon or evening
        """
        hour = datetime.datetime.now().hour
        if hour < 12:
            return 'morning'
        elif hour < 17:
            return 'afternoon'
        else:
            return 'evening'

'''
def update_l30(message):
    """Updates the Level 30 Channel with messages"""
    try:
        #send_message(sc,'l30-progress',message)
        print message
        send_message(sc,'ot-mh-testing',message)
    except Exception as e:
        print e
        print('What's going on, I am unable to connect to Slack! IRC anyone???')
    return None

def last_played_test(lastplay_date):
    if lastplay_date < datetime.datetime.now()-datetime.timedelta(days=7):
        message = '\n> WTF *{}*, you been on the :beach_with_umbrella: or summat?'.format(summoner)
    elif lastplay_date < datetime.datetime.now()-datetime.timedelta(days=4):
        message = '\n> Yo *{}*, you haven't played in ages! Come on, get back on the Rift!!! :sadbrewer:'.format(summoner)
    else:
        message = '\n> Good work *{}*, you are playing lots of LoL, keep it up :thumbsup:'.format(summoner)
    update_l30(message)
    return None

def game_mode_test(game_mode):
    if game_mode == 'CLASSIC':
        game_mode = 'SUMMONER'S RIFT'
    elif game_mode == 'ARAM':
        message = '\n\n> WTF, srsly dude, ARAM??? That's just :shit:, plainly :shit:!'
        update_l30(message)
    return game_mode

def winner_test():
    if winner == True:
        winner = 'winner'
    else:
        winner = 'big f**king loser'
    return None

def abuse_test(summoner_id, champ_name):
    if summoner_id == '79761554':
        if champ_name in ('Soraka', 'Sona'):
            message = '\n > Holy Shit *{}*, there's a surprise you played {}, so boring :)'.format(summoner, champ_name)
        else:
            message = '\n > Holy Shit *{}*, you played something other than Soraka or Sona, you played {}, that is :surprisinglylovely:'.format(summoner, champ_name)
        update_l30(message)
    elif summoner_id == '68520962':
        if champ_name in ('Caitlyn'):
            message = '\n > Holy Shit *{}*, there's a surprise you played {}, so you're the Sheriff, big bloody deal :)'.format(summoner, champ_name)
            update_l30(message)
    elif summoner_id == '77402230':
        if champ_name in ('Veigar'):
            message = '\n > Holy Shit *{}*, there's a surprise you played {}. You think you're special with your Event Horizon bullshit, eh :)'.format(summoner, champ_name)
            update_l30(message)
    return None

def has_penta(pentakills):
    if pentakills > 0:
        message = '\n> HOLY SHIT, you got a `pentakill` :fistbump:'
        update_l30(message)
    return None

def played_well_test(summoner_id, damage_dealt, damage_taken):
    """We work out whether or not the summoner has actually played well or not, most likely not"""
    if damage_dealt < damage_taken:
        message = '\n\n> Jesus dude, you got creamed :rekt: :lololol:'
    if damage_dealt > (2.5 * damage_taken):
        message = '\n>>> *ggwp* in that last game dude :ggez:'
    return None

def greeting():
    period = get_current_hour()
    message = 'boom: Hey Summoners, here is the *Level 30* :newspaper: for this {}!!! :boom:'.format(period)
    update_l30(message)
    return None

def send_level_message(summoner):
    global message
    level = get_level(summoner)
    message = 'Yo *{}*, you are at level {}'.format(summoner,level)
    if level == 30 and summoner not in ('II uspdan II', 'Stelks'):
        message += '\n\n> Awesome work {}!!! Onwards and upwards to the toxic world of Ranked for you :thumbsup:'.format(summoner)
    update_l30(message)
    return None

def send_game_messages(summoner_id):
    """Works out a bunch of things based on the summoner id for their last game"""
    try:
        global message
        (highest_rank, champ_id, timestamp, game_mode, winner, kills, deaths, assists, damage_dealt, damage_taken, pentakills) = get_game(summoner_id)
        game_mode_test(game_mode)
        (lastplay_date, lastplay_day) = get_time(timestamp)
        champ_name = get_champ_name(champ_id)
        message = '>>> In your last game with :{}:, on {}'.format(champ_name, lastplay_day)
        update_l30(message)
        message = '```You played {} and were a {}. You had {} kills, {} deaths and {} assists! You dealt {} total damage and took {} total damage. Your current rank is {} btw!```'.format(game_mode, winner, kills, deaths, assists, damage_dealt, damage_taken, highest_rank)
        last_played_test(lastplay_date)
        played_well_test(summoner_id, damage_dealt, damage_taken)
        update_l30(message)
        abuse_test(summoner_id, champ_name)
        has_penta(pentakills)
    except Exception as e:
        print('Unknown Game Status, something failed with the Summoner ID API call!')
        print(e)
    return None


if __name__ == '__main__':
    from docopt import docopt

    try:
    # Parse arguments (from the cli), using file docstring as a parameter definition
        arguments = docopt(__doc__, version='level_check 0.4')
        api_key = str(arguments['--apikey'])
        slack_token = str(arguments['--stoken'])
        sc = SlackClient(slack_token) # Create the slack bot instance with the token we created earlier:

    # Handle invalid options with an exception
    except Exception as e:
        print(e)

    # Setting up the list of tuple of summoners and summoner ids
    summoners = [('SECURITATEM', '68520962'), ('II uspdan II', '77402230') , ('siosafoo', '64399216') , ('Stelks', '79761554')]
    summoner_data = []
    greeting()
    for (summoner, summoner_id) in summoners:
        try:
            send_level_message(summoner)
            send_game_messages(summoner_id)
        except Exception as e:
            print(e)
'''

if __name__ == '__main__':
    try:
        args = docopt(__doc__, version='level_check v0.4')
        champs = Champions(args['--apikey'])
        summoner = Summoner(args['--apikey'], 'Zirnitra')
        game = summoner.get_game()
        print(game)
    except Exception as ex:
        print(ex)
        raise
