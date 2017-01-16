import os

from flask_babel import Babel
from flask_flatpages import FlatPages
from flask_wtf.csrf import CSRFProtect

from flask import Flask, g, request

from .apps import flatpages, typus_web

site = Flask(__name__)
site.config.from_object(os.environ['SITE_CONFIG'])
site.register_blueprint(typus_web.bp, url_prefix='/typus')
site.register_blueprint(flatpages.bp)

pages = FlatPages(site)
babel = Babel(site)
csrf = CSRFProtect(site)

# Fucking Jesus fuck! I'm not able to pass a class based view
# since it has an endpoint which is not equal to views's name!
# And I can't use a decorator because of relative fucking imports!
# See the form, it has to exempt csrf too.
# Who the hell had invented this?
csrf.exempt('website.apps.typus_web.views.api_view')


@babel.localeselector
def get_locale():
    supported_locals = site.config['BABEL_SUPPORTED_LOCALES']
    lang = request.args.get('lang')
    if lang and lang in supported_locals:
        return lang

    fallback = site.config['BABEL_DEFAULT_LOCALE']
    return request.accept_languages.best_match(supported_locals) or fallback


@site.before_request
def before_request():
    g.pages = pages
    g.locale = get_locale()
