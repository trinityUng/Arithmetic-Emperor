import unittest
from unittest.mock import mock_open, patch
from Player import Player

class TestPlayer(unittest.TestCase):
    """
    Unit tests for the Player class.
    """

    def setUp(self):
        """
        Set up the test environment by creating a Player instance.
        """
        self.player = Player("test_user", "test_password")

    def test_initialization(self):
        """
        Test the initialization of a Player object.
        """
        self.assertEqual(self.player.name, "test_user")
        self.assertEqual(self.player.password, "test_password")
        self.assertEqual(self.player.level, 0)
        self.assertEqual(self.player.addition, 0)
        self.assertEqual(self.player.subtraction, 0)
        self.assertEqual(self.player.multiplication, 0)
        self.assertEqual(self.player.division, 0)
        self.assertEqual(self.player.bosses, 0)

    @patch('csv.reader')
    def test_load_player(self, mock_csv_reader):
        """
        Test loading a player's information from a CSV file.
        """
        mock_csv_reader.return_value = iter([["test_user", "test_password", "5", "4", "3", "2", "1"]])
        self.player.load_player()
        self.assertEqual(self.player.addition, "5")
        self.assertEqual(self.player.subtraction, "4")
        self.assertEqual(self.player.multiplication, "3")
        self.assertEqual(self.player.division, "2")
        self.assertEqual(self.player.bosses, "1")

    @patch('csv.writer')
    @patch('csv.reader')
    def test_save_info(self, mock_csv_reader, mock_csv_writer):
        """
        Test saving a player's information to a CSV file.
        """
        mock_file = mock_open()
        mock_csv_reader.return_value = iter([["test_user", "test_password", "1", "2", "3", "4", "5"]])
        with patch("builtins.open", mock_file):
            self.player.save_info()
            # Check if writerows was called with the expected data
            mock_csv_writer.return_value.writerows.assert_called_with([["test_user", "test_password", 0, 0, 0, 0, 0]])

    def test_update_bosses(self):
        """
        Test updating a player's boss score and saving the information.
        """
        new_score = 10
        with patch.object(Player, 'save_info') as mock_save_info:
            self.player.update_bosses(new_score)
            self.assertEqual(self.player.bosses, new_score)
            mock_save_info.assert_called_once()

    def test_update_add(self):
        """
        Test updating a player's addition score and saving the information.
        """
        new_score = 10
        with patch.object(Player, 'save_info') as mock_save_info:
            self.player.update_add(new_score)
            self.assertEqual(self.player.addition, new_score)
            mock_save_info.assert_called_once()

    def test_update_mul(self):
        """
        Test updating a player's multiplication score and saving the information.
        """
        new_score = 10
        with patch.object(Player, 'save_info') as mock_save_info:
            self.player.update_mul(new_score)
            self.assertEqual(self.player.multiplication, new_score)
            mock_save_info.assert_called_once()

    def test_update_div(self):
        """
        Test updating a player's division score and saving the information.
        """
        new_score = 10
        with patch.object(Player, 'save_info') as mock_save_info:
            self.player.update_div(new_score)
            self.assertEqual(self.player.division, new_score)
            mock_save_info.assert_called_once()

    def test_update_sub(self):
        """
        Test updating a player's subtraction score and saving the information.
        """
        new_score = 10
        with patch.object(Player, 'save_info') as mock_save_info:
            self.player.update_sub(new_score)
            self.assertEqual(self.player.subtraction, new_score)
            mock_save_info.assert_called_once()

    def test_get_name(self):
        """
        Test retrieving a player's name.
        """
        self.assertEqual(self.player.get_name(), "test_user")

    def test_get_bosses(self):
        """
        Test retrieving a player's boss score.
        """
        self.player.bosses = 5
        self.assertEqual(self.player.get_bosses(), 5)

    def test_get_add(self):
        """
        Test retrieving a player's addition score.
        """
        self.player.addition = 5
        self.assertEqual(self.player.get_add(), 5)

    def test_get_mul(self):
        """
        Test retrieving a player's multiplication score.
        """
        self.player.multiplication = 5
        self.assertEqual(self.player.get_mul(), 5)

    def test_get_div(self):
        """
        Test retrieving a player's division score.
        """
        self.player.division = 5
        self.assertEqual(self.player.get_div(), 5)

    def test_get_sub(self):
        """
        Test retrieving a player's subtraction score.
        """
        self.player.subtraction = 5
        self.assertEqual(self.player.get_sub(), 5)

if __name__ == '__main__':
    unittest.main()
