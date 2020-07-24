from sqlalchemy import asc
from flask_quiz import db
from flask_quiz.models import Highscore, Question, Answer


def create_database():
    db.create_all()


def add_high_score(user_id, name: str):
    print('user "{}" registration with name "{}"'.format(user_id, name))
    db.session.add(Highscore(user=user_id, name=name))
    db.session.commit()


def get_all_highscores():
    return Highscore.query.order_by(asc(Highscore.completion_date_time)).all()


def add_answer_to_user(user_id, answer):
    db.session.add(Answer(user=user_id, text=answer))
    db.session.commit()


def get_answers_by_user(user_id):
    return Answer.query.filter_by(user=user_id).order_by(Answer.id.asc())


def get_all_answers():
    return Answer.query.all()


def add_question(question_text: str, answer_text: str, order_number: int):
    db.session.add(Question(text=question_text, answer=answer_text, order_number=order_number))
    db.session.commit()


def update_question(question_id: int, question_text: str, answer_text: str):
    question = Question.query.filter_by(id=question_id).first()
    question.text = question_text
    question.answer = answer_text
    db.session.commit()


def update_question_postion(question_id: int,
                            question_order_number: int,
                            other_question_id: int,
                            other_question_order_number: int):
    question = Question.query.filter_by(id=question_id).first()
    question.order = question_order_number
    other_question = Question.query.filter_by(id=other_question_id).first()
    other_question.order = other_question_order_number
    db.session.commit()


def get_all_questions():
    return Question.query.all()


def delete_question_by_id(question_id: int):
    Question.query.filter_by(id=question_id).delete()
    db.session.commit()


def delete_all_user_data():
    db.session.execute('DELETE FROM answer')
    db.session.execute('DELETE FROM highscore')
    db.session.commit()


create_database()
