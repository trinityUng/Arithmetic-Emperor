import unittest
from unittest.mock import MagicMock

from Player import Player
from Question import Question

class TestQuestion(unittest.TestCase):
    """
    Unit tests for the Question class.
    """
    def setUp(self):
        """
        Set up the test environment by creating a Player and a Question instance.
        """
        self.player = Player("test_name", "test_password")
        self.question = Question(self.player)

    def test_generate_question_addition_low_level(self):
        """
        Test the generation of a low-level addition question.
        """
        self.player.get_add = MagicMock(return_value=2)
        question, answer = self.question.generate_question('+')
        num1, num2 = map(int, question[:-3].split(' + '))
        self.assertTrue(1 <= num1 <= 9)
        self.assertTrue(1 <= num2 <= 9)
        self.assertEqual(answer, num1 + num2)

    def test_generate_question_subtraction_high_level(self):
        """
        Test the generation of a high-level subtraction question.
        """
        self.player.get_sub = MagicMock(return_value=11)
        question, answer = self.question.generate_question('-')
        num1, num2 = map(int, question[:-3].split(' - '))
        self.assertTrue(1 <= num1 <= 50)
        self.assertTrue(1 <= num2 <= 50)
        self.assertEqual(answer, num1 - num2)

    def test_generate_question_multiplication_middle_level(self):
        """
        Test the generation of a middle-level multiplication question.
        """
        self.player.get_mul = MagicMock(return_value=15)
        nums = self.question.generate_question('*')
        self.assertTrue(2 <= nums[0] <= 15)
        self.assertTrue(2 <= nums[1] <= 15)

    def test_generate_question_division_low_level(self):
        """
        Test the generation of a low-level division question.
        """
        self.player.get_div = MagicMock(return_value=5)
        answer, question = self.question.generate_question('/')
        num1 = int(question.split('/')[1][:-1])
        self.assertTrue(1 <= num1 <= 2)
        self.assertTrue(answer == int(answer))  # Check if the answer is an integer

    def test_generate_question_arithmetic_emperor_middle_level(self):
        """
        Test the generation of a middle-level arithmetic emperor question.
        """
        self.player.get_bosses = MagicMock(return_value=15)
        expression, result = self.question.generate_question('emperor')
        self.assertTrue(isinstance(eval(expression), (int, float)))
        self.assertEqual(result, eval(expression))

    def test_generate_question_subtraction_high_level(self):
        """ 
        Test the generation of a high-level subtraction question.
        """
        self.player.get_sub = MagicMock(return_value=11)
        question, answer = self.question.generate_question('-')
        # Remove the '?' character before splitting
        num1, num2 = map(int, question[:-1].split(' - '))
        self.assertTrue(1 <= num1 <= 50)
        self.assertTrue(1 <= num2 <= 50)
        self.assertEqual(answer, num1 - num2)

    def test_generate_question_subtraction_low_level(self):
        """
        Test the generation of a low-level subtraction question.
        """
        self.player.get_sub = MagicMock(return_value=3)
        question, answer = self.question.generate_question('-')
        # Remove the '?' character before splitting
        num1, num2 = map(int, question[:-1].split(' - '))
        self.assertTrue(1 <= num1 <= 9)
        self.assertTrue(1 <= num2 <= 9)
        self.assertEqual(answer, num1 - num2)

if __name__ == '__main__':
    unittest.main()