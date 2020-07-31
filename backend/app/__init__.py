import os

from flask import Flask

from .api import api_blueprint
from .models import db
from .schemas import ma
from .utils import get_db, setup


def create_app():
    app = Flask(__name__)
    url = get_db()
    app.config['SQLALCHEMY_DATABASE_URI'] = str(url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'abcd'
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        if url.drivername.startswith("sqlite"):
            db.create_all()
        setup()
        app.register_blueprint(api_blueprint)
    return app
