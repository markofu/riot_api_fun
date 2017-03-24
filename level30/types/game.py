__author__ = 'Asbjorn Kjaer <akjaer@riotgames.com>'
__all__ = ()

from level30.errors import GameNotFound

class Game(object):
    def __init__(self, data):
        """
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
        """

    @property
    def game_start_timestamp(self):
        return self.info['gameInfo']['gamestartTimestamp']

    @property
    def game_mode(self):
        return self.info['gameInfo']['gameMode']

    @property
    def champion_id(self):
        return self.player['championId']

