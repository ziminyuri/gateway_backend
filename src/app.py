from flask import Flask
from flask_migrate import Migrate

from src.api.blueprints import auth_bp, role_bp
from src.api.docs import docs
from src.api.v1.serializers import ma
from src.core.config import update_config
from src.db import init_db
from src.error_handlers import register_errors
from src.services.auth import init_jwt
from src.commands import init_commands
from src.utils import pagination_init


migrate = Migrate()


def main(config=None):
    flask_app = Flask(__name__)
    update_config(flask_app, config)
    db = init_db(flask_app)
    migrate.init_app(flask_app, db)
    ma.init_app(flask_app)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(role_bp)
    docs.init_app(flask_app)
    register_errors(flask_app)
    init_jwt(flask_app)
    init_commands(flask_app)
    pagination_init(flask_app, db)
    return flask_app


app = main()
