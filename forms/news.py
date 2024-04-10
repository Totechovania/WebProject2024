from flask_wtf import FlaskForm
from wtforms import StringField, FileField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = FileField("Содержание")
    is_private = BooleanField("Не публичное")
    submit = SubmitField('Подтвердить')
