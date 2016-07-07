from flask import Blueprint

from .views import form_view

bp = Blueprint('typus_web', __name__, 'static', template_folder='templates')
bp.add_url_rule('/', view_func=form_view, methods=('GET', 'POST'))
