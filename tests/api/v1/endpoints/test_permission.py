import json

import pytest

from core.config import URL_PREFIX
from db import db
from db.models import Permission
from tests.constants import UUID
from tests.testdata.permission import (create_perm_data, delete_perm_data,
                                       initial_perm_data, update_perm_data)
from tests.utils import get_headers


class TestPermission:
    endpoint = f"{URL_PREFIX}/permission"

    @pytest.fixture(scope='class', autouse=True)
    def initial_permission(self, app):
        with app.app_context():
            role_record = Permission(**initial_perm_data)
            db.session.add(role_record)
            db.session.commit()
            return role_record.id

    @pytest.fixture
    def deleted_permission(self, app):
        with app.app_context():
            role_record = Permission(**delete_perm_data)
            db.session.add(role_record)
            db.session.commit()
            return role_record.id

    def test_get_all_permissions(self, client, login_super_user, login_user, initial_permission):
        """Тест получение всех полномочий"""
        access_token, _ = login_super_user
        response = client.get(self.endpoint, headers=get_headers(access_token))
        data = response.json

        assert response.status_code == 200
        assert isinstance(data, list)
        assert any([permission['id'] == str(initial_permission) for permission in data])

        # Not is superuser
        access_token, _ = login_user
        response = client.get(self.endpoint, headers=get_headers(access_token))

        assert response.status_code == 401

    def test_create_permission(self, client, login_super_user, login_user):
        """Тест создание новой роли"""
        access_token, _ = login_super_user
        response = client.post(self.endpoint,
                               data=json.dumps(create_perm_data),
                               headers=get_headers(access_token))
        data = response.json

        assert response.status_code == 201
        assert data['name'] == create_perm_data['name']

        # Not is superuser
        access_token, _ = login_user
        response = client.post(self.endpoint,
                               data=json.dumps(create_perm_data),
                               headers=get_headers(access_token))

        assert response.status_code == 401

    def test_get_permission(self, client, login_super_user, login_user, initial_permission):
        """Тест получение роли по uuid"""
        access_token, _ = login_super_user
        response = client.get(f'{self.endpoint}/{initial_permission}',
                              headers=get_headers(access_token))
        data = response.json

        assert response.status_code == 200
        assert data['id'] == str(initial_permission)

        # Not is superuser
        invalid_access_token, _ = login_user
        response = client.get(f'{self.endpoint}/{initial_permission}',
                              headers=get_headers(invalid_access_token))

        assert response.status_code == 401

        # Wrong uuid
        response = client.get(f'{self.endpoint}/{UUID}', headers=get_headers(access_token))

        assert response.status_code == 400
        assert UUID in response.json['message']

    def test_update_permission(self, client, login_super_user, login_user, initial_permission):
        """Тест обновления роли"""
        access_token, _ = login_super_user
        response = client.put(f'{self.endpoint}/{initial_permission}',
                              data=json.dumps(update_perm_data),
                              headers=get_headers(access_token))
        data = response.json

        assert response.status_code == 200
        assert data['name'] == update_perm_data['name']

        # Not is superuser
        invalid_access_token, _ = login_user
        response = client.put(f'{self.endpoint}/{initial_permission}',
                              data=json.dumps(update_perm_data),
                              headers=get_headers(invalid_access_token))

        assert response.status_code == 401

        # Wrong uuid
        response = client.put(f'{self.endpoint}/{UUID}',
                              data=json.dumps(update_perm_data),
                              headers=get_headers(access_token))

        assert response.status_code == 400
        assert UUID in response.json['message']

    def test_delete_permission(self, client, login_super_user, login_user, deleted_permission):
        """Тест удаление роли"""
        access_token, _ = login_super_user
        response = client.delete(f'{self.endpoint}/{deleted_permission}',
                                 headers=get_headers(access_token))

        assert response.status_code == 200
        assert response.json['message'] == 'Permission is deleted'

        # Not is superuser
        invalid_access_token, _ = login_user
        response = client.delete(f'{self.endpoint}/{deleted_permission}',
                                 headers=get_headers(invalid_access_token))

        assert response.status_code == 401
