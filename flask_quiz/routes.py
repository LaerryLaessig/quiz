import os
import uuid
from sqlalchemy.exc import IntegrityError
from flask import render_template, request, redirect, url_for, send_file, send_from_directory
from flask_httpauth import HTTPBasicAuth
from flask_quiz.database import add_high_score, get_all_highscores, delete_question_by_id, add_question, \
    add_answer_to_user, delete_all_user_data, get_all_questions, update_question, update_in_order_new_order_questions, \
    get_question_by_id, get_answers_by_user
from flask_quiz import app, USER_ADMIN, PWD_ADMIN
from flask_quiz.forms import AnswerForm, NamingForm, AddQuestionForm
from flask_quiz.order import toggle_postion_in_order, sort_question_by_order_number
from flask_quiz.replay import get_next_question_and_is_last_answer_correct

auth = HTTPBasicAuth()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def question_page():
    user_id = uuid.uuid4() if request.args.get('id') is None else request.args.get('id')
    nxt_question, is_last_answer_correct = get_next_question_and_is_last_answer_correct(get_all_questions(),
                                                                                        get_answers_by_user(str(user_id)))
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
    answer = request.form['answer'].strip()
    print('user "{}" answered "{}"'.format(user_id, answer))
    add_answer_to_user(user_id, answer)
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
    questions = get_all_questions()
    return render_template('admin_page.html',
                           question_form=AddQuestionForm(),
                           questions=get_all_questions(),
                           active_tab='question' if request.args.get('active_tab') is None
                           else request.args.get('active_tab'),
                           last_order_number=len(questions))


@app.route('/question', methods=['POST'])
@auth.login_required
def put_question():
    add_question(question_text=request.form.get('question'),
                 answer_text=request.form['answer'],
                 order_number=get_nxt_question_order_number())
    return redirect(url_for('admin_page',
                            active_tab='question'))


@app.route('/question/<int:question_id>', methods=['POST'])
@auth.login_required
def edit_question(question_id=0):
    update_question(question_id, request.form['question'], request.form['answer'])
    return redirect(url_for('admin_page',
                            active_tab='question') + '#question_{}'.format(question_id))


@app.route('/question/<int:question_id>/up', methods=['POST'])
@auth.login_required
def move_up_question(question_id=0):
    update_in_order_new_order_questions(toggle_postion_in_order(get_all_questions(),
                                                                get_question_by_id(question_id),
                                                                False))
    return redirect(url_for('admin_page',
                            active_tab='question') + '#question_{}'.format(question_id))


@app.route('/question/<int:question_id>/down', methods=['POST'])
@auth.login_required
def move_down_question(question_id=0):
    update_in_order_new_order_questions(toggle_postion_in_order(get_all_questions(),
                                                                get_question_by_id(question_id),
                                                                True))
    return redirect(url_for('admin_page',
                            active_tab='question') + '#question_{}'.format(question_id))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
@auth.login_required
def delete_question(question_id=0):
    delete_question_by_id(question_id)
    update_in_order_new_order_questions(sort_question_by_order_number(get_all_questions()))
    return redirect(url_for('admin_page',
                            active_tab='question') + '#question_{}'.format(question_id - 1))


@app.route('/users/delete', methods=['POST'])
@auth.login_required
def action_delete_all_user_data():
    delete_all_user_data()
    return redirect(url_for('admin_page',
                            active_tab='userdata'))


@app.route('/charts', methods=['GET'])
@auth.login_required
def charts_page():
    return redirect(url_for('admin_page',
                            active_tab='charts'))


@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('question_page'))


@app.route('/health')
def health_check():
    return {"status": "ok"}


def get_nxt_question_order_number():
    return len(get_all_questions()) + 1
