"""
This module implements the logic and the requirements to run the Sandwich Stack game using Pygame. It is a game
where the player uses the left and right arrow keys to move a panda character left and right of the screen to
catch falling food to answer the required math questions. The game includes a start, instruction, win, loss,
and game screen, as well as movement mechanics and the logic for collision detection.
"""
# Import appropriate libraries
import pygame, sys, random
from Button import Button
from Player import Player
from Question import Question

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

# Initialize sounds for game
LOSS = pygame.mixer.Sound("sound/LossSound.mp3")
WIN = pygame.mixer.Sound("sound/LevelComplete.mp3")
CORRECT = pygame.mixer.Sound("sound/Correct.mp3")
INCORRECT = pygame.mixer.Sound("sound/Incorrect.mp3")

# Initialize the base screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SANDWICH STACK')

# Initialize the screen backgrounds
BACKGROUND = pygame.image.load("images/sandwich_stack_bg.png")
START_SCREEN = pygame.image.load("images/sandwich_stack_start.png")
DIVISION_INSTRUCTIONS = pygame.image.load("images/division_instruction.png")
SS_INSTRUCTIONS = pygame.image.load("images/ss_instructions.png")
WIN_SCREEN = pygame.image.load("images/ss_win_screen.png")
LOSE_SCREEN = pygame.image.load("images/ss_lose_screen.png")
RECTANGLE = pygame.image.load("images/rectangle.png")

# Initalize smaller assets and features
LINE = pygame.image.load("images/line.png")
BACK = pygame.image.load("images/back_button.png")
RESIZED_BACK = pygame.image.load("images/resized_back.png")
RESIZED_NEXT = pygame.transform.rotate(pygame.image.load("images/resized_back.png"), 180)
HEART_F = pygame.image.load("images/heart_full.png")
HEART_E = pygame.image.load("images/heart_empty.png")
HEART_FULL = pygame.transform.scale(HEART_F, (50, 50))
HEART_EMPTY = pygame.transform.scale(HEART_E, (50, 50))

# Initialize the player's character (panda)
PANDA_SPEED = 4
PANDA = pygame.transform.scale(pygame.image.load("images/panda_tray.png"), (190, 126))
panda_rect = PANDA.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))

# Initialize the food items
CARROT = pygame.transform.scale(pygame.image.load("images/carrot.png"), (75, 79))
BREAD = pygame.transform.scale(pygame.image.load("images/bread.png"), (90, 62))
CUCUMBER = pygame.transform.scale(pygame.image.load("images/cucumber.png"), (70, 70))
MEAT = pygame.transform.scale(pygame.image.load("images/meat.png"), (115, 54))
food_items = [CARROT, BREAD, CUCUMBER, MEAT]


def get_font(font, size):
    """
    Loads and returns a Pygame font object based on a given font name and size.

    Parameters:
    - font (str): A string representing the font name. If the font is "Sawarabi" or "Shojumaru",
            a specific font fle is loaded
    - size (int): The size of the font in points

    Returns:
    A Pygame font object.
    """
    if font == "Sawarabi":
        return pygame.font.Font("fonts/SawarabiMincho-Regular.ttf", size)
    elif font == "Shojumaru":
        return pygame.font.Font("fonts/Shojumaru-Regular.ttf", size)

def spawn_food(answer_bank):
    """
    Selects a random food item and spawns it as a random location at the top of the screen.
    An answer is chosen randomly from the provided answer band and associated with the food item.

    Parameters:
    - answer_bank: A list of possible answer (integers) that can be associated with the food item.

    Returns:
    A tuple containing the food surface, its Rect object, the chosen answer, the rendered answer
    text surface, and its Rect object.
    """
    # This block of code randomly chooses a food item and answer from a item list and answer bank list, then randomly places them
    food = random.choice(food_items)
    answer = random.choice(answer_bank)
    x_pos = random.randrange(0, SCREEN_WIDTH - food.get_width())
    y_pos = -food.get_height()
    food_rect = food.get_rect(topleft = (x_pos, y_pos))

    # Initializes the font for the text and renders the text
    font = get_font('Shojumaru', 15)
    text_surface = font.render(str(answer), True, "white")
    text_rect = text_surface.get_rect(center = (food_rect.centerx, food_rect.y - 20))
    return food, food_rect, answer, text_surface, text_rect

# Start spawning food items
current_food, current_food_rect, current_answer, answer_text_surface, answer_text_rect = spawn_food([random.randint(1, 144), random.randint(1, 144)])

def instruction1():
    """
    Displays the first instruction screen.

    This screen shows the instructions for the division operation and has two buttons: one to go to the previous screen and one to proceed to the next
    instruction screen. This function checks for a mouse input to determine which button has been clicked.

    Parameters:
    None

    Returns:
    None
    """
    while True:
        # Obtain the mouse position on the screen
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        # Place the first instruction screen
        SCREEN.blit(DIVISION_INSTRUCTIONS, (0, 0))

        # Create the next and back buttons
        INSTRUCTIONS_BACK = Button(pygame.image.load("images/back_button.png"), pos = (70, 55), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
        INSTRUCTIONS_NEXT = Button(pygame.transform.rotate(pygame.image.load("images/back_button.png"), 180), pos = (680, 475), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
        INSTRUCTIONS_BACK.update(SCREEN)
        INSTRUCTIONS_NEXT.update(SCREEN)

        # If the mouse hovers over the buttons, resize the button to be bigger
        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))
        if (690<MOUSE_X<705 and 465<MOUSE_Y<490):
            SCREEN.blit(RESIZED_NEXT, (540, 324))

        # Check for events
        for event in pygame.event.get():
            # If the user exits out of the screen, close pygame and exit the system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            # If the user clicks using the left mouse key
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Go back to the title screen if the back button is pressed
                if INSTRUCTIONS_BACK.checkInput(GAME_MOUSE_POS):
                    return
                # Go to next instruction screen if the next button is pressed
                if INSTRUCTIONS_NEXT.checkInput(GAME_MOUSE_POS):
                    instruction2()
        # Update the screen
        pygame.display.update()

def instruction2():
    """
    Displays the second instruction screen.

    This screen shows the instructions to play the game and has a button to back to the first instruction screen when clicked. It checks for the mouse position and input
    to determine if the back button has been clicked.

    Parameters:
    None

    Returns:
    None
    """
    while True:
        # Obtain the mouse position on the screen
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        # Place the second instruction screen
        SCREEN.blit(SS_INSTRUCTIONS, (0, 0))
        
        # Create the next and back buttons
        INSTRUCTIONS_BACK = Button(pygame.image.load("images/back_button.png"), pos = (70, 55), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
        INSTRUCTIONS_BACK.update(SCREEN)

        # If the mouse hovers over the buttons, resize the button to be bigger
        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))

        # Check for events
        for event in pygame.event.get():
            # If the user exits out of the screen, close pygame and exit the system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            # If the user clicks using the left mouse key
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Go back to the first instruction screen if the back button is pressed
                if INSTRUCTIONS_BACK.checkInput(GAME_MOUSE_POS):
                    return
        # Update the screen
        pygame.display.update()

def sandwich_stack(username, password):
    """
    Initiates the Sandwich Stack game from the main menu.

    The title screen has three options: start the game, view instructions, or return to the game map. This function sets ip the title screen and handles button clicks for navigating. Background
    music is played upon starting this screen.

    Parameters:
    - username (str): A string representing the player's username. Used for authentication purposes for later uses (obtaining the player's division level).
    - password (str): A string representing the player's password. Used for authentication purposes for later uses (obtaining the player's division level).

    Returns:
    None
    """
    # Play the background music
    play_music("sound/SandwichStackMusic.mp3")
    while True:
        # Obtain the mouse position on the screen
        MOUSE_POS = pygame.mouse.get_pos()
        # Place the title screen
        SCREEN.blit(START_SCREEN, (0,0))

        # Create the start, instructions, and return to game map buttons
        START_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 250), text_input = "START GAME", font = get_font("Shojumaru", 22), base_colour = "#b51f09", hovering_colour = "White")
        INSTRUCTION_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 380), text_input = "INSTRUCTIONS", font = get_font("Shojumaru", 22), base_colour = "#b51f09", hovering_colour = "White")
        RETURN_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 510), text_input = "BACK TO MAP", font = get_font("Shojumaru", 22), base_colour = "#b51f09", hovering_colour = "White")

        # For each button, allow the button to change the colour duing the hover state and then update the button on the screen
        for button in [START_BUTTON, INSTRUCTION_BUTTON, RETURN_BUTTON] :
            button.changeColour(MOUSE_POS)
            button.update(SCREEN)

        # Check for events
        for event in pygame.event.get():
            # If the user exits out of the screen, close pygame and exit the system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            # If the user clicks using the left mouse key
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Start the game if the "start" button is clicked
                if START_BUTTON.checkInput(MOUSE_POS):
                      start_game(username, password)
                # Go to the instructions page if the "instruction" button is clicked
                if INSTRUCTION_BUTTON.checkInput(MOUSE_POS):
                     instruction1()
                # Go back to the game map if the "return" button is clicked
                if RETURN_BUTTON.checkInput(MOUSE_POS):
                     return

        # Update the display
        pygame.display.update()

def win_screen(score):
    """
    Displays the win screen after a player successfully completes the game (earning a score of 5).

    The screen congratulates the player and shows their updated division level. 
    It provides a button to return to the title screen.

    Parameters:
    - score (int): The final score achieved by the player, used to display the division level.

    Returns:
    None
    """
    # Stop playing the background music and then play the level completed music
    pygame.mixer.music.stop()
    WIN.play()
    while True:
        # Obtain the mouse position on the screen
        MOUSE_POS = pygame.mouse.get_pos()
        # Place the win screen
        SCREEN.blit(WIN_SCREEN, (0, 0))

        # Create the new level update and progress status then place the font onto the screen
        font = get_font("Shojumaru", 15)
        score_surface = font.render(f"Your Division Level is Now: {score}", True, "White")
        progress_surface = font.render("Your progress has been saved.", True, "White")
        SCREEN.blit(score_surface, (250, 420))
        SCREEN.blit(progress_surface, (240, 440))
            
        # Place the button to return to the title screen
        RETURN = Button(image = pygame.image.load("images/scroll_button.png"), pos = (SCREEN_WIDTH / 2, 520), text_input = "TITLE SCREEN", font = get_font("Shojumaru", 18), base_colour = "#b51f09", hovering_colour = "White")
        RETURN.changeColour(MOUSE_POS)
        RETURN.update(SCREEN)

        # Check for events
        for event in pygame.event.get():
            # If the user exits out of the screen, close pygame and exit the system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            # If the user clicks using the left mouse key
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Go back to the title screen if the "return" button
                if RETURN.checkInput(MOUSE_POS):
                    return
        # Update the display
        pygame.display.update()

def lose_screen(username, password, score):
    """
    Displays the lose screen if the player loses all three lives before completing the game.

    The screen shows the player's current division level and the score they achieved. It also 
    provides a button to return to the title screen. The player's data, such as the division level, 
    is loaded based on the provided username and password.

    Parameters:
    - username (str): The username of the player, used to load player data.
    - password (str): The password of the player, used for authentication purposes when loading player data.
    - score (int): The score achieved by the player up to the point of losing the game.

    Returns:
    None
    """
    # Stop playing the background music and then play the level incomplete music
    pygame.mixer.music.stop()
    LOSS.play()
    # Create a new player instance and load the player's stats
    player = Player(username, password)
    player.load_player()
    while True:
        # Obtain the position of the mouse
        MOUSE_POS = pygame.mouse.get_pos()

        # Display the losing screen background
        SCREEN.blit(LOSE_SCREEN, (0, 0))
        # Create the player's level and display it on the screen
        level_font = get_font("Shojumaru", 20)
        level_surface = level_font.render(f"Current level: {player.get_div()}", True, "White")
        SCREEN.blit(level_surface, (130, 340))

        # Create the player's current score and display it on the screen
        score_font = get_font("Shojumaru", 20)
        score_surface = score_font.render(f"Score: {score} / 5", True, "White")
        SCREEN.blit(score_surface, (520, 340))

        # Create a return button to go back to the title screen
        RETURN = Button(image = pygame.image.load("images/scroll_button.png"), pos = (SCREEN_WIDTH / 2, 440), text_input = "TITLE SCREEN", font = get_font("Shojumaru", 18), base_colour = "#b51f09", hovering_colour = "White")
        RETURN.changeColour(MOUSE_POS)
        RETURN.update(SCREEN)

        # Check for events
        for event in pygame.event.get():
            # If the user exits out of the screen, close pygame and exit the system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            # If the user clicks using the left mouse key
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Go back to the title screen if the "return" button
                if RETURN.checkInput(MOUSE_POS):
                    return
        # Update the display
        pygame.display.update()

def play_music(file):
    """
    Initializes the Pygame mixer module and plays the specified music file in a continuous loop.

    Parameters:
    - file (str): The path to the music file to be played.

    Returns:
    None
    """
    pygame.mixer.init()                 # Initialize the music function from PyGame
    pygame.mixer.music.load(file)       # Load the sound file
    pygame.mixer.music.play(-1)         # Play the sound constantly

def start_game(username, password):
    """
    Starts the game loop. The player controls a panda character to catch falling food item that represent answers to the math question displayed. If the player catches the item with the
    correct answer, score increase by one until they reach five points. This means that they have practiced enough to earn a level point for their division skill. If the player catches
    the wrong item, they lose one life until they lose all three of their lives. This results in a game over and the player is prompted to return back to the title screen.

    Parameters:
    - username (str): A string representing the player's username. Used for authentication purposes (obtaining the player's division level).
    - password (str): A string representing the player's password. Used for authentication purposes (obtaining the player's division level).
    
    The function uses global variables for game state, such as the food items, panda character, and scores.
    """
    # Obtain the mouse position
    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
    MOUSE_POS = pygame.mouse.get_pos()

    # Initialize variables
    lives = 3
    score = 0
    message_active = True
    display_correct_message = False
    display_incorrect_message = False
    message_duration = 2000
    message_start_time = 0

    # Create a new player instance and load the player's stats
    player = Player(username, password)
    player.load_player()

    # Create an initial answer bank and generate a question to start 
    answer_bank = [random.randint(1, 144) for _ in range(3)]                # Create an initial answer bank
    current_question = Question(player)
    correct_answer, question = current_question.generate_question("/")
    answer_bank[0] = correct_answer                                         # Ensure one of the answers is correct
    # This will be used to display the previous correct answer if the player gets the wrong answer
    answers = [correct_answer, correct_answer]
    previous_answer = answers[0]
    level = player.get_mul()

    # Re-use the global variables to keep the current state
    global current_food, current_food_rect, current_answer, answer_text_surface, answer_text_rect
    current_food, current_food_rect, current_answer, answer_text_surface, answer_text_rect = spawn_food(answer_bank)

    clock = pygame.time.Clock()  # To control the game's framerate

    game_active = True
    while game_active:
        # Obtain the mouse position
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        MOUSE_POS = pygame.mouse.get_pos()
        # Check for events
        for event in pygame.event.get():
            # If the user exits out of the program, quit the game and exit the system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            # If the user left clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Go back to the title screen
                if BACK.checkInput(MOUSE_POS):
                    return

        # This block of code is to check for the keys pressed and moves the character accordingly
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and panda_rect.left > 0:
            panda_rect.x -= PANDA_SPEED
        if keys[pygame.K_RIGHT] and panda_rect.right < SCREEN_WIDTH:
            panda_rect.x += PANDA_SPEED

        # Set the speed for the falling food
        current_food_rect.y += 3

        # Place the answer rectangle on top of the food item
        answer_text_rect.centerx = current_food_rect.centerx
        answer_text_rect.y = current_food_rect.y - 20

        SCREEN.blit(BACKGROUND, (0, 0))                         # Place the background
        SCREEN.blit(PANDA, panda_rect)                          # Place the panda character
        SCREEN.blit(current_food, current_food_rect)            # Place the food item
        SCREEN.blit(answer_text_surface, answer_text_rect)      # Place the answer box
        # Place the top header assets
        SCREEN.blit(RECTANGLE, (0,0))
        SCREEN.blit(LINE, (0, 47))
        SCREEN.blit(LINE, (0, 149))

        # Set the font for the question and place the text on the screen
        font = get_font('Shojumaru', 20)
        text_surface = font.render('What is the answer to:', True, "White")
        question_surface = font.render(question, True, "White")
        SCREEN.blit(text_surface, (50, 75))
        SCREEN.blit(question_surface, (158, 100))

        # Create and place a back button
        BACK = Button(image = "images/back_button.png", pos = (40, 25), text_input = "", font = get_font("Shojumaru", 22), base_colour = "White", hovering_colour = "#b51f09")
        BACK.update(SCREEN)

        # If the user hovers over the back button, resize the image
        if (10<MOUSE_X<45 and 10<MOUSE_Y<40):
            SCREEN.blit(RESIZED_BACK, (-120,-126))

        # Check if there are 3 lives
        if lives == 3:
            # Place 3 full hearts
            SCREEN.blit(HEART_FULL, (400, 90))
            SCREEN.blit(HEART_FULL, (450, 90))
            SCREEN.blit(HEART_FULL, (500, 90))
        elif lives == 2:
            # Place 2 full hearts, 1 empty heart
            SCREEN.blit(HEART_FULL, (400, 90))
            SCREEN.blit(HEART_FULL, (450, 90))
            SCREEN.blit(HEART_EMPTY, (500, 90))
        elif lives == 1:
            # Place 1 full heart, 2 empty hearts
            SCREEN.blit(HEART_FULL, (400, 90))
            SCREEN.blit(HEART_EMPTY, (450, 90))
            SCREEN.blit(HEART_EMPTY, (500, 90))

        # Place the player's current division power and their score out of 5
        level_surface = font.render(f'Level: {level}', True, "White")
        score_surface = font.render(f'Score: {score} / 5', True, "White")
        lives_surface = font.render('Lives:', True, "White")
        SCREEN.blit(level_surface, (600, 80))
        SCREEN.blit(score_surface, (600, 100))
        SCREEN.blit(lives_surface, (440, 65))

        # Check if the character collides with the food item
        if panda_rect.colliderect(current_food_rect):
            # Create a timer and flag for a message to appear
            message_start_time = pygame.time.get_ticks()
            message_active = True

            # If the player grabs the correct answer
            if current_answer == correct_answer:
                # Display "Correct", play the correct sound, and add 1 to their score
                display_correct_message = True
                display_incorrect_message = False
                CORRECT.play()
                score += 1
            else:
                # Otherwise display the correct answer, play the incorrect sound, and subtract 1 life
                display_incorrect_message = True
                display_correct_message = False
                INCORRECT.play()
                lives -= 1

            # Check if the score is 5
            if score == 5:
                # The player has completed the level
                new_score = int(player.get_div()) + 1           # Add 1 to the player's current division level
                player.update_div(str(new_score))               # Update the level in the database
                win_screen(new_score)                           # Display the win screen
                play_music("sound/SandwichStackMusic.mp3")      # Replay the music if the user returns back
                return
            elif lives > 0:
                # Generate a new question and answer set
                answer_bank = [random.randint(1, 144) for _ in range(3)]
                correct_answer, question = current_question.generate_question("/")
                # Update the answer bank with the new correct answer
                answer_bank[0] = correct_answer
                # Obtain the previous correct answer
                answers = [answers[1], correct_answer]
                previous_answer = answers[0]
                # Spawn a new food item
                current_food, current_food_rect, current_answer, answer_text_surface, answer_text_rect = spawn_food(answer_bank)
            else:
                # End game loop if no lives left
                game_active = False
                lose_screen(username, password, score)      # Display the lose screen
                play_music("sound/SandwichStackMusic.mp3")  # Replay the music if the user returns back
                return

        # If a food item goes off the bottom of the screen
        if current_food_rect.top > SCREEN_HEIGHT:
            # Generate a new question and answer set
            current_food, current_food_rect, current_answer, answer_text_surface, answer_text_rect = spawn_food(answer_bank)

        # If a message is required
        if message_active:
            # Obtain the time (the message should display for 2 seconds)
            elapsed_time = pygame.time.get_ticks() - message_start_time
            # If the time that has passed is less than the set message duration
            if elapsed_time < message_duration:
                # If the message to display is the "correct" message
                if display_correct_message:
                    # Display "correct on the screen"
                    message_font = get_font("Shojumaru", 19)
                    message_surface = message_font.render("Correct!", True, "White")
                    SCREEN.blit(message_surface, (360, 160))
                # If the message to display is the "incorrect" message
                if display_incorrect_message:
                    # Display "incorrect" and the correct answer to the previous question
                    message_font = get_font('Shojumaru', 19)
                    message_surface = message_font.render(f"Incorrect. The answer is: {previous_answer}", True, "White")
                    SCREEN.blit(message_surface, (220, 160))
            else:
                # Otherwise set all the message flags to false
                message_active = False
                display_correct_message = False
                display_incorrect_message = False
        # Update the display
        pygame.display.update()
        # Keep the game running at 60 FPS
        clock.tick(60)
