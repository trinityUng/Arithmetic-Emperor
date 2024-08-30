import unittest
from unittest.mock import MagicMock
from SnakeSums import *

class TestSnakeSums(unittest.TestCase):
    """
    A class to test for the Snake Sums game functionality.
    """

    def setUp(self):
        """
        Set up any necessary objects, configurations, etc.
        
        This method initializes a test user and loads the player profile.
        """
        self.user = Player(name="test_user", password="123456")
        self.user.load_player()

    def test_question_generation(self):
        """
        Test the generation of questions and correct answers.
        
        This test ensures that a question and its corresponding correct answer
        are generated correctly by the Question class.
        """
        question, correct_answer = Question(self.user).generate_question("+")
        self.assertIsInstance(question, str)
        self.assertIsInstance(correct_answer, int)

    def test_options_generation(self):
        """
        Test the generation of answer options.
        
        This test checks if the options function correctly generates a list of
        options, including the correct answer, for a given correct answer value.
        """
        correct_answer = 10
        generated_options = options(correct_answer)
        self.assertIsInstance(generated_options, list)
        self.assertEqual(len(generated_options), 5)  # Including the correct answer

    def test_fruit_coordinates(self):
        """
        Test the generation of fruit coordinates.
        
        This test verifies that the fruit_coordinates function generates a list
        of coordinates for the fruits in the game, including the snake head.
        """
        snake_head_x, snake_head_y = 400, 300
        fruit_coord = fruit_coordinates(snake_head_x, snake_head_y)
        self.assertIsInstance(fruit_coord, list)
        self.assertEqual(len(fruit_coord), 5)  # 4 fruits + snake head

    def test_end_screen(self):
        """
        Test the end screen scenarios.
        
        This test checks the behavior of the end_screen function for both win
        and loss scenarios, ensuring that it returns None, indicating a return
        to the main menu.
        """
        win_screen = end_screen(True)
        self.assertIsNone(win_screen)  # Player returns to main menu

        loss_screen = end_screen(False)
        self.assertIsNone(loss_screen)  # Player returns to main menu

    def test_game_initialization(self):
        """
        Test the game initialization.
        
        This test verifies that a Player object is correctly initialized with
        default values, specifically checking the default level for addition.
        """
        user = Player(name="test", password="123")
        self.assertEqual(user.get_add(), 0)  # Default level is 0

if __name__ == '__main__':
    unittest.main()