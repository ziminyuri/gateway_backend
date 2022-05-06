from http import HTTPStatus

import pyotp
from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import (create_access_token, get_jwt, get_jwt_identity,
                                jwt_required)
from flask_restful import Resource

from src.api.v1.serializers.users import (AuthHistory, ChangePassword,
                                          LoginSchema, PersonalChanges,
                                          RefreshSchema, RegisterSchema,
                                          TokenSchema)
from src.db.access import AuthHistoryAccess, TotpAccess, UserAccess
from src.db.models import User
from src.services.auth import (change_password, change_personal_data,
                               create_tokens, deactivate_all_user_tokens,
                               deactivate_tokens, get_additional_claims,
                               is_valid_refresh_token, login_required,
                               prepare_auth_history_params)
from src.templates.totp_sync_template import qr_code_template
from src.utils import get_pagination_params

user_access = UserAccess()
auth_history_access = AuthHistoryAccess()
totp_access = TotpAccess()

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
            auth_history_params = prepare_auth_history_params(current_user)
            auth_history_access.create(**auth_history_params)
            return {'access_token': access_token, 'refresh_token': refresh_token},\
                HTTPStatus.OK


@doc(tags=[tag])
class Logout(MethodResource, Resource):
    @login_required()
    def get(self, **kwargs):
        jti = get_jwt()["jti"]
        deactivate_tokens(kwargs['user_id'], jti)
        return {'message': 'Logout successful'}, HTTPStatus.OK


@doc(tags=[tag])
class LogoutFromEverywhere(MethodResource, Resource):
    @login_required()
    def get(self, **kwargs):
        """ Выйти со всех устройств """
        deactivate_all_user_tokens(kwargs['user_id'])
        return {'message': 'You are logged out of all devices successfully'}, HTTPStatus.OK


@doc(tags=[tag])
class AuthHistory(MethodResource, Resource):

    @marshal_with(AuthHistory(many=True))
    @login_required()
    def get(self, **personal_data):
        """ История входов пользователя """
        res = auth_history_access.get_all(
            f"user_id = '{personal_data['user_id']}'",
            get_pagination_params()
        )
        return res, HTTPStatus.OK


@doc(tags=[tag])
class ChangePersonalData(MethodResource, Resource):

    @use_kwargs(PersonalChanges)
    @login_required()
    def post(self, **kwargs):
        """ Внесение изменений в пользовательские данные """
        change_personal_data(kwargs)
        return {'message': 'User successfully updated.'}, HTTPStatus.OK


@doc(tags=[tag])
class ChangePassword(MethodResource, Resource):

    @use_kwargs(ChangePassword)
    @login_required()
    def post(self, **kwargs):
        """ Внесение изменений в пользовательские данные """
        change_password(kwargs)
        return {'message': 'Password successfully updated.'}, HTTPStatus.OK


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


@doc(tags=[tag])
class TwoFactorAuthentication(MethodResource, Resource):

    @jwt_required(locations=['query_string'])
    def get(self):
        """Получение QR кода """
        user_id = get_jwt_identity()
        secret = pyotp.random_base32()

        saved_secret = totp_access.create(user_id=user_id, secret=secret)
        totp = pyotp.TOTP(saved_secret)
        provisioning_url = totp.provisioning_uri(name=user_id + '@some.ru',
                                                 issuer_name='Auth service')
        tmpl = qr_code_template % provisioning_url
        headers = {'Content-Type': 'text/html'}
        return make_response(tmpl, 200, headers)

    def post(self, user_id, **kwargs):
        pass
