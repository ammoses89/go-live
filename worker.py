"""
Worker will check releases every 3 hours

A while loop
That every 3 hours, queries the mongodb for releases that have not been checked in 3 hours
Then using gevent lookup for each DSP
If the release is up set the right property to is_up
another worker that runs every 5 hours will send emails

"""

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from time import sleep
import datetime

from gl.release import Releases
from gl.lookup import Lookup

def itunes_lookup(release):
    upc = release.upc
    lookup = Lookup(upc)
    result = lookup.itunes(upc)
    if result['resultCount'] == 1:
       release.is_up_itunes = True
    return release

def spotify_lookup(release):
    upc = release.upc
    lookup = Lookup(upc)
    result = lookup.spotify(upc)
    if result['albums'].get('total', None) == 1:
       release.is_up_spotify = True
    return release

def run_check():
    params = {}
    releases = Releases.query(params)
    pool = Pool(5)
    releases = pool.map(itunes_lookup, releases)
    Releases.update(releases)
    releases = pool.map(spotify_lookup, releases)
    Releases.update(releases)

def run():
    while True:
        print "Running lookup worker"
        run_check()
        sleep(3 * 60 * 60) # 3 hours
