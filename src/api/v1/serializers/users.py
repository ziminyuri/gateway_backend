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


class PersonalChanges(Schema):
    username = fields.String(load_only=True)


class ChangePassword(Schema):
    old_password = fields.String(load_only=True, required=True)
    new_password = fields.String(load_only=True, required=True)


class AuthHistory(Schema):
    login_at = fields.DateTime(dump_only=True)
    user_agent = fields.String(dump_only=True)
