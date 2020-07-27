from flask_quiz.models import Answer, Question


def get_next_question_and_is_last_answer_correct(questions: [Question], answers: [Answer]):
    all_questions_iterator = iter(questions)
    user_answers = answers
    next_question_to_answer = next(all_questions_iterator, None)
    is_last_answer_correct = None
    for user_answer in user_answers:
        if user_answer.text.lower() == next_question_to_answer.answer.lower():
            next_question_to_answer = next(all_questions_iterator, None)
            is_last_answer_correct = True
        else:
            is_last_answer_correct = False

    return next_question_to_answer, is_last_answer_correct
