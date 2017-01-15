from flask import Blueprint

from .views import ApiView, FormView

bp = Blueprint('typus_web', __name__, 'static', template_folder='templates')
bp.add_url_rule('/', view_func=FormView.as_view('form_view'))
bp.add_url_rule('/api/v1/', view_func=ApiView.as_view('api_view'))
