from flask import Blueprint, request
from flask_restx import Api, Resource

from .models import *
from .schemas import StudentSchema
from .utils import get_scores

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_blueprint, version="v1", doc='/docs')


@api.route('/student/<string:key>/<string:val>')
class StudentSingleEndpoint(Resource):
    @staticmethod
    def get(key, val):
        try:
            student = Student.query.filter_by(
                **{key: val}
            ).first_or_404()
            return StudentSchema().dump(student)
        except:
            return {'message': 'no such student'}, 404


@api.route('/student')
class StudentEndpoint(Resource):
    @staticmethod
    def get():
        page = int(request.args.get('pageNum', 1))
        per_page = int(request.args.get('pageSize', 10))
        return {
            'content': StudentSchema(many=True).dump(
                Student.query.paginate(page, per_page).items
            )
        }

    @staticmethod
    def post():
        pass


@api.route('/student/firing')
class StudentFiringEndpoint(Resource):
    def get(self):
        result = []
        for student in Student.query.all():
            scores, fails = get_scores(student)
            schedule = student.cls.subject.schedule
            if scores[0] < schedule.min_compulsory_credit:
                result.append(student)
            elif scores[1] < schedule.min_limited_credit:
                result.append(student)
            elif scores[2] < schedule.min_elective_credit:
                result.append(student)

        return StudentSchema(many=True).dump(result)


@api.route('/student/fired')
class StudentFiredEndpoint(Resource):
    def get(self):
        result = []
        for student in Student.query.all():
            scores, fails = get_scores(student)
            schedule = student.cls.subject.schedule
            if fails[0] > schedule.max_compulsory_fail_credit:
                result.append(student)
            elif fails[1] > schedule.max_limited_fail_credit:
                result.append(student)
            elif fails[2] > schedule.max_elective_fail_credit:
                result.append(student)

        return StudentSchema(many=True).dump(result)


@api.route('/student/score')
class StudentScoreEndpoint(Resource):
    def get(self):
        result = []
        student_id = request.args.get('id')
        if not student_id:
            return {'message': '?'}, 404
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': '?'}, 404
        for i in student.scores:
            result.append({
                'courseName': i.course.name,
                'firstScore': i.first_try,
                'secondScore': i.second_try,
                'courseType': i.course.type,
                'courseCredit': i.course.credit,
            })
        return result


@api.route('/student/teacher')
class StudentTeacherEndpoint(Resource):
    def get(self):
        pass


@api.route('/data')
class NewDataEndpoint(Resource):
    @staticmethod
    def post():
        data = request.json
        cls = Class.query.filter_by(name=data['className']).first()
        subject = Subject.query.filter_by(name=data['subjectName']).first()
        college = College.query.filter_by(name=data['collegeName']).first()
        if not college:
            college = College(name=data['collegeName'])
            db.session.add(college)
        if not subject:
            schedule = Schedule(
                min_compulsory_credit=22,
                min_elective_credit=10,
                min_limited_credit=6,
                max_compulsory_fail_credit=10,
                max_elective_fail_credit=30,
                max_limited_fail_credit=20,
            )
            subject = Subject(
                name=data['subjectName'], college=college,
                schedule=schedule
            )
            db.session.add(schedule)
            db.session.add(subject)
        if not cls:
            cls = Class(name=data['className'], subject=subject)
            db.session.add(cls)
        db.session.commit()
        assert cls.subject_id == subject.id
        assert subject.college_id == college.id
        student = Student(
            name=data['studentName'],
            male=data['studentIsMale'],
            studentNum=data['studentNum'],
            birthDate=data['studentBirthDate'],
            cls=cls
        )
        db.session.add(student)

        for name, type, credit, prefix in (
                ('语文', 0, 10, 'chinese'),
                ('数学', 0, 10, 'math'),
                ('英语', 0, 8, 'english'),
                ('限选', 1, 10, 'xianXuan'),
                ('任选', 2, 6, 'renXuan'),
                # 先hard code在这吧。。。越写越成gibberish
        ):
            course = Course.query.filter_by(
                name=name, cls_id=student.cls_id
            ).first()
            if not course:
                course = Course(
                    name=name, type=type,
                    credit=credit, cls=student.cls,
                    teacher=Teacher(
                        name=data[prefix + 'TeacherName']
                    )
                    # 如果当前班级已有此课程，则忽略表单中的教师名称（就当是记错了）
                )
                db.session.add(course)
            score = Score(
                first_try=data[prefix + 'FirstScore'],
                second_try=data[prefix + 'SecondScore'],
                student=student,
                course=course,
            )
            db.session.add(score)
        db.session.commit()
        return {}
