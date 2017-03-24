__author__ = 'Asbjorn Kjaer <akjaer@riotgames.com>'
__all__ = ()

from level30.errors import SummonerNotFound


class Summoner(object):
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
