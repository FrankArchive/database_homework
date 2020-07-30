import os

from flask import Flask
from flask_migrate import Migrate, upgrade, migrate

from .api import api_blueprint
from .models import *
from .schemas import ma
from .utils import get_db, setup


mi = Migrate()


def create_app():
    app = Flask(__name__)
    url = get_db()
    app.config['SQLALCHEMY_DATABASE_URI'] = str(url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'abcd'
    with app.app_context():
        db.init_app(app)
        mi.init_app(app, db)
        ma.init_app(app)
        db.drop_all()
        if url.drivername.startswith("sqlite"):
            db.create_all()
        else:
            upgrade()
            # pass
        app.register_blueprint(api_blueprint)
    return app
