import os


class Config(object):
    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_SUPPORTED_LOCALES = {'en', 'ru'}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True


class Prod(Config):
    SECRET_KEY = os.getenv('SITE_SECRET_KEY')


class Dev(Config):
    # Boo! Do what ever you want, unit FLASK_DEBUG=1 is not exported
    # it's DEBUG=False for CLI
    # https://github.com/pallets/flask/blob/master/flask/cli.py#L403
    DEBUG = True
    SECRET_KEY = 'booze'
