from flask import Blueprint
from flask_restx import Api, Resource

from app.models import Student
from .schemas import StudentSchema

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_blueprint, version="v1", doc='/docs')


@api.route('/student/<string:key>/<string:val>')
class StudentEndpoint(Resource):
    @staticmethod
    def get(key, val):
        try:
            student = Student.query.filter_by(
                **{key: val}
            ).first_or_404()
            return StudentSchema().dump(student)
        except:
            return {'message': 'no such student'}, 404


@api.route('/student/firing')
class StudentFiringEndpoint(Resource):
    def get(self):
        pass
