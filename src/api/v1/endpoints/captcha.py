from flask import make_response, redirect, render_template, url_for
from flask_restful import Resource

from src.services.captcha import recaptcha


class CaptchaTemplateView(Resource):
    """ Тест на человека """

    @staticmethod
    def get():
        return make_response(render_template('html/captcha.html'))

    @staticmethod
    def post():
        if recaptcha.verify():
            return redirect(url_for('captcha_api.captchasuccesstemplateview'))
        else:
            return redirect(url_for('captcha_api.captchatemplateview'))


class CaptchaSuccessTemplateView(Resource):

    @staticmethod
    def get():
        return make_response(render_template('html/captcha_success.html'))
