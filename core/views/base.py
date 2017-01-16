from flask_babel import lazy_gettext as _

from flask import url_for
from flask.views import MethodView

from .mixins import FormViewMixin, TemplateViewMixin


class TemplateView(TemplateViewMixin, MethodView):
    def get_context_data(self, **context):
        return super().get_context_data(widgets=self.get_widgets(), **context)

    def get_widgets(self):
        return {
            'navigation': self.get_navigation(),
        }

    def get_navigation(self):
        # Dear god :(
        return (
            (url_for('flatpages.index_view'), _('all projects')),
            (url_for('typus_web.form_view'), _('typus demo')),
            (url_for('flatpages.page_view', path='typus/api'), _('typus api')),
        )


class TemplateFormView(FormViewMixin, TemplateView):
    methods = ('GET', 'POST')

    def get(self):
        return self.response(form=self.form_class())

    def form_valid(self, form):
        return self.response(form=form)

    def form_invalid(self, form):
        return self.response(form=form)
