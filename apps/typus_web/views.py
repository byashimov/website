import re
from difflib import SequenceMatcher

from typus import en_typus, ru_typus
from typus.utils import splinter

from flask import g, make_response, render_template
from flask.views import MethodView

from html import escape
from http import HTTPStatus

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
            return self.response(HTTPStatus.UNPROCESSABLE_ENTITY, form=form)

        typus = self.typus[g.locale]
        escape_phrases = self.split_phrases(form.escape_phrases.data)

        original = form.text.data
        processed = typus(original, escape_phrases=escape_phrases)
        diff = self.mark_diff(original, processed)

        # Puts processed text back in form for easy copy&paste
        # and visual diff with sans-serif
        form.text.data = processed
        return self.response(form=form, diff=diff)

    def response(self, *args, **context):
        content = render_template(self.template_name, **context)
        return make_response(content, *args)

    def mark_diff(self, before, after):
        diff = ''
        matcher = SequenceMatcher(None, before, after)
        marked = False

        for op, *x, start, stop in matcher.get_opcodes():
            hunk = escape(after[start:stop])
            if op in {'replace', 'insert'}:
                hunk = '<mark>{}</mark>'.format(hunk)
                marked = True
            diff += hunk

        if marked:
            return diff
