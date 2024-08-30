import unittest
from unittest.mock import patch, mock_open
from mainMenu import append_to_csv, username_exists, validate_username, validate_password, load_player

class TestMainMenu(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_append_to_csv(self, mock_file):
        """
        Appends a new user's username and password to a CSV file while initializing their game stats to 0.

        Parameters:
        - username (str): The username of the new user
        - password (str): The password for the new user.

        Returns:
        None
        """
        append_to_csv('testuser', 'testpass')
        mock_file.assert_called_with('data.csv', 'a', newline='')
        mock_file().write.assert_called_once()

    @patch('mainMenu.csv.reader')
    def test_username_exists(self, mock_csv_reader):
        """
        Checks if the given username already exists in the specified CSV file.

        Parameters:
        - username (str): The username to check for existence.
        - filepath (str, optional): The path to the CSV file. Defaults to "data.csv".

        Returns:
        - bool: True if the username exists, False otherwise.
        """
        mock_csv_reader.return_value = iter([['testuser', 'testpass']])
        self.assertTrue(username_exists('testuser'))
        self.assertFalse(username_exists('nonexistentuser'))

    def test_validate_username(self):
        """
        Validates the given username based on predetermined criteria (alphanumeric characters only).

        Parameters:
        - username (str): The username to validate.

        Returns:
        - bool: True if the username is valid, False otherwise.
        """
        self.assertTrue(validate_username('validUser123'))
        self.assertFalse(validate_username('invalid user'))
        self.assertFalse(validate_username('!@#$%'))

    def test_validate_password(self):
        """
        Validates the given password based on predetermined criteria (length and alphanumeric characters).

        Parameters:
        - password (str): The password to validate.

        Returns:
        - bool: True if the password is valid, False otherwise.
        """
        self.assertTrue(validate_password('ValidPass123'))
        self.assertFalse(validate_password('short'))
        self.assertFalse(validate_password('toolongpassworddefinitely'))
        self.assertFalse(validate_password('no$ymb0l$'))
    
    @patch("builtins.open", mock_open(read_data="username,password,0,0,0,0,0\nanotheruser,pass,1,1,1,1,1"))
    def test_load_player(self):
        """
        Loads a player's information from a CSV file based on the given username and password.

        Parameters:
        - input_username (str): The username of the player to load.
        - input_password (str): The password of the player to load.

        Returns:
        - dict or None: A dictionary containing the player's information if found, or None if not found.
        """
        self.assertIsNotNone(load_player('username', 'password'))
        self.assertIsNone(load_player('nonexistentuser', 'nopass'))

if __name__ == "__main__":
    unittest.main()