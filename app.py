import os
import pymysql
from flask import Flask
from flask import render_template

import config as cfg
from core.last_searches import last_searches_page
from core.login import login_page
from core.result import result_page
from core.search import search_page


app = Flask(__name__)
app.register_blueprint(search_page)
app.register_blueprint(result_page)
app.register_blueprint(last_searches_page)
app.register_blueprint(login_page)



@app.route("/")
def index():
    return render_template('login.html', wrongTry=0)


@app.route("/about")
def about():
    return render_template('about.html')


@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error=e)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host=cfg.host, port=cfg.port)
