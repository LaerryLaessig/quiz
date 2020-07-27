from flask_quiz.database import get_all_questions, get_question_by_id, update_in_order_new_order_questions


def order_question_by_order_number():
    questions = get_all_questions()
    return sorted(questions, key=lambda question: question.order_number)


def toggle_postion_in_order(question_id: int, is_new_pos_higher: bool):
    questions = get_all_questions()
    ordered_questions = sorted(questions, key=lambda question: question.order_number)
    question = get_question_by_id(question_id)

    if question_id > 0:
        index_question = ordered_questions.index(question)

        if is_new_pos_higher is True:
            ordered_questions.remove(question)
            ordered_questions.insert(index_question + 1, question)
        elif is_new_pos_higher is False:
            ordered_questions.remove(question)
            ordered_questions.insert(index_question - 1, question)

    return ordered_questions
