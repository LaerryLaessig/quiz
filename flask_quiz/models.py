from datetime import datetime
from flask_quiz.database import db


class Question(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    order_number = db.Column('order_number', db.Integer)
    text = db.Column('text', db.String)
    answer = db.Column('answer', db.String)

    def __init__(self, text, answer, order_number):
        self.text = text
        self.answer = answer
        self.order_number = order_number


class Answer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column('user', db.String)
    text = db.Column('text', db.String)

    def __init__(self, user, text):
        self.user = user
        self.text = text


class Highscore(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column('user_id', db.String, unique=True)
    name = db.Column('username', db.String)
    completion_date_time = db.Column(db.DateTime, nullable=False,
                                     default=datetime.utcnow)
