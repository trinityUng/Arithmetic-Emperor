import unittest
import random
from unittest.mock import patch
from ArithmeticEmperor import attack_emperor, attack_player, check_answer, start_game

"""
A test suite for testing the functionality of the Sandwich Stack game's non-GUI logic.
"""
class TestArithmeticEmperor(unittest.TestCase):

    def setUp(self):
        """
        Sets up the initial conditions for testing.
        """
        # Set up initial health and other parameters
        self.player_attack = 30
        self.player_health = 100
        self.emperor_health = 100
        self.emperor_attack_power = 30

        self.attack_frames = []
        self.attack_type = [0, 1, 2, 3]
        self.emperor_rotation = [0, 1, 2, 3]
        self.position = (0, 0)
        self.attacker = 1 
        self.attack_type_text = ""
        self.attacked_emperor = False  # Assuming the player didn't attack the emperor initially

    def test_normal_attack_emperor(self):
        """
        Tests if attack_emperor properly deals normal or super effective damage amount based on player attack type and emperor type.
        """
        valid = True
        for attack in self.attack_type:
            for rotation in self.emperor_rotation:
                if (attack == rotation - 1 or attack - 3 == rotation ):
                    if (not(self.emperor_health - (1.5 * self.player_attack)== attack_emperor(self.player_attack, self.attack_frames, self.position, self.attacker, self.attack_type_text, self.emperor_health, self.player_health, attack, rotation))):
                        valid = False
                else:
                    if (not(self.emperor_health - self.player_attack == attack_emperor(self.player_attack, self.attack_frames, self.position, self.attacker, self.attack_type_text, self.emperor_health, self.player_health, attack, rotation))):
                        valid = False
        
        self.assertTrue(valid)

    @patch('ArithmeticEmperor.display_basic_screen')
    @patch('ArithmeticEmperor.display_static_text')
    def test_player_attacked_inccorrect(self, mock_display_static_text, mock_display_basic_screen):
        """
        Tests the player's health after answering the question incorrectly. See if emperor attacks player
        """
        player_health_before = 100 
        expected_player_health = player_health_before - self.emperor_attack_power
        
        # Call the function to simulate the attack
        updated_player_health = attack_player(self.emperor_attack_power, self.attack_frames, self.position, self.attacker, self.attack_type_text, self.attacked_emperor, self.emperor_health, self.player_health, self.emperor_rotation[0])

        # Check if the player's health is as expected
        self.assertEqual(expected_player_health, updated_player_health, "Player's health should decrease after getting the question wrong.")

    @patch('ArithmeticEmperor.display_basic_screen')
    @patch('ArithmeticEmperor.display_static_text')
    def test_player_attacked_correct(self, mock_display_static_text, mock_display_basic_screen):
        """
        Tests the player's health after answering the question correctly. See if emperor attacks player or not.
        """
        # Now the emperor may or may not respond after the player gets question right
        self.attacked_emperor = True if random.random() <= 0.5 else False
        
        # Call the function to simulate the attack
        updated_player_health = attack_player(self.emperor_attack_power, self.attack_frames, self.position, self.attacker, self.attack_type_text, self.attacked_emperor, self.emperor_health, self.player_health, self.emperor_rotation[0])

        # Check if the player's health is approximately as expected (due to randomness)
        self.assertTrue(updated_player_health == 70 or updated_player_health == 100, "Player's health should be approximately correct based on randomness.")

    def test_check_answer_correct(self):
        """
        Tests if check_answer correctly identifies a correct answer
        """
        correct_answer = "10"
        player_answer = "10"
        
        is_correct = check_answer(player_answer, correct_answer)
        
        self.assertTrue(is_correct, "check_answer is validating a correct answer as incorrect")
    
    def test_check_answer_incorrect(self):
        """
        Tests if check_answer correctly identifies an incorrect answer
        """
        correct_answer = "10"
        player_answer = "5"
        is_correct = check_answer(player_answer, correct_answer)
        
        self.assertFalse(is_correct, "check_answer is validating an inccorrect answer as correct")

if __name__ == "__main__":
    unittest.main()