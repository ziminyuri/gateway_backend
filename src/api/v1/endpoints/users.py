from http import HTTPStatus

from flask import request
from flask_restx import Resource

from api.v1.endpoints import user_ns
from api.v1.serializers.users import UserSchema, user_model
from db.access import UserAccess
from db.models import User

user_schema = UserSchema()
user_access = UserAccess()


@user_ns.route('/registration')
class Registration(Resource):

    # todo изменить код ответа с 200 на 201, убрать отдачу пароля

    @user_ns.expect(user_model, validate=True)
    @user_ns.response(HTTPStatus.CREATED, 'User was created')
    @user_ns.marshal_with(user_model, code=HTTPStatus.CREATED)
    def post(self):
        """ Регистрация нового пользователя """
        data = request.json

        errors = user_model.validate(data)
        if errors:
            return str(errors), HTTPStatus.BAD_REQUEST

        user = user_access.create(**data)
        return user


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
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if current_user.check_password(data['password']):
            return {'message': 'Logged in as {}'.format(current_user.username)}
        else:
            return {'message': 'Wrong credentials'}
