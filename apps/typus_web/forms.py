from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class TypusForm(FlaskForm):
    text = TextAreaField(_('Type some text here'),
                         [DataRequired(), Length(min=3, max=42000)])
    escape_phrases = StringField(_('Escape phrases, comma separated'),
                                 [Length(max=200)])
