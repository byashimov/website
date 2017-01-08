from flask import Blueprint

from .views import PageView

bp = Blueprint('flatpages', __name__, 'static', template_folder='templates')
bp.add_url_rule('/', defaults={'path': 'index'},
                view_func=PageView.as_view('index'))
