from flask import g

from website.core.views import TemplateView


class PageView(TemplateView):
    template_name = 'page.html'

    def get(self, path):
        page = g.pages.get_or_404(path)
        return self.response(page=page)
