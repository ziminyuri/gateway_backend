import pytest

from src.app import main
from src.db import db
from tests.utils import create_test_db_url


@pytest.fixture(scope='class')
def app():
    app = main({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': create_test_db_url(),
    })

    yield app

    db.drop_all()


@pytest.fixture(scope='class')
def client(app):
    return app.test_client()
