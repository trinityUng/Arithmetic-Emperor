"""
This module implements the logic and the requirements to create a new Player object.
"""
# Import appropriate libraries
import csv

class Player: 
    """
    A class to represent a player in the game.

    Attributes:
    - name (str): The player's username.
    - password (str): The player's password.
    - level (int): The player's current level in the game.
    - addition (int): The player's high score in addition questions.
    - subtraction (int): The player's high score in subtraction questions.
    - multiplication (int): The player's high score in multiplication questions.
    - division (int): The player's high score in division questions.
    - bosses (int): The number of bosses the player has defeated.
    """
    def __init__ (self, name, password):
        """
        Constructs all the necessary attributes for the player object.

        Parameters:
        - name (str): The name of the player.
        - password (str): The password of the player.
        """
        self.name = name
        self.password = password
        self.level = 0
        self.addition = 0
        self.subtraction = 0
        self.multiplication = 0
        self.division = 0
        self.bosses = 0
    
    def load_player(self):
        """
        Loads the player's data from a CSV file based on their username and password.
        """
        # Open the CSV file and obtian the player's information
        with open("data.csv", newline = '') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                username, password = row[0], row[1]

                # If the player exists
                if username == self.name and password == self.password:
                    # Set the scores to the player's scores within the file
                    self.addition = row[2]
                    self.subtraction = row[3]
                    self.multiplication = row[4]
                    self.division = row[5]
                    self.bosses = row[6]

    def save_info(self):
        """
        Saves the current player's data to a CSV file, updating their scores and information.
        """
        player = []

        # Read current info and match with current player
        with open("data.csv", "r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == self.name and row[1] == self.password:
                    # Update this player's data
                    row[2] = self.addition
                    row[3] = self.subtraction
                    row[4] = self.multiplication
                    row[5] = self.division
                    row[6] = self.bosses
                player.append(row)
        
        # Write the updated/all data back to the CSV
        with open("data.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(player)
    
    def update_bosses (self, new_bosses_score):
        """
        Updates the player's boss defeat count and saves the new information.

        Parameters:
        - new_bosses_score (int): The new boss defeat count.
        """
        self.bosses = new_bosses_score
        self.save_info()

    def update_add (self, new_add_score):
        """
        Updates the player's addition high score and saves the new information.

        Parameters:
        - new_add_score (int): The new addition high score.
        """
        self.addition = new_add_score
        self.save_info()

    def update_mul (self, new_mul_score):
        """
        Updates the player's multiplication high score and saves the new information.

        Parameters:
        - new_mul_score (int): The new multiplication high score.
        """
        self.multiplication = new_mul_score
        self.save_info()

    def update_div (self, new_div_score):
        """
        Updates the player's division high score and saves the new information.

        Parameters:
        - new_div_score (int): The new division high score.
        """
        self.division = new_div_score
        self.save_info()

    def update_sub (self, new_sub_score):
        """
        Updates the player's subtraction high score and saves the new information.

        Parameters:
        - new_sub_score (int): The new subtraction high score.
        """
        self.subtraction = new_sub_score
        self.save_info()

    def get_name (self):
        """
        Returns the player's username.

        Returns:
        - str: The player's username.
        """
        return self.name
    
    def get_bosses (self):
        """
        Returns the player's boss defeat count.

        Returns:
        - int: The number of bosses the player has defeated.
        """
        return self.bosses
    
    def get_add (self):
        """
        Returns the player's addition high score.

        Returns:
        - int: The player's high score in addition questions.
        """
        return self.addition
    
    def get_mul (self):
        """
        Returns the player's multiplication high score.

        Returns:
        - int: The player's high score in multiplication questions.
        """
        return self.multiplication
    
    def get_div (self):
        """
        Returns the player's division high score.

        Returns:
        - int: The player's high score in division questions.
        """
        return self.division
    
    def get_sub (self):
        """
        Returns the player's subtraction high score.

        Returns:
        - int: The player's high score in subtraction questions.
        """
        return self.subtraction