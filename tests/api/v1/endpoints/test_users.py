import json
from http import HTTPStatus

from src.core.config import URL_PREFIX
from src.db.access import UserAccess
from tests.testdata.user import users
from tests.utils import get_headers, get_user_agent

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

        assert user_from_db_by_id == user_access.get_by_username(test_user['username'], quiet=False)

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
        """ Авторизация пользователя с пустым username """

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

    def test_get_auth_history_success(self, client, login_user):
        """ Тестирование получения сессий авторизации c токеном в header """

        access_token, _ = login_user
        response = client.get(f'{self.route}/history', headers=get_headers(access_token))
        data = response.json
        assert len(data) == 1
        first_auth_history = data[0]
        assert first_auth_history.get('login_at') is not None
        assert first_auth_history.get('user_agent') is not None
        assert response.status_code == HTTPStatus.OK

    def test_get_auth_history_with_invalid_token(self, client, login_user):
        """ Тестирование получения сессий авторизации c неверным токеном в header """

        access_token, _ = login_user
        response = client.get(f'{self.route}/history', headers=get_headers(f'{access_token}123'))
        data = response.json
        assert len(data) == 1
        assert data.get('msg') == 'Signature verification failed'
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_get_auth_history_with_refresh_token(self, client, login_user):
        """ Тестирование получения сессий авторизации c неверным токеном в header """

        _, refresh_token = login_user
        response = client.get(f'{self.route}/history', headers=get_headers(refresh_token))
        data = response.json
        assert len(data) == 1
        assert data.get('msg') == 'Only non-refresh tokens are allowed'
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_logout_success(self, client, login_user):
        """ Успешный выход из аккаунта """
        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        data = response.json
        access_token = data['access_token']

        response = client.get(f'{self.route}/logout', headers=get_headers(access_token))
        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Logout successful'
        assert response.status_code == HTTPStatus.OK

        response = client.get(f'{self.route}/history', headers=get_headers(access_token))
        assert len(response.json) == 1
        assert response.json.get('msg') == 'Token has been revoked'
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_refresh_success(self, client, login_user):
        """ Успешное получение нового access token """

        access_token_1, refresh_token = login_user
        response = client.post(
            f'{self.route}/refresh',
            headers=get_headers(access_token_1),
            data=json.dumps({'refresh_token': refresh_token})
        )
        data = response.json
        assert len(data) == 1

        assert access_token_1 != data['access_token']
        assert response.status_code == HTTPStatus.OK

        response = client.get(f'{self.route}/history', headers=get_headers(data['access_token']))
        assert response.status_code == HTTPStatus.OK

    def test_change_password_invalid_old(self, client):
        """ Изменение пароля, введен не правильно старый пароль """

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        access_token = response.json['access_token']

        response = client.post(
            f'{self.route}/password/change',
            headers=get_headers(access_token),
            data=json.dumps({
                'old_password': f"{test_user['password']}bad",
                'new_password': f"{test_user['password']}new"
            })
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Some error with user. Wrong credentials'
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_change_password_invalid_new(self, client):
        """ Изменение пароля, введен не правильно старый пароль """

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        access_token = response.json['access_token']

        response = client.post(
            f'{self.route}/password/change',
            headers=get_headers(access_token),
            data=json.dumps({
                'old_password': test_user['password'],
                'new_password': test_user['password']
            })
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Some error with user. Passwords match'
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_change_password_success(self, client):
        """ Успешное изменение пароля """

        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        access_token = response.json['access_token']

        response = client.post(
            f'{self.route}/password/change',
            headers=get_headers(access_token),
            data=json.dumps({
                'old_password': test_user['password'],
                'new_password': f"{test_user['password']}new"
            })
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Password successfully updated.'
        assert response.status_code == HTTPStatus.OK

        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({
                'username': test_user['username'],
                'password': f"{test_user['password']}new"
            })
        )

        assert response.status_code == HTTPStatus.OK
        client.post(
            f'{self.route}/password/change',
            headers=get_headers(access_token),
            data=json.dumps({
                'old_password': f"{test_user['password']}new",
                'new_password': test_user['password']
            })
        )

    def test_change_user_data_invalid(self, client, login_user):
        """ Изменение username на занятый """
        access_token, _ = login_user
        test_user_another = users[1]

        response = client.post(
            f'{self.route}/personal_data',
            headers=get_headers(access_token),
            data=json.dumps({'username': test_user_another['username']})
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'Some error with user. Not valid username'
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_change_user_data_success(self, client):
        """ Изменение username """
        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            content_type='application/json',
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        access_token = response.json['access_token']

        response = client.post(
            f'{self.route}/personal_data',
            headers=get_headers(access_token),
            data=json.dumps({'username': f"{test_user['username']}new"})
        )
        data = response.json
        assert len(data) == 1
        assert data.get('message') == 'User successfully updated.'
        assert response.status_code == HTTPStatus.OK

        response = client.post(
            f'{self.route}/personal_data',
            headers=get_headers(access_token),
            data=json.dumps({'username': test_user['username']})
        )
        assert response.status_code == HTTPStatus.OK

    def test_change_success_logout_all_device(self, client):
        """ Успешный выход из всех аккаунтов """
        test_user = users[1]
        response = client.post(
            f'{self.route}/login',
            headers={'Content-Type': 'application/json'} | get_user_agent('Chrome/93.0.4577.82'),
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        access_token_1 = response.json['access_token']
        assert response.status_code == HTTPStatus.OK

        response = client.post(
            f'{self.route}/login',
            headers={'Content-Type': 'application/json'} | get_user_agent('Safari/537.36'),
            data=json.dumps({'username': test_user['username'], 'password': test_user['password']})
        )
        assert response.status_code == HTTPStatus.OK
        assert access_token_1 != response.json['access_token']

        response = client.get(
            f'{self.route}/logout/device/all',
            headers=get_headers(access_token_1),
            data=json.dumps({'username': test_user['username']})
        )

        assert response.json.get('message') == 'You are logged out of all devices successfully'
        assert response.status_code == HTTPStatus.OK
