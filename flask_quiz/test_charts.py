import unittest
from flask_quiz.charts import generate_chart_most_false_answered_questions
from flask_quiz.models import Answer, Question


class TestCharts(unittest.TestCase):
    def test_something(self):
        answers = [Answer(user='user_id1', text='A'),
                   Answer(user='user_id2', text='B'),
                   Answer(user='user_id1', text='C')]

        questions = [Question(text='', answer='', order_number=1)]

        generate_chart_most_false_answered_questions(questions, answers)


if __name__ == '__main__':
    unittest.main()
