import os

from flask_quiz import app
from flask_quiz.models import Answer, Question


def generate_wordcloud_img(answers: [Answer]):
    words = [a.text for a in answers]
    print(words)
    is_wordcloud_generated = False
    if len(words) > 0:
        try:
            is_wordcloud_generated = True
        except ValueError:
            is_wordcloud_generated = False
    return is_wordcloud_generated


def generate_chart_most_false_answered_questions(questions: [Question], answers: [Answer]):
    user_ids = {answer.user: answer for answer in answers}

