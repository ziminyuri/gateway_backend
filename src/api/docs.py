from flask_apispec import FlaskApiSpec

from api.v1.endpoints.roles import Role, Roles
from core.config import BLUEPRINT_API

docs = FlaskApiSpec()

docs.register(Roles, blueprint=BLUEPRINT_API)
docs.register(Role, blueprint=BLUEPRINT_API)
