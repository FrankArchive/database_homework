from flask_marshmallow import Marshmallow
from marshmallow import fields

from .models import Student

ma = Marshmallow()


class StudentSchema(ma.SQLAlchemyAutoSchema):
    studentId = fields.Integer(attribute='id')
    className = fields.Str()
    views = {
        'public': [
            'studentId', 'name', 'birthDate', 'male',
            'studentNum', 'className', 'collegeName', 'subjectName',
        ]
    }

    class Meta:
        model = Student
        include_fk = True

    def __init__(self, view='public', *args, **kwargs):
        if view:
            kwargs['only'] = self.views[view]
        super(StudentSchema, self).__init__(*args, **kwargs)
