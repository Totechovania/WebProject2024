from data import db_session
from flask import Flask
from flask_login import LoginManager

global_manager = None


def init_app():
    db_session.global_init("db/database.db")
    app = Flask('__main__')
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    init_manager(app)
    import api
    app.register_blueprint(api.blueprint)
    return app


def init_manager(app):
    global global_manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    global_manager = login_manager


def get_manager():
    return global_manager
