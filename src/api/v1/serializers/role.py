from src.api.v1.serializers import ma
from src.db.models import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)

    class Meta:
        model = Role


def role_args_parse(**kwargs):
    name = kwargs['name']
    return {'name': name}
