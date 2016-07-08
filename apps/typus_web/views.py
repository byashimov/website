import re

from flask import g, make_response, render_template
from flask.views import MethodView
from typus import en_typus, ru_typus
from typus.utils import splinter

from .forms import TypusForm

phrases_delim = re.compile(r'(?<!\\),\s*')


class FormView(MethodView):
    method = ('GET', 'POST')
    form_class = TypusForm
    template_name = 'form_view.html'
    split_phrases = staticmethod(splinter(','))
    typus = {
        'en': en_typus,
        'ru': ru_typus
    }

    def get(self):
        return self.response(form=self.form_class())

    def post(self):
        form = self.form_class()
        if not form.validate_on_submit():
            return self.response(422, form=form)

        typus = self.typus[g.locale]
        escape_phrases = self.split_phrases(form.escape_phrases.data)
        form.text.data = typus(form.text.data,
                               escape_phrases=escape_phrases,
                               debug=form.debug.data)
        return self.response(form=form)

    def response(self, *args, **context):
        content = render_template(self.template_name, **context)
        return make_response(content, *args)
