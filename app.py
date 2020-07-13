#!/usr/bin/env python3
import os
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from flask import Flask, render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import asc
from waitress import serve
from wordcloud import WordCloud

from Forms import AnswerForm, NamingForm, AddQuestionForm

USER_ADMIN = os.getenv('USER_ADMIN')
PWD_ADMIN = os.getenv('PWD_ADMIN')

IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
auth = HTTPBasicAuth()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)
Bootstrap(app)


class Question(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    text = db.Column('text', db.String)
    answer = db.Column('answer', db.String)

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer


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


def do_quiz_replay_by_user(user_id):
    all_questions_iterator = iter(Question.query.all())
    user_answers = Answer.query.filter_by(user=str(user_id)).order_by(Answer.id.asc())
    next_question_to_answer = next(all_questions_iterator, None)
    is_last_answer_correct = None
    for user_answer in user_answers:
        if user_answer.text.lower() == next_question_to_answer.answer.lower():
            next_question_to_answer = next(all_questions_iterator, None)
            is_last_answer_correct = True
        else:
            is_last_answer_correct = False

    return next_question_to_answer, is_last_answer_correct


@app.route('/', methods=['GET'])
def question_page():
    user_id = uuid.uuid4() if request.args.get('id') is None else request.args.get('id')
    nxt_question, is_last_answer_correct = do_quiz_replay_by_user(user_id)
    if nxt_question is not None:
        return render_template('question_page.html',
                               question=nxt_question,
                               form=AnswerForm(),
                               id=user_id,
                               is_last_answer_correct=is_last_answer_correct)
    else:
        return render_template('naming_page.html',
                               form=NamingForm(),
                               id=user_id)


@app.route('/user/<string:user_id>/answer', methods=['POST'])
def question(user_id):
    print('user "{}" answered "{}"'.format(user_id, request.form['answer']))
    db.session.add(Answer(user=user_id, text=request.form['answer']))
    db.session.commit()
    return redirect(url_for('question_page', id=user_id))


@app.route('/user/<string:user_id>/name', methods=['POST'])
def naming_page(user_id):
    try:
        print('user "{}" registration with name "{}"'.format(user_id, request.form['name']))
        db.session.add(Highscore(user=user_id, name=request.form['name']))
        db.session.commit()
        return redirect(url_for('high_score_page'))
    except IntegrityError:
        print('user "{}" with name "{}" is registered yet'.format(user_id, request.form['name']))
        return redirect(url_for(question_page))


@app.route('/highscore')
def high_score_page():
    return render_template('highscore_page.html', users=Highscore.query.order_by(asc(Highscore.completion_date_time))
                           .all())


@auth.verify_password
def verify_password(username, password):
    if username == USER_ADMIN and password == PWD_ADMIN:
        return username


@app.route('/admin', methods=['GET'])
@auth.login_required
def admin_page():
    return render_template('admin_page.html',
                           question_form=AddQuestionForm(),
                           questions=Question.query.all(),
                           show_wordcloud=request.args.get('is_wordcloud_generated'))


@app.route('/question', methods=['POST'])
@auth.login_required
def put_question():
    db.session.add(Question(text=request.form.get('question'), answer=request.form['answer']))
    db.session.commit()
    return redirect(url_for('admin_page'))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
@auth.login_required
def delete_question(question_id):
    Question.query.filter_by(id=question_id).delete()
    db.session.commit()
    return redirect(url_for('admin_page'))


@app.route('/users/delete', methods=['POST'])
@auth.login_required
def delete_all_user_data():
    db.session.execute('DELETE FROM answer')
    db.session.execute('DELETE FROM highscore')
    db.session.commit()
    return redirect(url_for('admin_page'))


@app.route('/wordcloud', methods=['GET'])
@auth.login_required
def wordcloud_page():
    words = [a.text for a in Answer.query.all()]
    print(words)
    is_wordcloud_generated = False
    if len(words) > 0:
        try:
            wordcloud = WordCloud(width=1024, height=1024, margin=0).generate(' '.join(words))
            wordcloud.to_file('{}/wordcloud.png'.format(os.path.join(app.config['IMAGE_FOLDER'])))
            is_wordcloud_generated = True
        except ValueError:
            is_wordcloud_generated = False
    return redirect(url_for('admin_page', is_wordcloud_generated=is_wordcloud_generated))


@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('question_page'))


@app.route('/health')
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    db.create_all()
    serve(app, host='0.0.0.0', port=8000)
