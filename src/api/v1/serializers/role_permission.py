from api.v1.serializers import ma


class PermissionRoleSchema(ma.Schema):

    role_id = ma.UUID(required=True)
    permission_id = ma.UUID(required=True)
