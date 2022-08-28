from src.api.v1.serializers import ma


class UserRoleSchema(ma.Schema):

    role_id = ma.Int(required=True)
    user_id = ma.UUID(required=True)


def role_user_args_parse(**kwargs):
    role_id = kwargs['role_id']
    user_id = kwargs['user_id']
    return {
        'role_id': role_id,
        'user_id': user_id
    }
