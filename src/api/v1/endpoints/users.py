from http import HTTPStatus

from flask import request
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import decode_token
from flask_restful import Resource

from api.v1.serializers.users import AuthSchema, RefreshSchema
from db.access import UserAccess
from db.models import User
from db.redis import cache
from services.auth import (create_tokens, creating_access_token,
                           get_additional_claims, is_valid_refresh_token,
                           login_required)

user_access = UserAccess()

tag = 'User'


@doc(tags=[tag])
class Registration(MethodResource, Resource):

    @use_kwargs(AuthSchema)
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        """ Регистрация нового пользователя """

        if User.get_by_username(kwargs['username']):
            return {'message': 'User {} already exists'.format(kwargs['username'])}, \
                   HTTPStatus.BAD_REQUEST

        user = user_access.create(**kwargs)
        return {
            'id': user.id,
            'username': user.username
        }, HTTPStatus.CREATED


@doc(tags=[tag])
class Login(MethodResource, Resource):

    @use_kwargs(AuthSchema)
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        """ Авторизация пользователя """

        current_user = User.get_by_username(kwargs['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(kwargs['username'])}, \
                   HTTPStatus.NOT_FOUND
        if current_user.check_password(kwargs['password']):
            access_token, refresh_token = create_tokens(current_user, request.headers)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, HTTPStatus.OK
        else:
            return {'message': 'Wrong credentials'}, HTTPStatus.FORBIDDEN


@doc(tags=[tag])
class Logout(MethodResource, Resource):
    @login_required
    def get(self, **kwargs):
        cache.delete(cache.make_key(kwargs['user_id'], kwargs['user_agent']))
        cache.delete(cache.make_key(kwargs['user_id'], kwargs['user_agent'], refresh_token=True))
        return {'message': 'Logout successful'}, HTTPStatus.OK


@doc(tags=[tag])
class SecretResource(MethodResource, Resource):
    @login_required
    def get(self, **personal_data):
        """ URL для провекри работы токена """
        return {}, HTTPStatus.OK


@doc(tags=[tag])
class Refresh(MethodResource, Resource):

    @use_kwargs(RefreshSchema)
    @marshal_with(RefreshSchema)
    def post(self, **kwargs):
        decoded_token = decode_token(kwargs['refresh_token'])
        if is_valid_refresh_token(decoded_token['sub'], decoded_token['user_agent'],
                                  kwargs['refresh_token']):
            user = User.identify(decoded_token['sub'])
            user_agent = request.headers.get('User-Agent', 'No User-Agent')
            additional_claims = get_additional_claims(user, user_agent)
            return {
                'access_token': creating_access_token(user, user_agent, additional_claims)
            }, HTTPStatus.OK
        else:
            return {'message': 'Refresh token is expired'}, HTTPStatus.UNAUTHORIZED
