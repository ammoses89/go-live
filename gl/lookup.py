import requests
import ujson
import oauth2 as oauth
import urllib

from settings import CONSUMER_KEY, CONSUMER_SECRET

ITUNES_BASE_URL = "http://itunes.apple.com/lookup"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/search"


class Lookup(object):
    """The Lookup class represents objects used to lookup releases on DSPs"""

    def __init__(self, upc):
        self.upc = upc

    def itunes(self):
        response = requests.get(ITUNES_BASE_URL,
                                params={"upc": self.upc})
        if response.status_code == 200:
            return ujson.loads(response.text)

    def spotify(self):
        response = requests.get(SPOTIFY_BASE_URL,
                                params={"q": "upc:"+self.upc,
                                        "type": "album"})
        if response.status_code == 200:
            return ujson.loads(response.text)

    def rdio(self):
        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)
        response = client.request('http://api.rdio.com/1/',
                                  'POST',
                                  urllib.urlencode(
                                    {'method': 'getAlbumsByUPC',
                                     'upc': self.upc}))
        response = ujson.loads(response[1])
        if response["status"] == "ok":
            return response["result"]
