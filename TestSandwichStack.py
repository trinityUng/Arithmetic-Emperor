import unittest, pygame
from SandwichStack import spawn_food

class GameState:
    """
    A class to represent the state of the Sandwich Stack game.
    
    Attributes:
        score (int): The current score of the player.
        lives (int): The current number of lives the player has.
        max_score (int): The score needed to win the game.
        correct_answer (int or None): The correct answer for the current food item.
    """
    def __init__(self):
        """
        Initializes the GameState with a score of 0, 3 lives, a max score of 5, and no correct answer.
        """
        self.score = 0
        self.lives = 3
        self.max_score = 5
        self.correct_answer = None

    def update_score(self, correct):
        """
        Updates the score based on whether the player's answer is correct.
        
        Parameters:
            correct (bool): True if the player's answer is correct, False otherwise.
        """
        if correct:
            self.score += 1

    def update_lives(self, player_answer, correct_answer):
        """
        Updates the number of lives based on the player's answer compared to the correct answer.
        
        Parameters:
            player_answer (int): The answer provided by the player.
            correct_answer (int): The correct answer.
        """
        if player_answer != correct_answer:
            self.lives -= 1

    def game_over(self):
        """
        Checks whether the game is over, either by the player losing all lives or reaching the max score.
        
        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.lives <= 0 or self.score >= self.max_score
    
    def check_answer(self, player_answer):
        """
        Checks the player's answer against the correct answer, updates score or lives accordingly.
        
        Parameters:
            player_answer (int): The answer provided by the player.
            
        Returns:
            bool: True if the player's answer is correct, False otherwise.
        """
        correct = player_answer == self.correct_answer
        if correct:
            self.update_score(True)
        else:
            self.update_lives(player_answer, self.correct_answer)
        return correct

class TestSandwichStack(unittest.TestCase):
    """
    A test suite for testing the functionality of the Sandwich Stack game's non-GUI logic.
    """

    def setUp(self):
        """
        Sets up a test case environment by initializing a GameState instance.
        """
        self.game_state = GameState()

    def test_spawn_food(self):
        """
        Tests that the spawn_food function returns elements of correct types and values.
        """
        answer_bank = [10, 20, 30]
        food, food_rect, answer, text_surface, text_rect = spawn_food(answer_bank)
        self.assertIn(answer, answer_bank, "The answer should be one from the answer bank.")
        self.assertIsInstance(food_rect, pygame.Rect, "food_rect should be a tuple representing position and size.")
        self.assertIsInstance(answer, int, "The answer should be an integer.")

    def test_answer_correct(self):
        """
        Tests that the game state correctly identifies and handles a correct answer.
        """
        self.game_state.correct_answer = 42
        player_answer = 42
        result = self.game_state.check_answer(player_answer)
        self.assertTrue(result, "Answer check should return True for a correct answer.")
        self.assertEqual(self.game_state.score, 1, "Score should increment by 1 for a correct answer.")
        self.assertEqual(self.game_state.lives, 3, "Lives should not change for a correct answer.")

    def test_answer_incorrect(self):
        """
        Tests that the game state correctly identifies and handles an incorrect answer.
        """
        player_answer = 41
        result = self.game_state.check_answer(player_answer)
        self.assertFalse(result, "Answer check should return False for an incorrect answer.")
        self.assertEqual(self.game_state.score, 0, "Score should not change for an incorrect answer.")
        self.assertEqual(self.game_state.lives, 2, "Lives should decrease by 1 for an incorrect answer.")

    def test_answer_bank_randomness(self):
        """
        Tests that spawn_food selects random answers from the answer bank over multiple calls.
        """
        answer_bank = [1, 2, 3, 4, 5]
        answers_collected = set()
        # Spawn food 10 times to check randomness
        for _ in range(10):
            _, _, answer, _, _ = spawn_food(answer_bank)
            answers_collected.add(answer)
        self.assertTrue(len(answers_collected) > 1, "Multiple runs should yield different answers indicating randomness.")

    def test_update_score_correct(self):
        """
        Tests that the score is correctly updated for a correct answer.
        """
        self.game_state.update_score(True)
        self.assertEqual(self.game_state.score, 1, "Score should increment by 1 for a correct answer.")

    def test_update_score_incorrect(self):
        """
        Tests that the score is not updated for an incorrect answer.
        """
        self.game_state.update_score(False)
        self.assertEqual(self.game_state.score, 0, "Score should not change for an incorrect answer.")

    def test_update_lives_correct(self):
        """
        Tests that lives are not decreased for a correct answer.
        """
        correct_answer = 5
        self.game_state.update_lives(correct_answer, correct_answer)
        self.assertEqual(self.game_state.lives, 3, "Lives should not decrease for a correct answer.")

    def test_update_lives_incorrect(self):
        """
        Tests that lives are correctly decreased for an incorrect answer.
        """
        self.game_state.update_lives(4, 5)
        self.assertEqual(self.game_state.lives, 2, "Lives should decrease by 1 for an incorrect answer.")

    def test_game_over_by_lives(self):
        """
        Tests that the game correctly ends when the player runs out of lives.
        """
        self.game_state.lives = 0
        self.assertTrue(self.game_state.game_over(), "Game should end when lives are 0.")

    def test_game_continues(self):
        """
        Tests that the game continues under normal conditions (lives > 0 and score < max_score).
        """
        self.assertFalse(self.game_state.game_over(), "Game should continue when lives > 0 and score < max_score.")

    def test_game_over_by_score(self):
        """
        Tests that the game correctly ends when the player reaches the max score.
        """
        self.game_state.score = 5
        self.assertTrue(self.game_state.game_over(), "Game should end when score reaches the max score.")

if __name__ == "__main__":
    unittest.main()