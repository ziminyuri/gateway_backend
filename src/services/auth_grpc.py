import grpc
from flask import Flask
from flask_jwt_extended.exceptions import JWTExtendedException

from grpc_server.utils import validate_token
from src.db.access import PermissionAccess
from src.grpc_server.stubs import auth_pb2, auth_pb2_grpc


class AuthServicer(auth_pb2_grpc.AuthServicer):

    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app
        self.permission_access = PermissionAccess()

    def HasPermission(self, request, context):
        with self.flask_app.app_context():
            try:
                token = validate_token(request.token)
                role_ids = [role_id for role_id in token['roles'].keys()]
                permissions = self.permission_access.get_permissions_by_roles(role_ids)
                has_permission = request.permission in permissions
                return auth_pb2.IsPermitted(has_permission=has_permission)

            except JWTExtendedException as error:
                self.error_response(grpc.StatusCode.UNAUTHENTICATED,
                                    str(error).encode(), context)

            except Exception as error:
                self.error_response(grpc.StatusCode.ABORTED,
                                    str(error).encode(), context)

    def HasRole(self, request, context):
        with self.flask_app.app_context():
            try:
                token = validate_token(request.token)
                roles = [role for role in token['roles'].values()]
                has_role = request.role in roles
                return auth_pb2.RoleGranted(has_role=has_role)

            except JWTExtendedException as error:
                self.error_response(grpc.StatusCode.UNAUTHENTICATED,
                                    str(error).encode(), context)

            except Exception as error:
                self.error_response(grpc.StatusCode.ABORTED,
                                    str(error).encode(), context)

    def IsAuthorized(self, request, context):
        with self.flask_app.app_context():
            try:
                validate_token(request.token)
                return auth_pb2.IsValid(is_valid=True)

            except JWTExtendedException:
                return auth_pb2.IsValid(is_valid=False)

            except Exception as error:
                self.error_response(grpc.StatusCode.UNAUTHENTICATED,
                                    str(error).encode(), context)

    @staticmethod
    def error_response(code, error, context):
        context.set_code(code)
        context.set_details(error)
