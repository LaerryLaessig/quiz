from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AnswerForm(FlaskForm):
    answer = StringField('answer')


class NamingForm(FlaskForm):
    name = StringField('name')


class AddQuestionForm(FlaskForm):
    question = StringField('question')
    answer = StringField('answer')
