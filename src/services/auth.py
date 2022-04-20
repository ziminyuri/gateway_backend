from http import HTTPStatus

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)

from core.config import JWT_ACCESS_TOKEN_EXPIRE, JWT_REFRESH_TOKEN_EXPIRE
from db.redis import cache


def create_tokens(user, headers):
    """ Создание токенов для авторизации """
    user_agent = headers.get('User-Agent', 'No User-Agent')
    additional_claims = get_additional_claims(user, user_agent)

    access_token = creating_access_token(user, user_agent, additional_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

    cache.setex_value(
        cache.make_key(user.id, user_agent, refresh_token=True),
        refresh_token,
        JWT_REFRESH_TOKEN_EXPIRE
    )

    return access_token, refresh_token


def creating_access_token(user, user_agent, additional_claims: dict) -> str:
    """ Создание access токена """
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

    cache.setex_value(
        cache.make_key(user.id, user_agent),
        access_token,
        JWT_ACCESS_TOKEN_EXPIRE
    )

    return access_token


def login_required(func_to_decorate):
    """ Декоратор, на проверку авторизации пользовталя """

    @jwt_required()
    def wrapper(self):
        user_agent = request.headers.get('User-Agent', 'No User-Agent')
        user_id = get_jwt_identity()
        if not is_valid_access_token(user_id, user_agent):
            if cache.get_value(cache.make_key(user_id, user_agent, refresh_token=True)):
                return {'message': 'Access token expired'}, HTTPStatus.UNAUTHORIZED
            else:
                return {'message': 'You should sign in'}, HTTPStatus.UNAUTHORIZED

        token = get_jwt()
        func_to_decorate(self, **{
            'user_agent': user_agent,
            'permissions': token['permissions'],
            'is_superuser': token['is_superuser'],
            'user_id': user_id
        })

    return wrapper


def is_valid_access_token(user_id, user_agent):
    """ Проверка, что access токен не в списке удаленных """

    token_from_request = request.headers.get('Authorization').split('Bearer ')[1]
    token_from_cache = cache.get_value(cache.make_key(user_id, user_agent))
    return True if token_from_request == token_from_cache else False


def is_valid_refresh_token(user_id, user_agent, token_from_request):
    """ Проверка, что refresh токен валидный """

    token_from_cache = cache.get_value(cache.make_key(user_id, user_agent, refresh_token=True))
    return True if token_from_request == token_from_cache else False


def get_additional_claims(user, user_agent):
    return {
        'permissions': 'permissions',
        'is_superuser': user.is_superuser,
        'user_agent': user_agent
    }
