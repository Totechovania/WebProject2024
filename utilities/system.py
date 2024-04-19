from data import db_session
from flask import Flask
from flask_login import LoginManager
import os
from data import users


def init_all():
    if not os.path.exists("db"):
        os.mkdir("db")
    db_session.global_init("db/database.db")
    import api
    app = Flask('__main__')
    app.register_blueprint(api.blueprint)
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    login_manager = LoginManager()
    login_manager.init_app(app)
    return app, login_manager


def load_user_db(user_id):
    return db_session.create_session().query(users.User).get(user_id)
