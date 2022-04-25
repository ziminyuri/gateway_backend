import json

import pytest

from src.app import main
from src.core.config import URL_PREFIX
from src.db import db
from src.db.models import User
from tests.testdata.user import super_user
from tests.utils import create_test_db_url

user_url = f'{URL_PREFIX}/auth/login'


@pytest.fixture(scope='session')
def app():
    app = main({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': create_test_db_url(),
    })

    yield app

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='class')
def create_super_user(app):
    with app.app_context():
        user = User(**super_user)
        db.session.add(user)
        db.session.commit()


@pytest.fixture(scope='class')
def login_user(client, create_super_user):
    user = {
        "username": super_user['username'],
        "password": super_user['password']
    }
    response = client.post(user_url, data=json.dumps(user),
                           content_type='application/json')
    access_token, refresh_token = response.json.values()

    return access_token, refresh_token


@pytest.fixture(scope='class')
def client(app):
    return app.test_client()
