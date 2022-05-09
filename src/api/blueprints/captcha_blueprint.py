from flask import Blueprint
from flask_restful import Api

from src.api.v1.endpoints import (CaptchaSuccessTemplateView,
                                  CaptchaTemplateView)
from src.core.config import BLUEPRINT_CAPTCHA_API

captcha_bp = Blueprint(BLUEPRINT_CAPTCHA_API, __name__)
captcha_api = Api(captcha_bp)

captcha_api.add_resource(CaptchaTemplateView, '/captcha')
captcha_api.add_resource(CaptchaSuccessTemplateView, '/captcha/success')
