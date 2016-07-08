from flask import Blueprint

from .views import FormView

bp = Blueprint('typus_web', __name__, 'static', template_folder='templates')
bp.add_url_rule('/', view_func=FormView.as_view('form_view'))
