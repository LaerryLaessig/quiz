from flask_quiz.database import get_all_answers


def generate_chart_projection():
    all_answers = get_all_answers()
    answers_per_user = {}

    for answer in all_answers:
        if answer.user in answers_per_user:
            answers_per_user[answer.user].append({'id': answer.id, 'answer': answer.text})
        else:
            answers_per_user[answer.user] = [{'id': answer.id, 'answer': answer.text}]

    for a in answers_per_user:
        print('{}: {}'.format(a, answers_per_user[a]))
    return None