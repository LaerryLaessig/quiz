from flask_quiz.database import get_question_by_id
from flask_quiz.models import Question


def order_question_by_order_number(questions: [Question]):
    return sorted(questions, key=lambda question: question.order_number)


def toggle_postion_in_order(questions: [Question], question: Question, is_new_pos_higher: bool):
    ordered_questions = sorted(questions, key=lambda question: question.order_number)

    index_question = ordered_questions.index(question)

    if is_new_pos_higher is True:
        ordered_questions.remove(question)
        ordered_questions.insert(index_question + 1, question)
    elif is_new_pos_higher is False:
        ordered_questions.remove(question)
        ordered_questions.insert(index_question - 1, question)

    return ordered_questions
