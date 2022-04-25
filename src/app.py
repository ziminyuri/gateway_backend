from flask import Flask

from src.api import blueprint
from src.api.docs import docs
from src.api.v1.serializers import ma
from src.core.config import update_config
from src.db import init_db
from src.error_handlers import register_errors
from src.services.auth import init_jwt

app = Flask(__name__)


def main(config=None):
    update_config(app, config)
    init_db(app)
    ma.init_app(app)
    app.register_blueprint(blueprint)
    docs.init_app(app)
    register_errors(app)
    init_jwt(app)
    return app


if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=5000, debug=True)
