from flask_quiz.database import get_all_questions
from flask_quiz.models import Question


def set_new_order(question_id: int, is_new_pos_up: bool):
    questions = get_all_questions()

    ordered_questions = sorted(questions, key=lambda question: question.order_number)

    for q in ordered_questions:
        print('question {} order {}'.format(q.text, q.order_number))


