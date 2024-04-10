from data import db_session
import api
from flask import Flask


def init_all():
    app = Flask('__main__')
    app.register_blueprint(api.blueprint)
    print(app)
    return app
