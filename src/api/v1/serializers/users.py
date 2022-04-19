from marshmallow import Schema, fields


class AuthSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)


class RefreshSchema(Schema):
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(load_only=True)
    message = fields.String(dump_only=True)
