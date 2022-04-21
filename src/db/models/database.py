from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                         POSTGRES_PORT, POSTGRES_USER)

db = SQLAlchemy()


def init_db(app: Flask):
    db_url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
             f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    app.app_context().push()
    db.create_all()
