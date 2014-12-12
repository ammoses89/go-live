import sys
import requests
import ujson
import oauth2 as oauth
import urllib
from bs4 import BeautifulSoup

from settings import CONSUMER_KEY, CONSUMER_SECRET

ITUNES_BASE_URL = "http://itunes.apple.com/lookup"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/search"
RDIO_BASE_URL = "http://api.rdio.com/1/"
AMAZON_BASE_URL = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords="

def keyword_gen(*args):
    keywords = []
    for arg in args:
        keywords.append(arg)
    keywords = ' '.join(keywords)
    return '+'.join(keywords.split(' '))


class Lookup(object):
    """The Lookup class represents objects used to lookup releases on DSPs"""

    def __init__(self, upc=None, title=None, artist=None):
        self.upc = upc
        self.title = title
        self.artist = artist

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
        response = client.request(RDIO_BASE_URL,
                                  'POST',
                                  urllib.urlencode(
                                    {'method': 'getAlbumsByUPC',
                                     'upc': self.upc}))
        response = ujson.loads(response[1])
        if response["status"] == "ok":
            return response["result"]

    def amazon(self):
        title = self.title or ''
        artist = self.artist or ''

        keyword = keyword_gen(title, artist)

        url = AMAZON_BASE_URL + keyword
        print url
        response = requests.get(AMAZON_BASE_URL + keyword)

        print response.status_code
        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            div_elements = soup.find_all('div', class_="mp3Cell")
            if div_elements:
                div = div_elements[0]
                a = div.find_all('a')[0]
                return a['href']
        return False




if __name__ == '__main__':
    dsp = sys.argv[1]
    upc = sys.argv[2]
    if len(sys.argv) > 3:
        title = sys.argv[2]
        artist = sys.argv[3]
        lookup = Lookup(title=title, artist=artist)
    else:
        upc = sys.argv[2]
        lookup = Lookup(upc)
    dsp_lookup = getattr(lookup, dsp.lower())
    print dsp_lookup()

