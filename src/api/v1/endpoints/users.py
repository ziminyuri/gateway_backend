from http import HTTPStatus

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource

from api.v1.serializers.users import (LoginSchema, RefreshSchema,
                                      RegisterSchema, TokenSchema)
from db.access import UserAccess
from db.models import User
from services.auth import (create_tokens, deactivate_tokens,
                           get_additional_claims, is_valid_refresh_token,
                           login_required)

user_access = UserAccess()

tag = 'User'


@doc(tags=[tag])
class Registration(MethodResource, Resource):

    @use_kwargs(RegisterSchema)
    @marshal_with(RegisterSchema)
    def post(self, **kwargs):
        """ Регистрация нового пользователя """

        User.validate_username(kwargs['username'])
        user = user_access.create(**kwargs)
        return user, HTTPStatus.CREATED


@doc(tags=[tag])
class Login(MethodResource, Resource):

    @use_kwargs(LoginSchema)
    @marshal_with(TokenSchema)
    def post(self, **kwargs):
        """ Авторизация пользователя """

        current_user = user_access.get_by_username(kwargs['username'])

        if current_user.check_password(kwargs['password']):
            access_token, refresh_token = create_tokens(current_user)

            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, HTTPStatus.OK


@doc(tags=[tag])
class Logout(MethodResource, Resource):
    @login_required()
    def get(self, **kwargs):
        jti = get_jwt()["jti"]
        deactivate_tokens(kwargs['user_id'], jti)
        return {'message': 'Logout successful'}, HTTPStatus.OK


@doc(tags=[tag])
class SecretResource(MethodResource, Resource):
    @login_required()
    def get(self, **personal_data):
        """ URL для проверки работы токена """
        return {}, HTTPStatus.OK


@doc(tags=[tag])
class Refresh(MethodResource, Resource):

    @jwt_required(refresh=True, locations=['json'])
    @use_kwargs(RefreshSchema)
    @marshal_with(RefreshSchema)
    def post(self, **kwargs):
        decoded_token = get_jwt()
        jti = decoded_token['jti']
        user_id = decoded_token['sub']

        if is_valid_refresh_token(user_id, jti):
            user = User.identify(user_id)
            additional_claims = get_additional_claims(user)

            return {'access_token': create_access_token(
                str(user.id),
                additional_claims=additional_claims
            )}, HTTPStatus.OK
