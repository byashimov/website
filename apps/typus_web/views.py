from difflib import SequenceMatcher

from typus import en_typus, ru_typus
from typus.utils import splinter

from flask import g, jsonify
from flask.views import MethodView

from html import escape
from website.core.views import TemplateFormView
from website.core.views.mixins import FormViewMixin

from .forms import ApiForm, ViewForm


class TypusViewMixin:
    split_phrases = staticmethod(splinter(','))
    typus = {
        'en': en_typus,
        'ru': ru_typus
    }


class FormView(TypusViewMixin, TemplateFormView):
    methods = ('GET', 'POST')
    form_class = ViewForm
    template_name = 'form_view.html'

    def form_valid(self, form):
        typus = self.typus[g.locale]
        escape_phrases = self.split_phrases(form.escape_phrases.data)

        original = form.text.data
        processed = typus(original, escape_phrases=escape_phrases)
        diff = self.mark_diff(original, processed)

        # Puts processed text back in form for easy copy&paste
        # and visual diff with sans-serif
        form.text.data = processed
        return self.response(form=form, diff=diff)

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


class ApiView(TypusViewMixin, FormViewMixin, MethodView):
    methods = ('POST', )
    form_class = ApiForm

    def response(self, **context):
        return jsonify(context)

    def form_invalid(self, form):
        return self.response(errors=form.errors)

    def form_valid(self, form):
        typus = self.typus[form.lang.data]
        escape_phrases = self.split_phrases(form.escape_phrases.data)
        text = typus(form.text.data, escape_phrases=escape_phrases)
        return self.response(text=text)
