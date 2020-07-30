from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(api_blueprint, version="v1", doc='/docs')
