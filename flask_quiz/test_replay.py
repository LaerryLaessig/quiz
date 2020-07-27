import unittest

from flask_quiz.models import Question, Answer
from flask_quiz.replay import get_next_question_and_is_last_answer_correct

QUESTIONS = [Question(text='Question A', answer='Answer A', order_number=1),
             Question(text='Question B', answer='Answer B', order_number=2),
             Question(text='Question C', answer='Answer C', order_number=3)]


class TestReplay(unittest.TestCase):
    def test_no_answer_correct(self):
        answers = [Answer(text='Answer', user='uuid')]

        next_question, last_correct = get_next_question_and_is_last_answer_correct(QUESTIONS, answers)

        self.assertEqual(next_question, QUESTIONS[0])
        self.assertEqual(last_correct, False)

    def test_first_question_correct_last_answer_correct(self):
        answers = [Answer(text='Answer ', user='uuid'),
                   Answer(text='Answer A', user='uuid')]

        next_question, last_correct = get_next_question_and_is_last_answer_correct(QUESTIONS, answers)

        self.assertEqual(next_question, QUESTIONS[1])
        self.assertEqual(last_correct, True)

    def test_first_question_correct_last_answer_not_correct(self):
        answers = [Answer(text='Answer ', user='uuid'),
                   Answer(text='Answer A', user='uuid'),
                   Answer(text='Answer', user='uuid')]

        next_question, last_correct = get_next_question_and_is_last_answer_correct(QUESTIONS, answers)

        self.assertEqual(next_question, QUESTIONS[1])
        self.assertEqual(last_correct, False)

    def test_first_question_correct_last_answer_correct_lower_case(self):
        answers = [Answer(text='Answer ', user='uuid'),
                   Answer(text='answer a', user='uuid')]

        next_question, last_correct = get_next_question_and_is_last_answer_correct(QUESTIONS, answers)

        self.assertEqual(next_question, QUESTIONS[1])
        self.assertEqual(last_correct, True)

    def test_first_question_correct_last_answer_correct_upper_case(self):
        answers = [Answer(text='Answer ', user='uuid'),
                   Answer(text='ANSWER A', user='uuid')]

        next_question, last_correct = get_next_question_and_is_last_answer_correct(QUESTIONS, answers)

        self.assertEqual(next_question, QUESTIONS[1])
        self.assertEqual(last_correct, True)

    def test_first_question_correct_last_answer_correct_upper_case(self):
        answers = [Answer(text='Answer A', user='uuid'),
                   Answer(text='ANSWER B', user='uuid'),
                   Answer(text='answer c', user='uuid')]

        next_question, last_correct = get_next_question_and_is_last_answer_correct(QUESTIONS, answers)

        self.assertEqual(next_question, None)
        self.assertEqual(last_correct, True)


if __name__ == '__main__':
    unittest.main()
