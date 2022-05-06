from pathlib import Path

from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import JWTDecodeError


def validate_token(token: str) -> dict:
    token = decode_token(token)
    if token['type'] == 'refresh':
        raise JWTDecodeError('Token is invalid')

    return token


def get_credentials():
    path = Path(__file__).parent
    with open(path.joinpath('certificates/server.key'), 'rb') as f:
        server_key = f.read()
    with open(path.joinpath('certificates/server.pem'), 'rb') as f:
        server_cert = f.read()
    with open(path.joinpath('certificates/ca.pem'), 'rb') as f:
        ca_cert = f.read()

    return server_key, server_cert, ca_cert
