from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTDecodeError


def validate_token(token: str) -> dict:
    token = decode_token(token)
    if token['type'] == 'refresh':
        raise JWTDecodeError('Token is invalid')

    return token
