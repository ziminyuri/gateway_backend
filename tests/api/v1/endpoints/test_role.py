import pytest

from src.core.config import URL_PREFIX
from src.db import db
from src.db.models import Role
from tests.testdata.role import role
from tests.utils import get_headers


class TestRole:
    endpoint = f"{URL_PREFIX}/role"

    @pytest.fixture(scope='class', autouse=True)
    def initial(self, app):
        with app.app_context():
            role_record = Role(**role)
            db.session.add(role_record)
            db.session.commit()

    def test_get_all_roles(self, client, login_user):
        access_token, _ = login_user
        response = client.get(self.endpoint, headers=get_headers(access_token))
        data = response.json

        assert len(data) == 1
        assert data[0]['name'] == role['name']
