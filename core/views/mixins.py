from flask import make_response, render_template
from http import HTTPStatus


class FormViewMixin:
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


class TemplateViewMixin:
    methods = ('GET', )

    def get(self):
        return self.response()

    def response(self, **context):
        context_data = self.get_context_data(**context)
        content = render_template(self.template_name, **context_data)
        return make_response(content)

    def get_context_data(self, **context):
        return context


