from flask import Flask
from flask_restful import Api

from db import db, init_db

app = Flask(__name__)
api = Api(app)


def main():
    init_db(app)
    app.app_context().push()
    db.drop_all()
    db.create_all()
    return app


if __name__ == '__main__':
    main()
