from flask_restx import fields

from api.v1.endpoints import role_ns
from api.v1.serializers import ma
from db.models import Role

role_model = role_ns.model('Role', {
    'id': fields.String(description='Role uuid'),
    'name': fields.String(required=True,
                          description='Role name')
})


class RoleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Role
