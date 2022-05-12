import uuid
from datetime import date, timedelta
from functools import wraps

from flask import Flask, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, decode_token, get_jwt,
                                get_jwt_identity, jwt_required)
from user_agents import parse

from src.core.config import JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES
from src.db.access import AuthHistoryAccess, UserAccess
from src.db.models import User
from src.db.redis import cache
from src.services.exceptions import TokenException

jwt = JWTManager()
auth_history_access = AuthHistoryAccess()
user_access = UserAccess()


def init_jwt(app: Flask):
    jwt.init_app(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(_, jwt_data):
    jti = jwt_data['jti']
    token_from_cache = cache.get_value(jti)
    return bool(token_from_cache)


def create_tokens(user):
    """ Создание токенов для авторизации """
    user_agent = get_user_agent()
    additional_claims = get_additional_claims(user)

    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    refresh_token = creating_refresh_token(user, user_agent, additional_claims)

    return access_token, refresh_token


def creating_refresh_token(user, user_agent: str, additional_claims: dict) -> str:
    """ Создание refresh токена """
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

    cache.setex_value(
        cache.make_key(user.id, user_agent, refresh_token=True),
        decode_token(refresh_token)['jti'],
        JWT_REFRESH_TOKEN_EXPIRES
    )

    return refresh_token


def login_required(superuser=False):
    """ Декоратор, на проверку авторизации пользователя """

    def wrapper(func_to_decorate):

        @jwt_required()
        @wraps(func_to_decorate)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            token = get_jwt()

            if superuser and not token['is_superuser']:
                raise TokenException("User does not have permissions")

            kwargs.update({
                'roles': token['roles'],
                'is_superuser': token['is_superuser'],
                'user_id': user_id
            })
            return func_to_decorate(*args, **kwargs)
        return decorator

    return wrapper


def validate_refresh_token(user_id, jti):
    """ Проверка, что refresh токен валидный """

    user_agent = get_user_agent()
    token_from_cache = cache.get_value(cache.make_key(user_id, user_agent, refresh_token=True))
    if not jti == token_from_cache:
        raise TokenException('Refresh token is invalid')


def get_additional_claims(user) -> dict:
    return {
        'roles': {role.id: role.name for role in user.roles},
        'is_superuser': user.is_superuser,
    }


def deactivate_tokens(user_id, jti) -> None:
    user_agent = get_user_agent()
    cache.setex_value(jti, user_id, JWT_ACCESS_TOKEN_EXPIRES)
    cache.delete(cache.make_key(user_id, user_agent, refresh_token=True))


def deactivate_all_user_tokens(user_id) -> None:
    last_month = date.today().replace(day=1) - timedelta(1)
    all_user_auth = auth_history_access.get_all_user_auth_for_period(user_id, last_month)

    for user_auth in all_user_auth:
        cache.delete(cache.make_key(user_id, user_auth.user_agent, refresh_token=True))


def change_personal_data(personal_data):
    changes = {k: v for k, v in personal_data.items()
               if k not in ['user_id', 'roles', 'is_superuser']}
    if changes.get('username') is not None:
        User.validate_username(changes['username'])
    user_access.update(personal_data['user_id'], **changes)


def change_password(personal_data):
    new_password = personal_data['new_password']
    user = user_access.get_by_id(personal_data['user_id'])
    user.check_password(personal_data['old_password'])
    user.check_new_password(new_password)
    user_access.update(personal_data['user_id'],
                       **{'hashed_password': user.hash_password(new_password)})


def save_verification_code(user_id: uuid.UUID) -> str:
    unique_code = str(uuid.uuid4())
    key = cache.make_verification_key(user_id)
    cache.setex_value(key, unique_code, 60)
    return unique_code


def validate_verification_code(user_id: str, client_code: str):
    key = cache.make_verification_key(user_id)
    server_code = cache.get_value(key)
    if not server_code:
        raise TokenException('Verification code has expired')
    elif server_code != client_code:
        raise TokenException('Verification code is invalid')


def get_user_agent() -> str:
    return request.headers.get('User-Agent', 'No User-Agent')


def get_type_device(user_agent):
    user_agent = parse(user_agent)
    if user_agent.is_pc:
        return 'pc'
    if user_agent.is_tablet:
        return 'tablet'
    if user_agent.is_mobile:
        return 'mobile'
    return 'other'


def prepare_auth_history_params(current_user) -> dict:
    user_agent = get_user_agent()
    return {
        'user_agent': user_agent,
        'user_id': current_user.id,
        'device_type': get_type_device(user_agent),
        'ip_address': request.remote_addr
    }
