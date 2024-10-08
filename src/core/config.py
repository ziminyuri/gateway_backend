import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def update_config(app: Flask, config: dict):
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    app.config['JWT_BLACKLIST_ENABLED'] = JWT_BLACKLIST_ENABLED
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = JWT_BLACKLIST_TOKEN_CHECKS
    app.config['APISPEC_SPEC'] = APISPEC_SPEC
    app.config['APISPEC_SWAGGER_URL'] = APISPEC_SWAGGER_URL
    app.config['APISPEC_SWAGGER_UI_URL'] = APISPEC_SWAGGER_UI_URL
    # app.config['SQLALCHEMY_ECHO'] = True

    app.config['GOOGLE_CLIENT_ID'] = OAUTH_GOOGLE_CLIENT_ID
    app.config['GOOGLE_CLIENT_SECRET'] = OAUTH_GOOGLE_CLIENT_SECRET

    app.config['RECAPTCHA_SITE_KEY'] = RECAPTCHA_SITE_KEY
    app.config['RECAPTCHA_SECRET_KEY'] = RECAPTCHA_SECRET_KEY

    if config:
        app.config.update(config)


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

SECRET_KEY = os.getenv('SECRET_KEY')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access']
JWT_ACCESS_TOKEN_EXPIRES = 60 * 60
JWT_REFRESH_TOKEN_EXPIRES = 30 * 24 * 60 * 60

BLUEPRINT_ROLE_API = 'role_api'
BLUEPRINT_AUTH_API = 'auth_api'
BLUEPRINT_CAPTCHA_API = 'captcha_api'
BLUEPRINT_USER_API = 'user_api'

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

OAUTH_GOOGLE_CLIENT_ID = os.getenv('OAUTH_GOOGLE_CLIENT_ID')
OAUTH_GOOGLE_CLIENT_SECRET = os.getenv('OAUTH_GOOGLE_CLIENT_SECRET')

REQUEST_LIMIT_PER_MINUTE = 20

JAEGER_HOST = os.getenv('JAEGER_HOST')

RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
