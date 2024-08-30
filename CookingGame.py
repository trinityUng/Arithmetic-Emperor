"""
This module implements the logic and the requirements to run the  Cooking game using Pygame. It is a game
where the player uses the left and right arrow keys to add/remove dumplings on the plate to answer the questions on the order. The game includes a start, instruction, win, loss,
and game screen, as well as movement mechanics and the logic for collision detection.
"""

import pygame, sys
import random
from Button import Button
from Question import Question
from Player import Player

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Dumpling and Photo Settings
DUMPLING_SIZE = 100
PHOTO_SIZE = (200, 250)
PHOTO_INTERVAL_MS = 100
PHOTO_SPACING = 150

# Sounds
LOSS = pygame.mixer.Sound("sound/LossSound.mp3")
WIN = pygame.mixer.Sound("sound/LevelComplete.mp3")
CORRECT = pygame.mixer.Sound("sound/Correct.mp3")

# Colors
WHITE = (255, 255, 255)
GREEN = (88, 133, 120)

# Load images
BACKGROUND = pygame.image.load("images/cooking_game.png")
DUMPLING = pygame.image.load("images/dumpling.png")
DUMPLING = pygame.transform.scale(DUMPLING, (DUMPLING_SIZE, DUMPLING_SIZE))
ORDER = pygame.image.load("images/order.png")
ORDER = pygame.transform.scale(ORDER, PHOTO_SIZE)

# Changing screens
INSTRUCTION = pygame.image.load("images/Subtraction.png")
TUTORIAL = pygame.image.load("images/Instructions for cooking game.png")
BACK = pygame.image.load("images/back_button.png")
RESIZED_BACK = pygame.image.load("images/resized_back.png")
RESIZED_NEXT = pygame.transform.rotate(pygame.image.load("images/resized_back.png"), 180)
START_SCREEN = pygame.image.load("images/Cooking Game Start Screen.png")

LOSE_SCREEN = pygame.image.load("images/Cooking game lose game.png")
WIN_SCREEN = pygame.image.load("images/Cooking game winning.png")

# Back buttons
BACK = pygame.image.load("images/back_button.png")
RESIZED_BACK = pygame.image.load("images/resized_back.png")

# Initialize the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('COOKING GAME')

# Clock for controlling game speed
clock = pygame.time.Clock()

number_of_dumplings = 0 # Track the number of dumplings placed

def play_music(file):
    """
    Initializes the Pygame mixer and plays a specified music file on loop.

    Parameters:
    - file (str): The filepath to the music file to be played.

    Returns:
    None
    """
    
    # Plays background music
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def get_font(size):
    """
    Returns a Pygame font object of the specified size using a predefined font file.

    Parameters:
    - size (int): The desired font size.

    Returns:
    - pygame.font.Font: The font object of the specified size.
    """
    return pygame.font.Font("fonts/Shojumaru-Regular.ttf", size)

def instruction():
    """
    Displays the instruction screen with navigation options to go back or proceed to the tutorial.

    The function continuously checks for user inputs to navigate through the game's instruction screens
    using custom buttons.

    Parameters:
    None

    Returns:
    None
    """
    run = True
    while run:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        game_mouse_pos = pygame.mouse.get_pos()
        
        # Displays the instruction screen
        screen.blit(INSTRUCTION, (0, 0))
        
        # Buttons for the back and next button
        INSTRUCTIONS_BACK = Button(pygame.image.load("images/back_button.png"), pos = (70, 55), text_input = "", font = get_font(15), base_colour = "White", hovering_colour = "#b51f09")
        INSTRUCTIONS_NEXT = Button(pygame.transform.rotate(pygame.image.load("images/back_button.png"), 180), pos = (680, 475), text_input = "", font = get_font(15), base_colour = "White", hovering_colour = "#b51f09")
        
        # Increase the size of the button when users hover over the button
        if (40<mouse_x<75 and 40<mouse_y<70):
            screen.blit(RESIZED_BACK, (-90,-96))
        if (690<mouse_x<705 and 465<mouse_y<490):
            screen.blit(RESIZED_NEXT, (540, 324))

        # Updating the screen based on buttons
        INSTRUCTIONS_BACK.update(screen)
        INSTRUCTIONS_NEXT.update(screen)
        
        # This block listens for and handles Pygame events, including quitting the game or clicking mouse buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkInput(game_mouse_pos):
                    run = False
                if INSTRUCTIONS_NEXT.checkInput(game_mouse_pos):
                    tutorial()
        
        # Update the display
        pygame.display.update()

def tutorial():
    """
    Displays the tutorial screen with an option to navigate back to the previous screen.

    The function handles user interactions specifically for displaying the game's tutorial, 
    allowing the player to understand game mechanics.

    Parameters:
    None

    Returns:
    None
    """
    run = True
    while run:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        game_mouse_pos = pygame.mouse.get_pos()
        
        # Displays the instruction screen
        screen.blit(TUTORIAL, (0, 0))
        
        # Buttons for the back
        INSTRUCTIONS_BACK = Button(pygame.image.load("images/back_button.png"), pos = (70, 55), text_input = "", font = get_font(15), base_colour = "White", hovering_colour = "#b51f09")
        
        # Increase the size of the button when users hover over the button
        if (40<mouse_x<75 and 40<mouse_y<70):
            screen.blit(RESIZED_BACK, (-90,-96))
            
        # Updating the screen based on buttons
        INSTRUCTIONS_BACK.update(screen)
        
        # This block listens for and handles Pygame events, including quitting the game or clicking mouse buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkInput(game_mouse_pos):
                    return
        
        # Update the display
        pygame.display.update()


def handle_events(dumpling_positions, central_area, questions):
    """
    Handles user inputs and game events, including quitting the game, adding dumplings,
    removing dumplings, and checking answers.

    Parameters:
    - dumpling_positions (list): A list of tuples indicating the positions of dumplings on the screen.
    - central_area (pygame.Rect): A Pygame Rect object defining the central area of the screen.
    - questions (list): A list of questions for the player to answer.

    Returns:
    - int or None: An integer indicating a specific game event or action, or None if no action is required.
    """
    global number_of_dumplings
    # This block listens for and handles Pygame events, including quitting the game or clicking mouse buttons
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            BACK = Button(image="images/back_button.png", pos=(40, 25), text_input="", font=get_font(22), base_colour="White", hovering_colour="#b51f09")
            BACK.update(screen)
            
            if (10<mouse_x<45 and 10<mouse_y<40):
                screen.blit(RESIZED_BACK, (-120,-126))
            
            if BACK.checkInput(mouse_pos):
                return 3  # Signal that we should go back
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                add_dumpling(dumpling_positions, central_area) # Call function to add a dumpling
                number_of_dumplings += 1
            elif event.key == pygame.K_LEFT and dumpling_positions:
                dumpling_positions.pop() # Remove the last dumpling added
                number_of_dumplings -= 1
            elif event.key == pygame.K_SPACE and questions:  # Check answer when space bar is pressed
                if number_of_dumplings == questions[0][1]: 
                    # Clears the number of dumplings on the screen when the question is answered correctly
                    dumpling_positions.clear()
                    number_of_dumplings = 0
                    return 1
                else:
                    # Clears the number of dumplings on the screen when the question is answered incorrectly
                    dumpling_positions.clear()
                    return 2
    return None 

def add_dumpling(dumpling_positions, central_area):
    """
    Adds a dumpling to a random position within a specified area on the screen.

    Parameters:
    - dumpling_positions (list): A list that the new dumpling position will be appended to.
    - central_area (pygame.Rect): The area within which the dumpling will be placed.

    Returns:
    None
    """
    new_x = random.randint(central_area.left, central_area.right - DUMPLING_SIZE)
    new_y = random.randint(central_area.top, central_area.bottom - DUMPLING_SIZE)
    dumpling_positions.append((new_x, new_y))


def update_photos(photo_positions, last_photo_time, current_time, total_questions_generated):
    """
    Updates the positions of photos on the screen and adds new photos based on timing.

    Parameters:
    - photo_positions (list): A list of photo positions to be updated.
    - last_photo_time (int): The timestamp of the last photo update.
    - current_time (int): The current timestamp.
    - total_questions_generated (int): The total number of questions generated so far.

    Returns:
    - tuple: Contains updated last photo time and a boolean indicating if a new photo was added.
    """
    photo_added = False  # Track if a new photo is added
    if current_time - last_photo_time > PHOTO_INTERVAL_MS and total_questions_generated < 5:
        # Check if it's time to add a new photo and we haven't exceeded 5 questions
        last_photo_x, last_photo_y = photo_positions[-1] if photo_positions else (0, 0)
        new_photo_x = last_photo_x + PHOTO_SPACING if photo_positions else 0  # Adjust for the first photo
        if new_photo_x + PHOTO_SIZE[0] <= SCREEN_WIDTH:
            photo_positions.append((new_photo_x, 0))
            last_photo_time = current_time
            photo_added = True  # A new photo was added
    return last_photo_time, photo_added
    

def lose_screen(correct_order, question):
    """
    Displays the lose screen with an option to return to the title screen.

    Parameters:
    - correct_order (int): The correct order or answer that was expected.
    - question (str): The question that was asked.

    Returns:
    None
    """
    
    # Plays sound when the user loses
    pygame.mixer.music.stop()
    LOSS.play()
    run = True 
    pygame.display.update() # Update the display
    pygame.time.delay(1000)

    while run:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        game_mouse_pos = pygame.mouse.get_pos()
        # Create return button
        RETURN = Button(image = pygame.image.load("images/scroll_button.png"), pos = (400, 500), text_input = "TITLE SCREEN", font = get_font(18), base_colour = "#b51f09", hovering_colour = "White")
        
        screen.blit(LOSE_SCREEN, (0, 0))
        
        # Prints out the correct answer and the users answer when they get an answer wrong
        title_lines = ["Incorrect", f"Correct Answer = {question[1]}", f"Your Answer = {number_of_dumplings}"]
        
        line_height = get_font(25).get_height()
        
        # Displays text on screen
        for i, line in enumerate(title_lines):
            title_text = get_font(35).render(line, True, WHITE)
            inputRect = title_text.get_rect()
            inputRect.center = (SCREEN_WIDTH // 2, 300 + i * line_height)  # Adjust position for each line
            screen.blit(title_text, inputRect)

        RETURN.changeColour(game_mouse_pos)
        RETURN.update(screen)
        
        # This block listens for and handles Pygame events, including quitting the game or clicking mouse buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RETURN.checkInput(game_mouse_pos):
                    run = False

        if (660<mouse_x<685 and 390<mouse_y<415):
            screen.blit(RESIZED_NEXT, (510, 249))
        
        # Update the display
        pygame.display.update()
    return 
    

def win_screen():
    """
    Displays the win screen with an option to navigate back to the title screen.

    Parameters:
    None

    Returns:
    None
    """
    pygame.mixer.music.stop()
    WIN.play()
    run = True
    while run:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        game_mouse_pos = pygame.mouse.get_pos()
        # Load buttons
        RETURN = Button(image = pygame.image.load("images/scroll_button.png"), pos = (400, 500), text_input = "TITLE SCREEN", font = get_font(18), base_colour = "#b51f09", hovering_colour = "White")
            
        screen.blit(WIN_SCREEN, (0, 0))

        RETURN.changeColour(game_mouse_pos)
        RETURN.update(screen)
        
        # This block listens for and handles Pygame events, including quitting the game or clicking mouse buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RETURN.checkInput(game_mouse_pos):
                    return

        if (660<mouse_x<685 and 390<mouse_y<415):
            screen.blit(RESIZED_NEXT, (510, 249))
            
        # Update the display
        pygame.display.update()
    return 

def draw_screen(dumpling_positions, photo_positions, questions, level):
    """
    Draws the game screen with all elements, including dumplings, photos, and the current level.

    Parameters:
    - dumpling_positions (list): Positions of dumplings on the screen.
    - photo_positions (list): Positions of photos on the screen.
    - questions (list): The current questions displayed on the photos.
    - level (int): The current level of the player.

    Returns:
    None
    """
    screen.fill(WHITE)
    screen.blit(BACKGROUND, (0, 0))
    # Draw each dumpling
    for pos in dumpling_positions:
        screen.blit(DUMPLING, pos)
    # Draw orders and associated questions
    for i, pos in enumerate(photo_positions):
        screen.blit(ORDER, pos)
        if i < len(questions):
            question_text = questions[i]
            # Adjust text_surface creation to consider the size of the photo
            text_surface = get_font(20).render(question_text[0], True, (0, 0, 0))  # Black text
            # Position text on photo
            text_x_adjustment = 30  # Adjust as needed for leftward movement
            text_y_adjustment = 50  # Adjust as needed for upward movement

            text_x = pos[0] + (PHOTO_SIZE[0] - text_surface.get_width()) // 2 - text_x_adjustment
            text_y = pos[1] + (PHOTO_SIZE[1] - text_surface.get_height()) // 2 - text_y_adjustment
            screen.blit(text_surface, (text_x, text_y))
    
    # Display dumpling count, score, and level
    num_dumplings_text = get_font(20).render(f"Dumplings: {len(dumpling_positions)}", True, (0, 0, 0))
    screen.blit(num_dumplings_text, (26, SCREEN_HEIGHT - 55))
    
    score_text = get_font(20).render(f"Score: {correct_answer}", True, (0, 0, 0))
    screen.blit(score_text, (26, SCREEN_HEIGHT - 95))
        
    level_text = get_font(20).render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(level_text, (26, SCREEN_HEIGHT - 135))
    
    # Update back button and highlight if hovered
    mouse_x, mouse_y = pygame.mouse.get_pos()
    BACK = Button(image="images/back_button.png", pos=(40, 25), text_input="", font=get_font(22), base_colour="White", hovering_colour="#b51f09")
    BACK.update(screen)
            
    if (10<mouse_x<45 and 10<mouse_y<40):
        screen.blit(RESIZED_BACK, (-120,-126))
    
    # Update the display
    pygame.display.flip()


def play_game(username, password):
    """
    Starts and manages the main game loop, handling gameplay, events, and transitions.

    Parameters:
    - username (str): The player's username.
    - password (str): The player's password.

    Returns:
    None
    """
    
    # Initialize player with username and password, and load player data
    player = Player(username, password)
    player.load_player()
    
    # Reset correct answers and number of dumplings to 0
    global correct_answer, number_of_dumplings
    correct_answer = 0
    number_of_dumplings = 0
    
    # Setup game loop condition and game state variables
    done = False
    dumpling_positions = []
    photo_positions = []
    questions = []
    last_photo_time = pygame.time.get_ticks()
    
    # Define the central area for dumpling placement
    central_area = pygame.Rect(
        (SCREEN_WIDTH - SCREEN_WIDTH // 3) // 2, 
        (SCREEN_HEIGHT - SCREEN_HEIGHT // 3) // 2, 
        SCREEN_WIDTH // 3, 
        SCREEN_HEIGHT // 3
    )
    
    # Initialize game level and question count
    total_questions_generated = 0
    level = int(player.get_sub())
    current_question = Question(player)
    
    # Main game loop
    while not done:
        current_time = pygame.time.get_ticks()
        ans = handle_events(dumpling_positions, central_area, questions)
        
        # Wrong answer, show lose screen and exit loop
        if ans == 2: 
            lose_screen(correct_answer, questions[0])
            play_music("sound/CookingGameMusic.mp3")
            done = True
            break
        
        # User requested to exit, leave function
        elif ans == 3:
            return
        
        # Correct answer, game continues
        elif ans == 1 and questions:
            CORRECT.play()
            correct_answer = correct_answer + 1
            questions.pop(0)  # Remove the answered question
            photo_positions.pop(0)  # Remove the corresponding photo
        
        # Update photos on screen if needed
        last_photo_time, photo_added = update_photos(photo_positions, last_photo_time, current_time, total_questions_generated)
        if photo_added and total_questions_generated < 5:
            question_text = current_question.generate_question('-')
            questions.append(question_text)
            total_questions_generated += 1
            
        draw_screen(dumpling_positions, photo_positions, questions, level)
        
        if total_questions_generated >= 5 and not questions:
            questions.append('done')
            # End the game when all 5 questions have been generated and answered
            if correct_answer == 5:
                level = level + 1
                player.update_sub(str(level))
            win_screen()
            play_music("sound/CookingGameMusic.mp3")
            done = True
        
        
        pygame.time.Clock().tick(60)
        pygame.display.flip() # Update the display
    
    return


def cooking_game(username, password):
    """
    Initializes and displays the cooking game start screen, allowing the player to start the game, 
    view instructions, or return to the main menu. This function serves as the entry point to the cooking game, 
    setting up the environment, and managing player interactions with the game's initial options.

    Upon selecting an option, the function either launches the game loop, displays the game instructions, or exits back to the main menu. 
    It also initializes and plays the background music for the start screen.

    Parameters:
    - username (str): The player's username, used for loading and saving player data.
    - password (str): The player's password, used for authentication when loading and saving data.

    Returns:
    None
    """
    play_music("sound/CookingGameMusic.mp3")
    run = True
    while run:
        # display start screen
        screen.blit(START_SCREEN, (0,0))
        mouse_pos = pygame.mouse.get_pos()
        
        # Created buttons
        START_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 250), text_input = "START GAME", font = get_font(22), base_colour = "#b51f09", hovering_colour = "White")
        INSTRUCTION_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 380), text_input = "INSTRUCTIONS", font = get_font(22), base_colour = "#b51f09", hovering_colour = "White")
        RETURN_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 510), text_input = "BACK TO MENU", font = get_font(22), base_colour = "#b51f09", hovering_colour = "White")
        
        # Iterate through the list of buttons: START, INSTRUCTION, and RETURN
        for button in [START_BUTTON, INSTRUCTION_BUTTON, RETURN_BUTTON]:
            button.changeColour(mouse_pos)
            button.update(screen)
        
        # This block listens for and handles Pygame events, including quitting the game or clicking mouse buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if START_BUTTON.checkInput(mouse_pos):
                        play_game(username, password)
                    if INSTRUCTION_BUTTON.checkInput(mouse_pos):
                        instruction()
                    if RETURN_BUTTON.checkInput(mouse_pos):
                        return
        # Update the display
        pygame.display.update()

    # Quit back to the game map
    pygame.mixer.music.stop()
    return