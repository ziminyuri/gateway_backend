from marshmallow import Schema, fields


class RegisterSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)


class LoginSchema(Schema):
    username = fields.String(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)


class TokenSchema(Schema):
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)


class RefreshSchema(Schema):
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(required=True, load_only=True)
