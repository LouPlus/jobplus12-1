from flask import Flask
from flask_migrate import Migrate

from jobplus.models import db


def register_blueprint(app):
    from jobplus.handlers import front
    app.register_blueprint(front)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprint(app)
    register_extensions(app)

    return app
