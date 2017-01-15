from flask import make_response, render_template
from flask.views import MethodView

from http import HTTPStatus


class BaseFormView(MethodView):
    form_class = NotImplemented

    def post(self):
        form = self.form_class()
        if form.validate_on_submit():
            return self.form_valid(form)

        # Returns response with 422 status code
        response = self.form_invalid(form)
        response.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        return response

    def form_valid(self, form):
        raise NotImplementedError()

    def form_invalid(self, form):
        raise NotImplementedError()


class TemplateFormView(BaseFormView):
    def get(self):
        return self.response(form=self.form_class())

    def form_valid(self, form):
        return self.response(form=form)

    def form_invalid(self, form):
        return self.response(form=form)

    def response(self, **context):
        content = render_template(self.template_name, **context)
        return make_response(content)
