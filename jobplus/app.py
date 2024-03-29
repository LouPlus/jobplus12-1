from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment

from jobplus.filters import add_link_suffix
from jobplus.models import db, User
from jobplus.handlers import *


def register_blueprint(app):
    app.register_blueprint(front)
    app.register_blueprint(user)
    app.register_blueprint(seeker)
    app.register_blueprint(job)
    app.register_blueprint(company)
    app.register_blueprint(tag)
    app.register_blueprint(admin)
    app.register_blueprint(resume)
    app.register_blueprint(experience)
    app.register_blueprint(education)
    app.register_blueprint(project)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    moment = Moment(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    login_manager.login_view = 'front.login'





def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.add_template_filter(add_link_suffix)

    register_blueprint(app)
    register_extensions(app)

    return app
