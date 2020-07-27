from flask_quiz.database import get_all_questions, get_answers_by_user


def get_next_question_and_is_last_answer_correct(user_id: str):
    all_questions_iterator = iter(get_all_questions())
    user_answers = get_answers_by_user(user_id)
    next_question_to_answer = next(all_questions_iterator, None)
    is_last_answer_correct = None
    for user_answer in user_answers:
        if user_answer.text.lower() == next_question_to_answer.answer.lower():
            next_question_to_answer = next(all_questions_iterator, None)
            is_last_answer_correct = True
        else:
            is_last_answer_correct = False

    return next_question_to_answer, is_last_answer_correct
