from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentNum = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(30))
    birthDate = db.Column(db.Integer)
    male = db.Column(db.Boolean)

    @property
    def collegeName(self):
        return self.cls.subject.college.name

    @property
    def subjectName(self):
        return self.cls.subject.name

    @property
    def className(self):
        return self.cls.name

    cls_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    scores = db.relationship("Score", backref="student", )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_try = db.Column(db.Integer)
    second_try = db.Column(db.Integer)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship(
        'Course', foreign_keys='Score.course_id', lazy='select'
    )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    type = db.Column(db.Integer)
    credit = db.Column(db.Float)

    cls_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship(
        'Teacher', foreign_keys='Course.teacher_id', lazy='select'
    )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    students = db.relationship("Student", backref="cls", )
    courses = db.relationship("Course", backref="cls", )
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    subjects = db.relationship("Subject", backref="college", )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    classes = db.relationship("Class", backref="subject", )

    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    schedule = db.relationship(
        'Schedule', foreign_keys='Subject.schedule_id', lazy='select'
    )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    min_compulsory_credit = db.Column(db.Integer)
    min_elective_credit = db.Column(db.Integer)
    min_limited_credit = db.Column(db.Integer)

    max_compulsory_fail_credit = db.Column(db.Integer)
    max_elective_fail_credit = db.Column(db.Integer)
    max_limited_fail_credit = db.Column(db.Integer)
