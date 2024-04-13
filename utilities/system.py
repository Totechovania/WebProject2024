from data import db_session
from flask import Flask
from flask_login import LoginManager


def init_all():
    db_session.global_init("db/database.db")
    app = Flask('__main__')
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    login_manager = LoginManager()
    login_manager.init_app(app)
    return app, login_manager
