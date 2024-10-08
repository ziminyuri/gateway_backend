from flask import Flask
from flask_migrate import Migrate

from src.api.blueprints import auth_bp, captcha_bp, role_bp, user_bp
from src.api.docs import docs
from src.api.v1.serializers import ma
from src.commands import init_commands
from src.core.config import update_config
from src.db import init_db
from src.error_handlers import register_errors
from src.middleware import init_trace
from src.services.auth import init_jwt
from src.services.captcha import init_captcha
from src.services.oauth import init_oauth

migrate = Migrate()


def main(config=None):
    flask_app = Flask(__name__, template_folder='templates')
    update_config(flask_app, config)
    init_trace(flask_app)
    db = init_db(flask_app)
    migrate.init_app(flask_app, db)
    ma.init_app(flask_app)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(role_bp)
    flask_app.register_blueprint(captcha_bp)
    flask_app.register_blueprint(user_bp)
    docs.init_app(flask_app)
    register_errors(flask_app)
    init_jwt(flask_app)
    init_commands(flask_app)
    init_oauth(flask_app)
    init_captcha(flask_app)

    return flask_app


app = main()
