from flask_recaptcha import ReCaptcha

recaptcha = ReCaptcha()


def init_captcha(app):
    recaptcha.init_app(app)
