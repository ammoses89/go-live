from flask import Flask

import gl

app = Flask()


@app.route("/")
def index():
    return


if __name__ == '__main__':
    app.run()
