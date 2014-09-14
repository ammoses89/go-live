import nose
from nose.tools import with_setup

from gl.db import mongo
from gl.lookup import Lookup
from gl.release import Release, Releases

import datetime

def clear_db():
    Releases.clear()

def testItunesLookup():
    """ Testing iTunes Lookup"""
    upc = "840218148053"
    lookup = Lookup(upc)
    response = lookup.itunes()
    assert response['resultCount'] == 1

def testSpotifyLookup():
    """ Testing Spotify Lookup"""
    upc = "840218148053"
    lookup = Lookup(upc)
    response = lookup.spotify()
    assert response['albums']['total'] == 1

@with_setup(clear_db, None)
def testAReleaseInsert():
    """ Testing Inserting Release"""
    params = {
      "upc": "840218148053",
      "created_at": datetime.datetime.now(),
      "updated_at": datetime.datetime.now(),
      "is_up": False
    }

    release = Release(**params)
    release_id = release.insert()
    release = Release.get(release_id)
    assert release != None
    assert release.upc == params["upc"]
    assert release.is_up == params["is_up"]

def testReleasesQuery():
    """ Testing querying releases """
    upc = "840218148053"
    params = {"is_up": False}
    releases = Releases.query(params)
    assert len(releases) > 1

    release = releases[0]
    assert release.upc == upc
