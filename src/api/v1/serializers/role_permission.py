from src.api.v1.serializers import ma


class PermissionRoleSchema(ma.Schema):
    role_id = ma.UUID(required=True)
    permission_id = ma.UUID(required=True)


def role_permission_args_parse(**kwargs):
    role_id = kwargs['role_id']
    permission_id = kwargs['permission_id']
    return {
        'role_id': role_id,
        'permission_id': permission_id
    }
