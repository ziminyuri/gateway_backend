from flask_restx import fields

from api.v1.endpoints import user_ns
from api.v1.serializers import ma
from db.models import User

user_model = user_ns.model('User', {
    'id': fields.String(description='User uuid'),
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
