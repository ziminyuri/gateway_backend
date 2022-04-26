import json
from http import HTTPStatus

import pytest

from src.core.config import URL_PREFIX
from src.db import db
from src.db.access import UserAccess
from src.db.models import Role, User
from tests.testdata.role import create_role_data, initial_role_data
from tests.utils import get_headers


class TestUserRole:
    endpoint = f"{URL_PREFIX}/user/role"

    @pytest.fixture(scope='class', autouse=True)
    def initial_role(self, app, create_user):
        with app.app_context():
            user_access = UserAccess()
            role_record = Role(**initial_role_data)
            db.session.add(role_record)
            db.session.commit()
            user_access.assign_role(create_user, role_record.id)
            return str(role_record.id)

    @pytest.fixture(scope='class')
    def role_for_user(self, app):
        with app.app_context():
            role_record = Role(**create_role_data)
            db.session.add(role_record)
            db.session.commit()
            return {
                'role_id': str(role_record.id)
            }

    def test_get_all_user_roles(self, client, login_user, initial_role):
        """Тест получение всех ролей пользователя"""
        access_token, _ = login_user
        response = client.get(self.endpoint, headers=get_headers(access_token))
        data = response.json

        assert response.status_code == HTTPStatus.OK
        assert isinstance(data, list)
        assert any([role['id'] == initial_role for role in data])

    def test_create_user_role(self, app, client, login_user, role_for_user, create_user):
        """Тест присвоение пользователю новой роли"""
        access_token, _ = login_user
        response = client.post(self.endpoint,
                               data=json.dumps(role_for_user),
                               headers=get_headers(access_token))

        assert response.status_code == HTTPStatus.CREATED
        assert response.json['message'] == 'Role is assigned'

        with app.app_context():
            user = User.query.filter_by(id=str(create_user)).first()
            roles = user.roles
            assert any([str(role.id) == role_for_user['role_id']
                        for role in roles])

    def test_delete_role_from_user(self, app, client, login_user, initial_role, create_user):
        """Тест удаление роли у пользователя"""
        data = {'role_id': initial_role}
        access_token, _ = login_user
        response = client.put(self.endpoint,
                              data=json.dumps(data),
                              headers=get_headers(access_token))

        assert response.status_code == HTTPStatus.OK
        assert response.json['message'] == 'Role is removed'

        with app.app_context():
            user = User.query.filter_by(id=str(create_user)).first()
            roles = user.roles
            assert all([str(role.id) != initial_role for role in roles])
