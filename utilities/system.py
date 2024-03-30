from data import db_session
import api
from flask import Flask


def init_all(name):
    app = Flask(name)
    app.register_blueprint(api.blueprint)
    return app
