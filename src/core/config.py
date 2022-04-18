import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def update_config(app: Flask):
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["JWT_ACCESS_LIFESPAN"] = JWT_ACCESS_LIFESPAN
    app.config['APISPEC_SPEC'] = APISPEC_SPEC
    app.config['APISPEC_SWAGGER_URL'] = APISPEC_SWAGGER_URL
    app.config['APISPEC_SWAGGER_UI_URL'] = APISPEC_SWAGGER_UI_URL
    app.extensions['restx'] = {'apidoc_registered': True}


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_URL = os.getenv('POSTGRES_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ACCESS_LIFESPAN = {"hours": 1}

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
