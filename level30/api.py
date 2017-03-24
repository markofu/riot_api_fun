__author__ = 'Asbjorn Kjaer <akjaer@riotgames.com>'
__all__ = ('RiotAPI',)

import requests

APIS = {
    'game': {
        'global': False,
        'version': 'v1.3',
        'functions': {
            'by-summoner': ['{summonerId}/recent']
        }
    },
    'summoner': {
        'global': False,
        'version': 'v1.4',
        'functions': {
            'by-name': ['{summonerName}'],
            'by-id': ['{summonerId}']
        }
    },
    'static-data': {
        'global': True,
        'version': 'v1.2',
        'functions': {
            'champion': None
        }
    }
}

BASE_REGIONAL_HOST = 'https://{region}.api.pvp.net/api/lol/{region}/'
BASE_GLOBAL_HOST = 'https://global.api.pvp.net/api/lol/static-data/na/'

URLS = {}

for api, info in list(APIS.items()):
    for func, args in list(info['functions'].items()):
        base = BASE_GLOBAL_HOST if info['global'] else BASE_REGIONAL_HOST
        if args:
            path = "/".join([info['version'], api, func] + args)
        else:
            path = "/".join((info['version'], api, func))
        URLS['{}-{}'.format(api,func)] = base + path + "?api_key={api_key}"


class RiotAPI(object):
    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region

    def get_summoner_by_name(self, name):
        url = URLS['summoner-by-name'].format(
            region=self.region,
            summonerName=name,
            api_key=self.api_key
        )
        return requests.get(url).json()

    def get_summoner_by_id(self, id):
        url = URLS['summoner-by-id'].format(
            region=self.region,
            summonerId=id,
            api_key=self.api_key)
        return requests.get(url).json()

    def get_champions(self):
        url = URLS['static-data-champion'].format(api_key=self.api_key)
        print(url)
        return requests.get(url).json()
