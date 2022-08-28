from marshmallow import Schema, fields


class ProfileSchema(Schema):
    email = fields.String(dump_only=True)
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    phone = fields.String(dump_only=True)
