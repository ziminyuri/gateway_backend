import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def update_config(app: Flask):
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    app.config['JWT_BLACKLIST_ENABLED'] = JWT_BLACKLIST_ENABLED
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = JWT_BLACKLIST_TOKEN_CHECKS
    app.config['APISPEC_SPEC'] = APISPEC_SPEC
    app.config['APISPEC_SWAGGER_URL'] = APISPEC_SWAGGER_URL
    app.config['APISPEC_SWAGGER_UI_URL'] = APISPEC_SWAGGER_UI_URL


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

SECRET_KEY = os.getenv('SECRET_KEY')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access']
JWT_ACCESS_TOKEN_EXPIRES = 15 * 60
# JWT_ACCESS_TOKEN_EXPIRES = 30
JWT_REFRESH_TOKEN_EXPIRES = 30 * 24 * 60 * 60

BLUEPRINT_API = 'api'
URL_PREFIX = '/api/v1'

APISPEC_SPEC = APISpec(
    title='auth',
    version='v1',
    openapi_version='2.0.0',
    plugins=[MarshmallowPlugin()],
)
APISPEC_SWAGGER_URL = '/swagger/'
APISPEC_SWAGGER_UI_URL = '/swagger-ui/'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
