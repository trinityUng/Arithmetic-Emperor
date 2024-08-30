"""
This module implements the logic and the requirements to generate a new question.
"""
# Import appropriate libraries
import random
from Player import Player

class Question:
    """
    A class to generate arithmetic questions based on the player's level.

    Attributes:
        player (Player): The player for whom the question is being generated.
    """

    def __init__(self, player):
        """
        Initializes the Question object with a player.

        Parameters:
            player (Player): The player for whom the question is being generated.
        """
        self.player = player

    def generate_question(self, operation):
        """
        Generates an arithmetic question based on the player's level and the specified operation.

        Parameters:
            operation (str): The arithmetic operation for the question ('+', '-', '*', '/', or 'emperor').

        Returns:
            list: A list containing the question as a string and the answer as an integer or float.
        """
        # For the addition operation
        if operation == '+':
            # Obtain the current player's level
            level = int(self.player.get_add())
            if level < 5: # For single digit addition
                num1 = random.randint(1, 9)
                num2 = random.randint(1, 9)
            elif level < 10:
                num1 = random.randint(1, 49)
                num2 = random.randint(1, 49)
            else: # For double digit addition
                num1 = random.randint(1, 99)
                num2 = random.randint(1, 99)

            # Calculate the answer
            ans = num1 + num2
            # Create the question format
            q = str(num1) + " + " + str(num2) + " = ?"
            # Return the question and answer
            return [q, ans]
            
        # For the subtraction operation
        elif operation == '-':
            # Obtain the current player's level
            level = int(self.player.get_sub())
            
            if level <= 5: # For single digit
                digits = (1, 9)
            elif level <=10:
                digits = (1, 20)
            else: # For double digits
                digits = (1, 50)
            
            # Create random numbers
            num1 = random.randint(*digits)
            num2 = random.randint(*digits)

            # Ensure b <= a for subtraction
            if num2 > num1:
                num1, num2 = num2, num1  # Swap values
            
            # Calculate the answer
            ans = num1 - num2

        # For the multiplication operation
        elif operation == '*':
            # Obtain the current player's level
            level = int(self.player.get_mul())
            if level <= 5:
                digits = (2, 4)  # Single-digit numbers    
            elif 5 < level <= 10:
                digits = (2, 7)  # Single and double-digit numbers
            elif 10 < level <= 15:
                digits = (2, 10)  # Single, harder double-digit numbers
            elif 15 < level <= 20:
                digits = (2, 15)  # Single, and all double-digit numbers
            elif 20 < level <= 25:
                digits = (2, 20)  # Single, double, and easier triple-digit numbers
            elif 25 < level <= 30:
                digits = (2, 25)  # Single, double, and harder triple-digit numbers
            elif level > 30:
                digits = (2, 30)
            
            # Create random numbers
            num1 = random.randint(*digits)
            num2 = random.randint(*digits)

            # If the numbers are the same set and the second number is 1, then increment the second number by 1
            if num2 == num1:
                if num2 == 1:
                    num2+=1
                # Otherwise, decrement the second number by 1
                else:
                    num2-=1
            # Return the two number
            return [num1, num2]
        
        # For the divison operation
        elif operation == "/":
            # Obtain the current player's level
            level = int(self.player.get_div())
            if level <= 5:
                digits = (1, 2)  # Dividing numbers from 4 and below
            elif 5 < level <= 10:
                digits = (1, 4)  # Dividing numbers from 16 and below
            elif 10 < level <= 15:
                digits = (1, 6)  # Dividing numbers from 36 and below
            elif 15 < level <= 20:
                digits = (1, 8)  # Dividing numbers from 64 and below
            elif 20 < level <= 25:
                digits = (1, 10)  # Dividing numbers from 100 and below
            elif 25 < level <= 30:
                digits = (1, 12)  # Dividing numbers from 144 and below

            # Generate the numbers randomly
            num1 = random.randint(*digits)
            num2 = random.randint(*digits)

            # Calculate the correct answer
            dividend = num1 * num2
            quotient = dividend / num1
            # Format the question
            question = f"{dividend} / {num1}?"

            # Return the question and answer
            return [int(quotient), question]
        
        # For Arithemetic Emperor
        else:
            operandSymbols = ['+', '-', '*', '/']

            level = int(self.player.get_bosses())
            if level <= 5:
                digits = (1, 3)   
            elif 5 < level <= 10:
                digits = (1, 4)  
            elif 10 < level <= 15:
                digits = (1, 5) 
            elif 15 < level <= 20:
                digits = (1, 6) 
            elif 20 < level <= 25:
                digits = (1, 7)
            elif 25 < level <= 30:
                digits = (1, 8) 
            elif level > 30:
                digits = (1, 9)

            equationFound = False
            while True:
                num_operands = random.randint(2, 4)  # Random number of operands
                operands = random.choices(operandSymbols, k=num_operands)  # Randomly select operands
                numbers = [random.randint(digits[0], digits[1]) for _ in range(num_operands + 1)]  # Generate random numbers
                
                for i in range (len(operands)):
                    if operands[i] == '/':
                        if numbers[i]%numbers[i + 1] == 0:
                            equationFound = True
                        else:
                            equationFound = False
                            break

                if equationFound:
                    break

            expression = ' '.join([f'{num} {op}' for num, op in zip(numbers[:-1], operands)]) + f' {numbers[-1]}'
            result = eval(expression)
            return [expression, result]

        # Wrtie the question based on the operation given
        question = f"{num1} {operation} {num2}?"
    
        # Return the question and answer
        return [question, ans]