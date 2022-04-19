from marshmallow import Schema, fields, validate


class AuthSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True, validate=[validate.Length(max=255)])
    password = fields.String(required=True, load_only=True, validate=[validate.Length(max=50)])
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)