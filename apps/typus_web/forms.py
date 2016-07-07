from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class TypusForm(Form):
    text = TextAreaField(_('Type some text here'),
                         [DataRequired(), Length(min=3, max=42000)])
    debug = BooleanField(_('Replace non-breaking space with underscore'),
                         default=False)
    escape_phrases = StringField(_('Escape phrases, comma separated'),
                                 [Length(max=200)])
