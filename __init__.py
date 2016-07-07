import os

from flask import Flask, g, request
from flask_babel import Babel

from .apps import typus_web

site = Flask(__name__)
site.config.from_object(os.environ['SITE_CONFIG'])
site.register_blueprint(typus_web.bp, url_prefix='/typus')
babel = Babel(site)


@babel.localeselector
def get_locale():
    supported_locals = site.config['BABEL_SUPPORTED_LOCALES']
    lang = request.args.get('lang')
    if lang and lang in supported_locals:
        return lang
    return request.accept_languages.best_match(supported_locals)


@site.before_request
def before_request():
    g.locale = get_locale()
