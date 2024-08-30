import unittest
import pygame
from unittest.mock import patch
from CookingGame import add_dumpling, update_photos, handle_events  # Correct imports

class TestCookingGame(unittest.TestCase):
    def test_add_dumpling_within_bounds(self):
        """
        Tests that a dumpling added to the game is placed within the specified bounds.
        This checks that the dumpling's position falls within the rectangle defined by
        the `central_area`, ensuring it is not placed outside of the expected gameplay area.
        """
        dumpling_positions = []
        central_area = pygame.Rect(100, 100, 200, 200)
        add_dumpling(dumpling_positions, central_area)
        self.assertTrue(100 <= dumpling_positions[0][0] <= 300)
        self.assertTrue(100 <= dumpling_positions[0][1] <= 300)
    
    def test_add_dumpling_increases_count(self):
        """
        Verifies that calling the `add_dumpling` function increases the count of dumplings
        by 1, ensuring that dumplings are successfully added to the game's state.
        """
        dumpling_positions = []
        central_area = pygame.Rect(100, 100, 200, 200)
        add_dumpling(dumpling_positions, central_area)
        self.assertEqual(len(dumpling_positions), 1)

    @patch('CookingGame.pygame.event.get')
    def test_add_and_remove_dumpling(self, mock_get):
        """
        Tests the game's response to events for adding and then removing a dumpling.
        This simulates a user pressing keys to add a dumpling to the game and subsequently
        remove it, verifying that the game correctly updates its state in response to these actions.
        """
        dumpling_positions = []
        central_area = pygame.Rect(100, 100, 200, 200)
        
        # Simulate adding a dumpling
        mock_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})]
        handle_events(dumpling_positions, central_area, [])
        self.assertEqual(len(dumpling_positions), 1)
        
        # Simulate removing the added dumpling
        mock_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})]
        handle_events(dumpling_positions, central_area, [])
        self.assertEqual(len(dumpling_positions), 0)

    def test_update_photos_adds_photo(self):
        """
        Tests that photos are added to the game at appropriate intervals.
        This checks the functionality responsible for adding new photos to the game,
        ensuring that photos are added when expected based on time intervals.
        """
        photo_positions = [(0, 0)]
        last_photo_time = 0
        current_time = 101
        total_questions_generated = 0
        last_photo_time, photo_added = update_photos(photo_positions, last_photo_time, current_time, total_questions_generated)
        self.assertTrue(photo_added)
        self.assertEqual(len(photo_positions), 2)

    @patch('CookingGame.pygame.event.get')
    def test_handle_events_back_button(self, mock_get):
        """
        Tests the game's handling of the 'back' button event, simulating a user clicking
        the back button and verifying that the game responds as expected.
        """
        mock_get.return_value = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (40, 25)})]
        result = handle_events([], pygame.Rect(0, 0, 0, 0), [])
        self.assertEqual(result, 3)
    
    @patch('CookingGame.pygame.event.get')
    def test_space_bar_incorrect_dumplings(self, mock_get):
        """
        Simulates pressing the space bar to check if the player has the correct number of dumplings
        as per the current question. Adjusts the test environment to accurately reflect the game
        state and verifies that `handle_events` properly evaluates the scenario and returns the
        expected result indicating an incorrect answer.
        """
        global number_of_dumplings  # Ensure this matches how it's used in the actual game logic
        dumpling_positions = [(100, 100), (150, 150), (125, 125)]  # Setup to match expected answer
        central_area = pygame.Rect(100, 100, 200, 200)
        questions = [("How many dumplings?", 2)]  # Current question expecting 2 dumplings

        # Simulate pressing the space bar
        mock_get.return_value = [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})]
        
        result = handle_events(dumpling_positions, central_area, questions)

        self.assertEqual(result, 2, "handle_events should return 2 for incorrect number of dumplings")


if __name__ == '__main__':
    unittest.main()
