import re

from flask import g, render_template
from typus import en_typus, ru_typus

from .forms import TypusForm

phrases_delim = re.compile(r'(?<!\\),\s*')
typus_choices = {
    'en': en_typus,
    'ru': ru_typus
}


def form_view():
    form = TypusForm()
    if form.validate_on_submit():
        text = form.text.data
        debug = form.debug.data
        escape_phrases = phrases_delim.split(form.escape_phrases.data)
        typus = typus_choices[g.locale]
        form.text.data = typus(text, debug=debug,
                               escape_phrases=escape_phrases)
    return render_template('form_view.html', form=form)
