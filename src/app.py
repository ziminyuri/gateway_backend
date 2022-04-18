from flask import Flask
from flask_praetorian import Praetorian

from api import blueprint
from api.docs import docs
from api.v1.serializers import ma
from core.config import update_config
from db.models.database import init_db
from db.models.user import User

app = Flask(__name__)
guard = Praetorian()


def main():
    update_config(app)
    init_db(app)
    guard.init_app(app, User)
    ma.init_app(app)
    app.register_blueprint(blueprint)
    docs.init_app(app)
    return app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=5000, debug=True)
