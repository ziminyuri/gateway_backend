from flask import Blueprint
from flask_restful import Api

from src.api.v1.endpoints import (Users)
from src.core.config import BLUEPRINT_USER_API, URL_PREFIX

user_bp = Blueprint(BLUEPRINT_USER_API, __name__, url_prefix=URL_PREFIX)
user_api = Api(user_bp)

user_api.add_resource(Users, '/users')
