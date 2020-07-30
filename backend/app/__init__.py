import os

from flask import Flask
from flask_migrate import upgrade, Migrate
from sqlalchemy_utils import create_database, database_exists

from .api import api_blueprint
from .utils import get_db

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    url = get_db()
    app.config['SQLALCHEMY_DATABASE_URI'] = str(url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'abcd'
    with app.app_context():
        from .models import db
        db.init_app(app)
        migrate.init_app(app, db)

        if not database_exists(url):
            if url.drivername.startswith("mysql"):
                create_database(url, encoding="utf8mb4")
            else:
                create_database(url)
        if url.drivername.startswith("sqlite"):
            db.create_all()
        else:
            upgrade()
            pass
        app.register_blueprint(api_blueprint)
    return app
