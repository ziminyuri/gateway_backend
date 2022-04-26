from flask import Flask

from src.api import blueprint
from src.api.docs import docs
from src.api.v1.serializers import ma
from src.core.config import update_config
from src.db import init_db
from src.error_handlers import register_errors
from src.services.auth import init_jwt


def main(config=None):
    flask_app = Flask(__name__)
    update_config(flask_app, config)
    init_db(flask_app)
    ma.init_app(flask_app)
    flask_app.register_blueprint(blueprint)
    docs.init_app(flask_app)
    register_errors(flask_app)
    init_jwt(flask_app)
    return flask_app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=5000, debug=True)
