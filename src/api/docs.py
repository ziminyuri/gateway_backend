from flask_apispec import FlaskApiSpec

from api.v1.endpoints import Role, Roles, UserRole, UserRoleManager
from core.config import BLUEPRINT_API

docs = FlaskApiSpec()

docs.register(Roles, blueprint=BLUEPRINT_API)
docs.register(Role, blueprint=BLUEPRINT_API)
docs.register(UserRole, blueprint=BLUEPRINT_API)
docs.register(UserRoleManager, blueprint=BLUEPRINT_API)
