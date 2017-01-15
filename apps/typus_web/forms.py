from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class ViewForm(FlaskForm):
    text = TextAreaField(_('Type some text here'),
                         [DataRequired(), Length(min=3, max=42000)])
    escape_phrases = StringField(_('Escape phrases, comma separated'),
                                 [Length(max=200)])


class ApiForm(ViewForm):
    lang = SelectField(choices=[('en', 'en'), ('ru', 'ru')], default='en')

    class Meta(ViewForm.Meta):
        csrf = False
