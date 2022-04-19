from api.v1.serializers import ma


class UserRoleSchema(ma.Schema):

    user_id = ma.UUID(required=True)
    role_id = ma.UUID(required=True)
