import uuid

from authlib.integrations.flask_client import OAuth
from flask import Flask

from src.db.access import AuthHistoryAccess, SocialAccountAccess, UserAccess
from src.services.auth import create_tokens as creating_tokens
from src.services.auth import prepare_auth_history_params

oauth = OAuth()

social_account_access = SocialAccountAccess()
user_access = UserAccess()
auth_history_access = AuthHistoryAccess()

oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
            "scope": "openid email profile"
        }
    )


def init_oauth(app: Flask):
    oauth.init_app(app)


def create_tokens(client, social_name: str):
    """ Создание токенов для авторизации """

    token = client.authorize_access_token()
    user_info = token.get("userinfo")

    current_user = user_access.get_by_username_or_none(user_info['email'])
    if not current_user:
        current_user = user_access.create(**{
            'username': user_info['email'],
            'password': str(uuid.uuid4())
        })

    social_account = \
        social_account_access.get_by_id_and_social_account(user_info['sub'], social_name)

    if not social_account:
        social_account_access.create(**{
            'id': user_info['sub'],
            'social_name': social_name,
            'user_id': current_user.id
        })

    auth_history_params = prepare_auth_history_params(current_user)
    auth_history_access.create(**auth_history_params)

    return creating_tokens(current_user)
