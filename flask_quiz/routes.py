import os
import uuid
from wordcloud import WordCloud
from sqlalchemy.exc import IntegrityError
from flask import render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from flask_quiz.database import add_high_score, get_all_highscores, delete_question_by_id, add_question, \
    add_answer_to_user, delete_all_user_data, get_all_questions, get_all_answers
from flask_quiz import app, USER_ADMIN, PWD_ADMIN
from flask_quiz.forms import AnswerForm, NamingForm, AddQuestionForm
from flask_quiz.image_generator import generate_wordcloud_img
from flask_quiz.replay import get_nxt_question_and_is_last_answer_correct

auth = HTTPBasicAuth()


@app.route('/', methods=['GET'])
def question_page():
    user_id = uuid.uuid4() if request.args.get('id') is None else request.args.get('id')
    nxt_question, is_last_answer_correct = get_nxt_question_and_is_last_answer_correct(str(user_id))
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
    add_answer_to_user(user_id, request.form['answer'])
    return redirect(url_for('question_page', id=user_id))


@app.route('/user/<string:user_id>/name', methods=['POST'])
def naming_page(user_id):
    try:
        add_high_score(user_id, request.form['name'])
        return redirect(url_for('high_score_page'))
    except IntegrityError:
        print('user "{}" with name "{}" is registered yet'.format(user_id, request.form['name']))
        return redirect(url_for(question_page))


@app.route('/highscore')
def high_score_page():
    return render_template('highscore_page.html', users=get_all_highscores())


@auth.verify_password
def verify_password(username, password):
    if username == USER_ADMIN and password == PWD_ADMIN:
        return username


@app.route('/admin', methods=['GET'])
@auth.login_required
def admin_page():
    return render_template('admin_page.html',
                           question_form=AddQuestionForm(),
                           questions=get_all_questions(),
                           show_wordcloud=request.args.get('is_wordcloud_generated'))


@app.route('/question', methods=['POST'])
@auth.login_required
def put_question():
    add_question(question_text=request.form.get('question'), answer_text=request.form['answer'])
    return redirect(url_for('admin_page'))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
@auth.login_required
def delete_question(question_id):
    delete_question_by_id(question_id)
    return redirect(url_for('admin_page'))


@app.route('/users/delete', methods=['POST'])
@auth.login_required
def action_delete_all_user_data():
    delete_all_user_data()
    return redirect(url_for('admin_page'))


@app.route('/wordcloud', methods=['GET'])
@auth.login_required
def wordcloud_page():
    is_wordcloud_generated = generate_wordcloud_img()
    return redirect(url_for('admin_page',
                            is_wordcloud_generated=is_wordcloud_generated))


@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('question_page'))


@app.route('/health')
def health_check():
    return {"status": "ok"}
