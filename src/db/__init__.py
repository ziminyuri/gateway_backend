from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                         POSTGRES_URL, POSTGRES_USER)

db = SQLAlchemy()


def init_db(app: Flask):
    db_url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
             f'{POSTGRES_URL}:{POSTGRES_HOST}/{POSTGRES_DB}'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
