from flask import Flask, request, redirect

import gl
from gl.lookup import Lookup
from gl.db import models

import json
import datetime

app = Flask(__name__)

def dict_to_qs(_d):
    qs = ''
    for i, (k, v) in enumerate(_d.iteritems()):
        if i == 0:
            qs += '?'
        else:
            qs += '&'
        qs += '%s=%s' % (k, v)
    return qs

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

@app.route("/")
def index():
    """
    Return Basic API Info in this response
    """
    return app.send_static_file('index.html')

@app.route("/add", methods=["POST"])
def add():
    """
    This will accept:
     - a upc
     - album_id
     - album title
     - album artist
     - a list of outlets
     - a list of emails

    and adds it to the database for
    the worker to check

    if a duplicateKeyError is raised
    return a error response
    """

    request_data = json.loads(request.data)
    # TODO validate json

    release = models.ReleaseModel.query_for_album_id(
        request_data['album_id']).get()

    if not release:
        release = models.ReleaseModel.add_release_async(**request_data)\
            .get_result()

    return json.dumps(release.to_dict(), serial=json_serial)


@app.route("/check_status", methods=["POST"])
def check_status():
    """
    This will check status for upc
    although the person should be notified by email

    Possible feature: count of times upc has been checked
    """

    request_data = json.loads(request.data)
    distributor = request_data.pop('distributor', False)
    assert distributor, "No distributor provided"
    results = Lookup.lookup_by_distributor(distributor, **request_data)
    return json.dumps({
        'status': 'OK',
        'results': results
        })


@app.route("/album_status/<album_id>", methods=["GET"])
def album_status(album_id):
    """
    Using album id get status of all outlets
    the album has been distributed too
    """

    release = models.ReleaseModel.query_for_album_id(
        album_id).get()

    if not release:
        return json.dumps({
            'error': 'Album not found'
        })
    return json.dumps(release.to_dict(), serial=json_serial)


@app.route("/api/<distributor>")
def check_is_live(distributor):
    """
    Directly checks status
    """
    upc = request.args.get('upc')
    artist = request.args.get('artist')
    album_title = request.args.get('album_title')

    distributor = distributor.lower()

    if distributor in ['amazon', 'deezer', 'google']:
        if not artist or not album_title:
            return json.dumps({
                'status': 'error',
                'message': 'Amazon lookup requires both artist and album title'
                })

    results = Lookup.lookup_by_distributor(distributor, upc=upc, artist=artist,
        title=album_title)

    return json.dumps(results)

if __name__ == '__main__':
    app.run(debug=True)
