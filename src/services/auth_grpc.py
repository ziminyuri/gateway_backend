import grpc
from flask import Flask
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError

from grpc_server.utils import validate_token
from src.db.access import PermissionAccess
from src.grpc_server.stubs import auth_pb2, auth_pb2_grpc


class AuthServicer(auth_pb2_grpc.AuthServicer):

    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app
        self.permission_access = PermissionAccess()

    def GetPermissions(self, request, context):
        with self.flask_app.app_context():
            try:
                token = validate_token(request.token)
                role_ids = [role_id for role_id in token['roles'].keys()]
                permissions = self.permission_access.get_permissions_by_roles(role_ids)
                return auth_pb2.Permissions(permissions=permissions)

            except (JWTExtendedException, PyJWTError) as error:
                self.error_response(grpc.StatusCode.UNAUTHENTICATED,
                                    str(error), context)

            except Exception as error:
                self.error_response(grpc.StatusCode.ABORTED,
                                    str(error), context)

    def GetRoles(self, request, context):
        with self.flask_app.app_context():
            try:
                token = validate_token(request.token)
                roles = [role for role in token['roles'].values()]
                return auth_pb2.Roles(roles=roles)

            except (JWTExtendedException, PyJWTError) as error:
                self.error_response(grpc.StatusCode.UNAUTHENTICATED,
                                    str(error), context)

            except Exception as error:
                self.error_response(grpc.StatusCode.ABORTED,
                                    str(error), context)

    def IsAuthorized(self, request, context):
        with self.flask_app.app_context():
            try:
                validate_token(request.token)
                return auth_pb2.IsValid(is_valid=True)

            except (JWTExtendedException, PyJWTError):
                return auth_pb2.IsValid(is_valid=False)

            except Exception as error:
                self.error_response(grpc.StatusCode.ABORTED,
                                    str(error), context)

    @staticmethod
    def error_response(code, error, context):
        context.set_code(code)
        context.set_details(error)
