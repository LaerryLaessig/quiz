from flask_quiz.database import get_all_questions
from flask_quiz.models import Question


def set_new_order(question_id: int, is_new_pos_up: bool):
    question = Question.query.filter_by(id=question_id)
    nxt_question = Question.query.filter_by(order_number=question.order_number + 1)





