import json

import pytest

from core.config import URL_PREFIX
from db import db
from db.access import RoleAccess
from db.models import Permission, Role
from tests.testdata.permission import create_perm_data, initial_perm_data
from tests.testdata.role import initial_role_data
from tests.utils import get_headers


class TestUserRole:
    endpoint = f"{URL_PREFIX}/permission/role"

    @pytest.fixture(scope='class', autouse=True)
    def initial_role_permission(self, app):
        with app.app_context():
            role_access = RoleAccess()
            role_record = Role(**initial_role_data)
            permission_record = Permission(**initial_perm_data)
            db.session.add(role_record)
            db.session.add(permission_record)
            db.session.commit()
            role_access.add_permission(role_record.id, permission_record.id)
            return str(role_record.id), str(permission_record.id)

    @pytest.fixture(scope='class')
    def permission_for_role(self, app, initial_role_permission):
        role_id, _ = initial_role_permission
        with app.app_context():
            permission_record = Permission(**create_perm_data)
            db.session.add(permission_record)
            db.session.commit()
            return {
                'permission_id': str(permission_record.id),
                'role_id': role_id
            }

    def test_get_all_role_permissions(self, client, login_user, initial_role_permission):
        """Тест получение всех полномочий по роли"""
        role_id, permission_id = initial_role_permission
        access_token, _ = login_user
        response = client.get(f'{self.endpoint}/{role_id}',
                              headers=get_headers(access_token))
        data = response.json

        assert response.status_code == 200
        assert isinstance(data, list)
        assert any([permission['id'] == permission_id for permission in data])

    def test_create_role_permission(self, app, client, login_user, permission_for_role):
        """Тест присвоение полномочий к роле"""
        access_token, _ = login_user
        response = client.post(self.endpoint,
                               data=json.dumps(permission_for_role),
                               headers=get_headers(access_token))

        assert response.status_code == 201
        assert response.json['message'] == 'Permission is added'

        with app.app_context():
            role = Role.query.filter_by(id=permission_for_role['role_id']).first()
            permissions = role.permissions
            assert any([str(permission.id) == permission_for_role['permission_id']
                        for permission in permissions])

    def test_delete_permission_from_role(self, app, client, login_user, initial_role_permission):
        """Тест удаление полномочий у роли"""
        role_id, permission_id = initial_role_permission
        payload = {'role_id': role_id, 'permission_id': permission_id}
        access_token, _ = login_user
        response = client.put(self.endpoint,
                              data=json.dumps(payload),
                              headers=get_headers(access_token))

        assert response.status_code == 200
        assert response.json['message'] == 'Permission is removed'

        with app.app_context():
            role = Role.query.filter_by(id=role_id).first()
            permissions = role.permissions
            assert all([str(permission.id) != permission_id for permission in permissions])
