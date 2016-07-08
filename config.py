import os


class Config(object):
    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_SUPPORTED_LOCALES = {'en', 'ru'}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True


class Prod(Config):
    SECRET_KEY = os.getenv('SITE_SECRET_KEY')


class Dev(Config):
    DEBUG = True
    SECRET_KEY = 'booze'
