from flask import Flask

import gl
import ujson

app = Flask(__name__)


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

@app.route("/check_status/<upc>")
def check_status(upc):
    """
    This will check status for upc
    although the person should be notified by email

    Possible feature: count of times upc has been checked
    """
    pass



if __name__ == '__main__':
    app.run()
