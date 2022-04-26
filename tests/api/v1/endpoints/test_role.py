import json
from http import HTTPStatus

import pytest

from src.core.config import URL_PREFIX
from src.db import db
from src.db.models import Role
from tests.constants import UUID
from tests.testdata.role import (create_role_data, delete_role_data,
                                 initial_role_data, update_role_data)
from tests.utils import get_headers


class TestRole:
    endpoint = f"{URL_PREFIX}/role"

    @pytest.fixture(scope='class', autouse=True)
    def initial_role(self, app):
        with app.app_context():
            role_record = Role(**initial_role_data)
            db.session.add(role_record)
            db.session.commit()
            return role_record.id

    @pytest.fixture
    def deleted_role(self, app):
        with app.app_context():
            role_record = Role(**delete_role_data)
            db.session.add(role_record)
            db.session.commit()
            return role_record.id

    def test_get_all_roles(self, client, login_super_user, login_user, initial_role):
        """Тест получение всех ролей"""
        access_token, _ = login_super_user
        response = client.get(self.endpoint, headers=get_headers(access_token))
        data = response.json

        assert response.status_code == HTTPStatus.OK
        assert isinstance(data, list)
        assert any([role['id'] == str(initial_role) for role in data])

        # Not is superuser
        access_token, _ = login_user
        response = client.get(self.endpoint, headers=get_headers(access_token))

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_role(self, client, login_super_user, login_user):
        """Тест создание новой роли"""
        access_token, _ = login_super_user
        response = client.post(self.endpoint,
                               data=json.dumps(create_role_data),
                               headers=get_headers(access_token))
        data = response.json

        assert response.status_code == HTTPStatus.CREATED
        assert data['name'] == create_role_data['name']

        # Not is superuser
        access_token, _ = login_user
        response = client.post(self.endpoint,
                               data=json.dumps(create_role_data),
                               headers=get_headers(access_token))

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_get_role(self, client, login_super_user, login_user, initial_role):
        """Тест получение роли по uuid"""
        access_token, _ = login_super_user
        response = client.get(f'{self.endpoint}/{initial_role}', headers=get_headers(access_token))
        data = response.json

        assert response.status_code == HTTPStatus.OK
        assert data['id'] == str(initial_role)

        # Not is superuser
        invalid_access_token, _ = login_user
        response = client.get(f'{self.endpoint}/{initial_role}',
                              headers=get_headers(invalid_access_token))

        assert response.status_code == HTTPStatus.UNAUTHORIZED

        # Wrong uuid
        response = client.get(f'{self.endpoint}/{UUID}', headers=get_headers(access_token))

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert UUID in response.json['message']

    def test_update_role(self, client, login_super_user, login_user, initial_role):
        """Тест обновления роли"""
        access_token, _ = login_super_user
        response = client.put(f'{self.endpoint}/{initial_role}',
                              data=json.dumps(update_role_data),
                              headers=get_headers(access_token))
        data = response.json

        assert response.status_code == HTTPStatus.OK
        assert data['name'] == update_role_data['name']

        # Not is superuser
        invalid_access_token, _ = login_user
        response = client.put(f'{self.endpoint}/{initial_role}',
                              data=json.dumps(update_role_data),
                              headers=get_headers(invalid_access_token))

        assert response.status_code == HTTPStatus.UNAUTHORIZED

        # Wrong uuid
        response = client.put(f'{self.endpoint}/{UUID}',
                              data=json.dumps(update_role_data),
                              headers=get_headers(access_token))

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert UUID in response.json['message']

    def test_delete_role(self, client, login_super_user, login_user, deleted_role):
        """Тест удаление роли"""
        access_token, _ = login_super_user
        response = client.delete(f'{self.endpoint}/{deleted_role}',
                                 headers=get_headers(access_token))

        assert response.status_code == HTTPStatus.OK
        assert response.json['message'] == 'Role is deleted'

        # Not is superuser
        invalid_access_token, _ = login_user
        response = client.delete(f'{self.endpoint}/{deleted_role}',
                                 headers=get_headers(invalid_access_token))

        assert response.status_code == HTTPStatus.UNAUTHORIZED
