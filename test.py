__author__ = 'Asbjorn Kjaer <akjaer@riotgames.com>'
__all__ = ()

from level30.api import RiotAPI

api = RiotAPI('RGAPI-9BA243BB-E392-4AC1-B4F5-18B60A7B75B6', 'na')
print(api.get_champions())
