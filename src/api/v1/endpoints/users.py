from http import HTTPStatus

from flask_restful import Resource
from api.v1.serializers.users import AuthSchema
from flask_apispec import doc, marshal_with, use_kwargs
from api.auth import guard

from db.access import UserAccess
from db.models import User

user_access = UserAccess()


class Registration(Resource):

    @use_kwargs(AuthSchema)
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        """ Регистрация нового пользователя """

        user = user_access.create(**kwargs)
        auth = guard.authenticate(kwargs['username'], kwargs['password'])
        access_token = guard.encode_jwt_token(auth)
        refresh_token = guard.encode_jwt_token(auth)

        return {
            'id': user.id,
            'username': user.username,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, HTTPStatus.CREATED


class Login(Resource):

    @use_kwargs(AuthSchema)
    @marshal_with(AuthSchema)
    def post(self, **kwargs):
        """ Авторизация пользователя """

        current_user = User.get_by_username(kwargs['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(kwargs['username'])}, \
                   HTTPStatus.NOT_FOUND
        auth = guard.authenticate(kwargs['username'], kwargs['password'])
        if auth:
            access_token = guard.encode_jwt_token(auth)
            refresh_token = guard.encode_jwt_token(auth)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, HTTPStatus.OK
        else:
            return {'message': 'Wrong credentials'}
