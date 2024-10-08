from flask import Blueprint
from flask_restful import Api

from src.api.v1.endpoints import (AuthHistory, ChangePassword, Login, Logout,
                                  LogoutFromEverywhere, OauthCallback,
                                  OauthLogin, Refresh, Registration,
                                  TwoFactorAuthentication, UserRole)
from src.core.config import BLUEPRINT_AUTH_API, URL_PREFIX

auth_bp = Blueprint(BLUEPRINT_AUTH_API, __name__, url_prefix=URL_PREFIX)
auth_api = Api(auth_bp)

auth_api.add_resource(UserRole, '/user/role')

auth_api.add_resource(Login, '/auth/login')
auth_api.add_resource(OauthLogin, '/auth/login/oauth/<string:social_name>')
auth_api.add_resource(OauthCallback, '/auth/login/oauth/callback/<string:social_name>')
auth_api.add_resource(Logout, '/auth/logout')
auth_api.add_resource(LogoutFromEverywhere, '/auth/logout/device/all')
auth_api.add_resource(Registration, '/auth/registration')
auth_api.add_resource(Refresh, '/auth/refresh')

auth_api.add_resource(AuthHistory, '/auth/history')
auth_api.add_resource(TwoFactorAuthentication, '/auth/2fa')
auth_api.add_resource(ChangePassword, '/auth/password/change')
