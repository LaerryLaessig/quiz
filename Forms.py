from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AnswerForm(FlaskForm):
    answer = StringField('answer')
    submit = SubmitField('send')


class NamingForm(FlaskForm):
    name = StringField('name')
    submit = SubmitField('send')


class AddQuestionForm(FlaskForm):
    question = StringField('question')
    answer = StringField('answer')
    save = SubmitField('save')
