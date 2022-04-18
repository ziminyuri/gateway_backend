from flask import Flask
from flask_praetorian import Praetorian

from api import blueprint
from api.v1.serializers import ma
from core.config import JWT_ACCESS_LIFESPAN, SECRET_KEY
from db.models.database import init_db
from db.models.user import User

app = Flask(__name__)
guard = Praetorian()


def main():
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["JWT_ACCESS_LIFESPAN"] = JWT_ACCESS_LIFESPAN
    app.config["PROPAGATE_EXCEPTIONS"] = False
    init_db(app)
    guard.init_app(app, User)
    ma.init_app(app)
    app.register_blueprint(blueprint)
    return app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=5000, debug=True)
