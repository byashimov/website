import os


class Config(object):
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_SUPPORTED_LOCALES = ('en', 'ru')
    SESSION_COOKIE_HTTPONLY = True
    FLATPAGES_ROOT = 'apps/flatpages/pages'
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_MARKDOWN_EXTENSIONS = (
        'codehilite',
        'def_list'  ,
        'headerid'  ,
        'smarty'    , 
    )


class Prod(Config):
    SECRET_KEY = os.getenv('SITE_SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = 'byashimov.com'


class Dev(Config):
    DEBUG = True
    SECRET_KEY = 'booze'


class Testing(Dev):
    TESTING = True
    SERVER_NAME = 'localhost'
    WTF_CSRF_ENABLED = False
