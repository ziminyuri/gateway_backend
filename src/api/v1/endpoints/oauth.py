from http import HTTPStatus

from flask import url_for
from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource
from flask_restful import Resource
from werkzeug import exceptions

from src.api.v1.serializers.users import TokenSchema
from src.services.oauth import create_tokens, oauth

tag = 'Oauth'


@doc(tags=[tag])
class OauthLogin(MethodResource, Resource):
    def get(self, social_name):
        """ Авторизация пользователя через OAuth"""
        client = oauth.create_client(social_name)

        if not client:
            raise exceptions.NotFound()

        redirect_url = url_for('auth_api.oauthcallback', social_name=social_name, _external=True)

        return client.authorize_redirect(redirect_url)


@doc(tags=[tag])
class OauthCallback(MethodResource, Resource):
    @marshal_with(TokenSchema)
    def get(self, social_name):
        """ Callbacks от внешней системы авторизии по oauth"""

        client = oauth.create_client(social_name)
        access_token, refresh_token = create_tokens(client, social_name)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
