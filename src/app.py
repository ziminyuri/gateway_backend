from flask import Flask

from api import blueprint
from api.docs import docs
from api.v1.serializers import ma
from core.config import update_config
from db.models.database import init_db
from error_handlers import register_errors
from services.auth import init_jwt

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
