from flask_quiz.models import Question


def sort_question_by_order_number(questions: [Question]):
    return sorted(questions, key=lambda question: question.order_number)


def toggle_postion_in_order(questions: [Question], question_to_toggle: Question, is_new_pos_higher: bool):
    ordered_questions = sorted(questions, key=lambda question: question.order_number)

    index_question = ordered_questions.index(question_to_toggle)

    if is_new_pos_higher is True and index_question < len(ordered_questions):
        ordered_questions.remove(question_to_toggle)
        ordered_questions.insert(index_question + 1, question_to_toggle)
    elif is_new_pos_higher is False and index_question > 0:
        ordered_questions.remove(question_to_toggle)
        ordered_questions.insert(index_question - 1, question_to_toggle)

    return ordered_questions
