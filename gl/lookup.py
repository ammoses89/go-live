import requests


class LookUp(object):

    def __init__(self, upc):
        self.upc = upc

    def itunes(self):
        itunes_base_url = ""
        response = requests.get(itunes_base_url + self.upc)
        if response.status_code == 200:
            return response.text

    def spotify(self):
        spotify_base_url = ""
        response = requests.get(spotify_base_url + self.upc)
        if response.status_code == 200:
            return response.text
