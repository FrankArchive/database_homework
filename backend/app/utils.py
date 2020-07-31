import os

from flask import current_app
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import create_database, database_exists

from .models import *


def get_db():
    url = make_url(os.getenv('DB_URL') or 'sqlite:///test.db')
    if url.drivername.startswith('mysql'):
        url.query["charset"] = "utf8mb4"
    if not database_exists(url):
        if url.drivername.startswith("mysql"):
            create_database(url, encoding="utf8mb4")
        else:
            create_database(url)
    return url


def setup():
    with current_app.app_context():
        college = College(
            name='网络与信息安全学院'
        )
        db.session.add(college)
        subject = Subject(
            name='网络空间安全',
            college=college
        )
        db.session.add(subject)
        cls = Class(
            name='1818039'
        )
        db.session.add(cls)
        teacher = Teacher(
            name='张老师'
        )
        db.session.add(teacher)
        course1 = Course(
            name='数学',
            teacher=teacher,
            cls=cls
        )
        db.session.add(course1)
        db.session.add(Student(
            studentNum='18130500303',
            name='李轩哲',
            cls=cls,
            male=True,
        ))
        db.session.commit()
