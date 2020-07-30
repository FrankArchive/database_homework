import os

from sqlalchemy.engine.url import make_url


def get_db():
    url = make_url(os.getenv('DB_URL') or 'sqlite:///test.db')
    if url.drivername.startswith('mysql'):
        url.query["charset"] = "utf8mb4"
    return url
