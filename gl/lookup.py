import sys
import requests
import oauth2 as oauth
import urllib
from bs4 import BeautifulSoup
import json

from settings import CONSUMER_KEY, CONSUMER_SECRET

ITUNES_BASE_URL = "http://itunes.apple.com/lookup"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/search"
RDIO_BASE_URL = "http://api.rdio.com/1/"
AMAZON_BASE_URL = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords="
DEEZER_BASE_URL = "http://api.deezer.com/search/album?q="
GOOGLE_BASE_URL = "https://play.google.com/store/search?q=%s&c=music"

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

    def result_not_found(self, distro):
        return {
            'status': "Noop",
            'message': "Album from %s with title %s is not on %s..yet." \
                % (self.artist, self.title, distro),
            'color': 'red',
            'albumLink': ''
        }

    def result_found(self, distro, link):
        return {
            'status': "YES!",
            'color': "green",
            'message': 'The album is up! Here is the link:',
            'albumLink': link
        }

    def itunes(self):
        response = requests.get(ITUNES_BASE_URL,
                                params={"upc": self.upc})
        if response.status_code == 200:
            results = json.loads(response.text)
            if results['results']:
                link = results['results'][0]['collectionViewUrl']
                return self.result_found('iTunes', link)
            else:
                return results

        return self.result_not_found('iTunes')

    def spotify(self):
        response = requests.get(SPOTIFY_BASE_URL,
                                params={"q": "upc:"+self.upc,
                                        "type": "album"})
        if response.status_code == 200:
            results = json.loads(response.text)
            if results['albums']['items']:
                item = results['albums']['items'][0]
                link = item['external_urls']['spotify']
                return self.result_found('Spotify', link)

        return self.result_not_found('Spotify')

    def rdio(self):
        consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        client = oauth.Client(consumer)
        response = client.request(RDIO_BASE_URL,
                                  'POST',
                                  urllib.urlencode(
                                    {'method': 'getAlbumsByUPC',
                                     'upc': self.upc}))
        response = json.loads(response[1])
        if response["status"] == "ok":
            results = response["result"]
            if results:
                link = "http://www.rdio.com" + results[0]['url']
                return self.result_found("Rdio", link)
            else:
                return results

        return self.result_not_found('Rdio')

    def amazon(self):
        title = self.title or ''
        artist = self.artist or ''

        keyword = keyword_gen(title, artist)

        url = AMAZON_BASE_URL + keyword
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            div_elements = soup.find_all('div', class_="mp3Cell")
            if div_elements:
                div = div_elements[0]
                a = div.find_all('a')[0]
                return self.result_found('Amazon', a['href'])
        return self.result_not_found('Amazon')

    def deezer(self):
        title = self.title or ''
        artist = self.artist or ''

        query = artist + " " + title

        url = DEEZER_BASE_URL + query
        response = requests.get(url)


        if response.status_code == 200:
           res_dict = response.json()
           if res_dict['data']:
                link = res_dict['data'][0]['link']
                return self.result_found('Deezer', link)

        return self.result_not_found('Deezer')

    def google(self):
        title = self.title or ''
        artist = self.artist or ''

        query = artist + " " + title

        url = GOOGLE_BASE_URL % query
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            headings = soup.find_all('h1', class_='cluster-heading')
            for heading in headings:
                title_links = heading.find_all('a', class_='title-link')
                for title_link in title_links:
                    if title_link.text.lower() == 'albums':
                        div = heading.find_next_sibling('div')
                        if div:
                            a = div.find_all('a', class_='title')[0]
                            link = "https://play.google.com" + a['href']
                            return self.result_found('Google Play', link)
        return self.result_not_found('Google Play')


    @classmethod
    def lookup_by_distributor(cls, distributor, **kwargs):
        lookup = cls(**kwargs)
        lookup_method = getattr(lookup, distributor, False)
        if not lookup_method:
            raise Exception("Distributor %s not yet supported" % distributor)
        return lookup_method()


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
    print json.dumps(dsp_lookup(), indent=4, separators=(',', ':'))

