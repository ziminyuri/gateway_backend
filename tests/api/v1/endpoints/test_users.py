import json
from http import HTTPStatus

from src.core.config import URL_PREFIX
from src.db.access import UserAccess
from tests.testdata.user import users

user_access = UserAccess()


class TestUsers:
    route = f'{URL_PREFIX}/auth'

    def test_register_user_success(self, client):
        """ Успешная регистрация пользователя """

        test_user = users[0]
        response = client.post(
            f'{self.route}/registration',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        data = response.json
        assert len(data) == 2
        assert data.get('username') == test_user['username']
        assert data.get('id') is not None
        assert response.status_code == HTTPStatus.CREATED

        user_from_db_by_id = user_access.get_by_id(data.get('id'))
        assert user_from_db_by_id.is_superuser == test_user['is_superuser']
        assert user_from_db_by_id.username == data.get('username')

        assert user_from_db_by_id == user_access.get_by_username(test_user['username'])

    def test_register_user_without_password(self, client):
        """ Регистрация пользователя без поля password """

        test_user = users[0]
        response = client.post(
            f'{self.route}/registration',
            content_type='application/json',
            data=json.dumps({'username': test_user['username']})
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == {'password': ['Missing data for required field.']}
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_register_user_without_username(self, client):
        """ Регистрация пользователя без поля username """

        test_user = users[0]
        response = client.post(
            f'{self.route}/registration',
            content_type='application/json',
            data=json.dumps({'password': test_user['password']})
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == {'username': ['Missing data for required field.']}
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_register_user_with_extra_field(self, client):
        """ Регистрация пользователя с дополнительным полем """

        test_user = users[0]
        response = client.post(
            f'{self.route}/registration',
            content_type='application/json',
            data=json.dumps({
                'username': test_user['username'],
                'password': test_user['password'],
                'extra': 'extra'})
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == {'extra': ['Unknown field.']}
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_register_user_with_user_username(self, client):
        """ Регистрация пользователя с занятым username """

        test_user = users[1]
        response = client.post(
            f'{self.route}/registration',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )

        data = response.json
        assert len(data) == 2
        assert data.get('username') == test_user['username']
        assert data.get('id') is not None
        assert response.status_code == HTTPStatus.CREATED

        response = client.post(
            f'{self.route}/registration',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )

        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Some error with user. Not valid username'
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_auth_user_success(self, client):
        """ Успешная авторизация пользователя """

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )

        data = response.json
        assert len(data) == 2
        assert data.get('access_token') is not None
        assert data.get('refresh_token') is not None
        assert response.status_code == HTTPStatus.OK

    def test_auth_user_without_username(self, client):
        """ Авторизация пользователя без username"""

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'password': test_user['password']})
        )

        data = response.json

        assert len(data) == 1
        assert data.get('message') == {'username': ['Missing data for required field.']}
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_auth_user_with_empty_username(self, client):
        """ Авторизация пользователя с пустым username"""

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'password': test_user['password']})
        )

        data = response.json

        assert len(data) == 1
        assert data.get('message') == {'username': ['Missing data for required field.']}
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_auth_user_without_password(self, client):
        """ Авторизация пользователя без пароля """

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username']})
        )

        data = response.json
        assert len(data) == 1
        assert data.get('message') == {'password': ['Missing data for required field.']}
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_auth_user_with_wrong_password(self, client):
        """ Авторизация пользователя c неправильным паролем """

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({
                'username': test_user['username'],
                'password': f"{test_user['password']}123"
            })
        )

        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Some error with user. Wrong credentials'
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_auth_user_with_empty_password(self, client):
        """ Авторизация пользователя c пустым паролем """

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': ''})
        )

        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Some error with user. Wrong credentials'
        assert response.status_code == HTTPStatus.BAD_REQUEST
