from marshmallow import Schema, fields
from .profile import ProfileSchema


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
    user_id = fields.String(dump_only=True)
    verification_code = fields.String(dump_only=True)


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
    ip_address = fields.String(dump_only=True)
    device = fields.String(dump_only=True)


class TwoFactorAuthenticationSchema(Schema):
    user_id = fields.String(load_only=True, required=True)
    code = fields.Integer(load_only=True, required=True)
    verification_code = fields.String(load_only=True, required=True)


class UserRoleSchema(Schema):
    role = fields.String()


class UserSchema(Schema):
    username = fields.String(dump_only=True)
    id = fields.String(dump_only=True)
    profile = fields.Nested(ProfileSchema(only=('email', 'last_name', 'phone', 'first_name')))
