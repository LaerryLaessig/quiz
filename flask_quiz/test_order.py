import unittest

from flask_quiz.models import Question
from flask_quiz.order import sort_question_by_order_number, toggle_postion_in_order

FIRST_QUESTION = Question(text='FIRST_QUESTION', answer='FIRST_QUESTION', order_number=1)
SECOND_QUESTION = Question(text='SECOND_QUESTION', answer='SECOND_QUESTION', order_number=2)
QUESTION_TO_TOGGLE = Question(text='QUESTION_TO_TOGGLE', answer='QUESTION_TO_TOGGLE', order_number=3)
LAST_QUESTION = Question(text='LAST_QUESTION', answer='LAST_QUESTION', order_number=4)


class TestOrder(unittest.TestCase):

    def test_sort_by_order_number(self):
        questions = list()
        questions.append(SECOND_QUESTION)
        questions.append(LAST_QUESTION)
        questions.append(FIRST_QUESTION)
        questions.append(QUESTION_TO_TOGGLE)

        sorted_questions = sort_question_by_order_number(questions)

        self.assertEqual(sorted_questions[0], FIRST_QUESTION)
        self.assertEqual(sorted_questions[1], SECOND_QUESTION)
        self.assertEqual(sorted_questions[2], QUESTION_TO_TOGGLE)
        self.assertEqual(sorted_questions[3], LAST_QUESTION)

    def test_toggle_postion_in_order_higher_order_number(self):
        questions = list()
        questions.append(FIRST_QUESTION)
        questions.append(SECOND_QUESTION)
        questions.append(QUESTION_TO_TOGGLE)
        questions.append(LAST_QUESTION)

        sorted_questions = toggle_postion_in_order(questions, QUESTION_TO_TOGGLE, is_new_pos_higher=True)

        self.assertEqual(sorted_questions[0], FIRST_QUESTION)
        self.assertEqual(sorted_questions[1], SECOND_QUESTION)
        self.assertEqual(sorted_questions[2], LAST_QUESTION)
        self.assertEqual(sorted_questions[3], QUESTION_TO_TOGGLE)

    def test_toggle_postion_in_order_lower_order_number(self):
        questions = list()
        questions.append(FIRST_QUESTION)
        questions.append(SECOND_QUESTION)
        questions.append(QUESTION_TO_TOGGLE)
        questions.append(LAST_QUESTION)

        sorted_questions = toggle_postion_in_order(questions, QUESTION_TO_TOGGLE, is_new_pos_higher=False)

        self.assertEqual(sorted_questions[0], FIRST_QUESTION)
        self.assertEqual(sorted_questions[1], QUESTION_TO_TOGGLE)
        self.assertEqual(sorted_questions[2], SECOND_QUESTION)
        self.assertEqual(sorted_questions[3], LAST_QUESTION)

    def test_toggle_postion_in_order_first_question_dont_move(self):
        questions = list()
        questions.append(FIRST_QUESTION)
        questions.append(SECOND_QUESTION)
        questions.append(QUESTION_TO_TOGGLE)
        questions.append(LAST_QUESTION)

        sorted_questions = toggle_postion_in_order(questions, FIRST_QUESTION, is_new_pos_higher=False)

        self.assertEqual(sorted_questions[0], FIRST_QUESTION)
        self.assertEqual(sorted_questions[1], SECOND_QUESTION)
        self.assertEqual(sorted_questions[2], QUESTION_TO_TOGGLE)
        self.assertEqual(sorted_questions[3], LAST_QUESTION)

    def test_toggle_postion_in_order_last_question_dont_move(self):
        questions = list()
        questions.append(FIRST_QUESTION)
        questions.append(SECOND_QUESTION)
        questions.append(QUESTION_TO_TOGGLE)
        questions.append(LAST_QUESTION)

        sorted_questions = toggle_postion_in_order(questions, LAST_QUESTION, is_new_pos_higher=True)

        self.assertEqual(sorted_questions[0], FIRST_QUESTION)
        self.assertEqual(sorted_questions[1], SECOND_QUESTION)
        self.assertEqual(sorted_questions[2], QUESTION_TO_TOGGLE)
        self.assertEqual(sorted_questions[3], LAST_QUESTION)


if __name__ == '__main__':
    unittest.main()
