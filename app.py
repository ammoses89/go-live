from flask import Flask, request, redirect

import gl
from gl.lookup import Lookup
import json

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

@app.route("/")
def index():
    """
    Return Basic API Info in this response
    """
    return app.send_static_file('index.html')

@app.route("/add")
def add():
    """
    This will take a upc and email
    and add it to the database for
    the worker to check

    if a duplicateKeyError is raised
    return a error response
    """
    pass

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
    pass

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
    print "Results:", results

    return json.dumps(results)

if __name__ == '__main__':
    app.run(debug=True)
