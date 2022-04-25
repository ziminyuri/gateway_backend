from src.api.v1.serializers import ma
from src.db.models import Permission


class PermissionSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field(dump_only=True)

    class Meta:
        model = Permission


def permissions_args_parse(**kwargs):
    name = kwargs['name']
    return {'name': name}
