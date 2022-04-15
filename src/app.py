from flask import Flask
from flask_restful import Api

from db.models.database import init_db

app = Flask(__name__)
api = Api(app)


def main():
    init_db(app)
    return app


if __name__ == '__main__':
    main()
