from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import Resource

from api.v1.endpoints import user_ns
from api.v1.serializers.users import auth_model, user_model
from db.access import UserAccess
from db.models import User

user_access = UserAccess()


@user_ns.route('/registration')
class Registration(Resource):

    @user_ns.expect(auth_model, validate=True)
    @user_ns.marshal_with(user_model, code=HTTPStatus.CREATED)
    def post(self):
        """ Регистрация нового пользователя """
        data = request.json

        user = user_access.create(**data)
        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])

        return {
            'id': user.id,
            'username': user.username,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, HTTPStatus.CREATED


@user_ns.route('/login')
class Login(Resource):
    def post(self):
        """ Авторизация пользователя """

        data = request.json

        errors = user_model.validate(data)
        if errors:
            return str(errors), HTTPStatus.BAD_REQUEST

        current_user = User.get_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, \
                   HTTPStatus.NOT_FOUND

        if current_user.check_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, HTTPStatus.OK
        else:
            return {'message': 'Wrong credentials'}
