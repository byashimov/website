from flask import g, render_template
from flask.views import MethodView


class PageView(MethodView):
    methods = ['GET']
    template_name = 'page.html'

    def get(self, path):
        page = g.pages.get_or_404(path)
        return render_template(self.template_name, page=page)
