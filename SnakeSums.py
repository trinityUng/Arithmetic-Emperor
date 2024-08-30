"""
This module implements the logic and the requirements to run the Snake Sums game using Pygame. It is a game
where the player uses all four arrow keys to move a snake character around the garden map to eat the fruit with the corresponding correct answer.
The game includes a start, instruction, win, loss, and game screen, as well as movement mechanics and the logic for collision detection.
"""
# Import libraries and classes
import pygame
import sys
import random
from Player import Player
from Button import Button
from Question import Question

# Initialize Pygame
pygame.init()

# Initializing screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Creating screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SNAKE SUMS')

# Initialize sounds for game
LOSS = pygame.mixer.Sound("sound/LossSound.mp3")
WIN = pygame.mixer.Sound("sound/LevelComplete.mp3")

# Create dark overlay for question screen
OVERLAY = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
OVERLAY.set_alpha(128)  # Set transparency (0-255)
OVERLAY.fill((0, 0, 0))  # Fill with black

# Load images
BACKGROUND = pygame.image.load("images/snakegamebg.png")
QBOX = pygame.image.load("images/snakegameqbox.png")
INSTRUCTION1 = pygame.image.load("images/additionInstructions.png")
INSTRUCTION2 = pygame.image.load("images/snakeSumsInstructions.png")
BACK = pygame.image.load("images/back_button.png")
RESIZED_BACK = pygame.image.load("images/resized_back.png")
RESIZED_NEXT = pygame.transform.rotate(pygame.image.load("images/resized_back.png"), 180)
START_SCREEN = pygame.image.load("images/snakesumsstart.png")
LOST_SCREEN = pygame.image.load("images/lostscreensnake.png")
WIN_SCREEN = pygame.image.load("images/winscreensnake.png")

# Load fruit images and scale to the right size
FRUIT_SIZE = (50, 50)
BORDER_SIZE = (60, 60)
FRUIT_A = pygame.transform.scale(pygame.image.load("images/orangea.png").convert_alpha(), FRUIT_SIZE)
FRUIT_B = pygame.transform.scale(pygame.image.load("images/orangeb.png").convert_alpha(), FRUIT_SIZE)
FRUIT_C = pygame.transform.scale(pygame.image.load("images/orangec.png").convert_alpha(), FRUIT_SIZE)
FRUIT_D = pygame.transform.scale(pygame.image.load("images/oranged.png").convert_alpha(), FRUIT_SIZE)
FRUIT_BORDER = pygame.transform.scale(pygame.image.load("images/orangeborder.png").convert_alpha(), BORDER_SIZE)

# Clock for controlling game speed
clock = pygame.time.Clock()

# Colors
GOLD3 = (179, 152, 96)
GREEN2 = (153, 216, 196)
GREEN4 = (88, 133, 120)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Snake block size and speed
snake_block = 20
snake_speed = 8

def get_font(size):
    """
    Loads and returns a Pygame font object based on the font file "Shojumaru-Regular.ttf"
    and the given size.

    Parameters:
    - size (int): The size of the font in points.

    Returns:
    - pygame.font.Font: A Pygame font object.
    """
    return pygame.font.Font("fonts/Shojumaru-Regular.ttf", size)

def current_score(score):
    """
    Displays the current score on the screen.

    Parameters:
    - score (int): The current score to display.

    Returns:
    None
    """
    shadow = get_font(25).render("Score: " + str(score), True, GREEN4)
    SCREEN.blit(shadow, [652, 12])  
    main = get_font(25).render("Score: " + str(score), True, WHITE)
    SCREEN.blit(main, [650, 10]) 

def current_level(level):
    """
    Displays the current level on the screen.

    Parameters:
    - level (int): The current level to display.

    Returns:
    None
    """
    shadow = get_font(25).render("Level: " + str(level), True, GREEN4)
    SCREEN.blit(shadow, [502, 12])  
    main = get_font(25).render("Level: " + str(level), True, WHITE)
    SCREEN.blit(main, [500, 10])  

def snake(snake_block, snake_list):
    """
    Draws the snake on the screen.

    Parameters:
    - snake_block (int): The size of each block in the snake.
    - snake_list (list): List of coordinates for each block of the snake.

    Returns:
    None
    """
    for i in snake_list:
        # Draws each rectangle of the snake at the right coordinates
        pygame.draw.rect(SCREEN, GREEN2, [i[0], i[1], snake_block, snake_block])

def time_left(time):
    """
    Displays the time left for the question on the screen.

    Parameters:
    - time (int): The time left for the question.

    Returns:
    None
    """
    shadow = get_font(25).render("Time Left: " + str(time), True, GREEN4)
    SCREEN.blit(shadow, [282, 62])
    main = get_font(25).render("Time Left: " + str(time), True, WHITE)
    SCREEN.blit(main, [280, 60])

def options(correct_ans):
    """
    Generates options for the question.

    Parameters:
    - correct_ans (int): The correct answer to the question.

    Returns:
    - list: A list of four options.
    """
    # Altered by adding a random number
    opt1 = correct_ans + random.randint(1, 5)
    # Altered by subtracting a random number below the answer
    opt2 = correct_ans - random.randint(1, correct_ans-1)
    # Altered by multiplying by a percentage of the answer
    opt3 = int(float(correct_ans) * (10+random.randint(1, 5))//10)
    
    # Changing opt3 if it rounds to a repeat number
    while opt3 == opt2 or opt3 == opt1 or opt3 == correct_ans:  
        opt3 += 1

    opt_list = [opt1, opt2, opt3, correct_ans]

    # Picks out and assigns a random option from the list
    optA = random.choice(opt_list)
    opt_list.remove(optA)
    if optA == correct_ans:
        right_choice = "optA"
    optB = random.choice(opt_list)
    opt_list.remove(optB)
    if optB == correct_ans:
        right_choice = "optB"
    optC = random.choice(opt_list)
    opt_list.remove(optC)
    if optC == correct_ans:
        right_choice = "optC"
    optD = random.choice(opt_list)
    if optD == correct_ans:
        right_choice = "optD"

    # Turn each option into text
    a = get_font(25).render(str(optA), True, BLACK)
    b = get_font(25).render(str(optB), True, BLACK)
    c = get_font(25).render(str(optC), True, BLACK)
    d = get_font(25).render(str(optD), True, BLACK)

    return [a, b, c, d, right_choice]

def instruction1():
    """
    Displays the first instruction screen.

    Parameters:
    None

    Returns:
    None
    """
    run = True
    while run:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(INSTRUCTION1, (0, 0))

        INSTRUCTIONS_BACK = Button(pygame.image.load("images/back_button.png"), pos=(
            70, 55), text_input="", font=get_font(15), base_colour="White", hovering_colour="#b51f09")
        INSTRUCTIONS_NEXT = Button(pygame.transform.rotate(pygame.image.load("images/back_button.png"), 180), pos=(
            680, 475), text_input="", font=get_font(15), base_colour="White", hovering_colour="#b51f09")

        if (40 < MOUSE_X < 75 and 40 < MOUSE_Y < 70):
            SCREEN.blit(RESIZED_BACK, (-90, -96))
        if (690 < MOUSE_X < 705 and 465 < MOUSE_Y < 490):
            SCREEN.blit(RESIZED_NEXT, (540, 324))

        INSTRUCTIONS_BACK.update(SCREEN)
        INSTRUCTIONS_NEXT.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkInput(GAME_MOUSE_POS):
                    run = False
                if INSTRUCTIONS_NEXT.checkInput(GAME_MOUSE_POS):
                    instruction2()
                    run = False

        pygame.display.update()


def instruction2():
    """
    Displays the second instruction screen.

    Parameters:
    None

    Returns:
    None
    """
    run = True
    while run:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(INSTRUCTION2, (0, 0))

        INSTRUCTIONS_BACK = Button(pygame.image.load("images/back_button.png"), pos=(
            70, 55), text_input="", font=get_font(15), base_colour="White", hovering_colour="#b51f09")

        if (40 < MOUSE_X < 75 and 40 < MOUSE_Y < 70):
            SCREEN.blit(RESIZED_BACK, (-90, -96))

        INSTRUCTIONS_BACK.update(SCREEN)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkInput(GAME_MOUSE_POS):
                    run = False

        pygame.display.update()

def fruit_coordinates(x1, y1):
    """
    Create a list of coordinates for the fruit.

    Randomly generates coordinates for 4 fruits with a minimum distance
    between them.

    Parameters:
    - x1 (int): X-coordinate of the snake head.
    - y1 (int): Y-coordinate of the snake head.

    Returns:
    - list: A list of lists, each containing the X and Y coordinates of a fruit.
    """
    # Randomize position of fruits
    fruit_coord = [[x1, y1]]
    i = 0
    min_distance = 100
    while i < 4:
        while True:
            num1 = round(random.randrange(50, SCREEN_WIDTH -
                         (snake_block + 50)) / 10.0) * 10.0
            num2 = round(random.randrange(50, SCREEN_HEIGHT -
                         (snake_block + 50)) / 10.0) * 10.0
            # Check distance from existing coordinates
            too_close = False
            for coord in fruit_coord:
                distance = ((num1 - coord[0]) ** 2 +
                            (num2 - coord[1]) ** 2) ** 0.5
                if distance < min_distance:
                    too_close = True
                    break
            if not too_close:
                break
        fruit_coord.append([num1, num2])
        i += 1
    return fruit_coord

def fruit_eaten(fruit_coord, correct_ans):
    """
    Check if fruit has been eaten by the snake.

    Checks if the snake's head overlaps with any of the fruit coordinates.
    Also checks if the eaten fruit is the correct answer.

    Parameters:
    - fruit_coord (list): A list of lists, each containing the X and Y coordinates of a fruit.
    - correct_ans (str): The letter corresponding to the correct answer among options 'optA', 'optB', 'optC', 'optD'.

    Returns:
    - int: 0 if no action needed, 1 if incorrect answer, 2 if correct answer, 3 if snake hits wall.
    """
    snakex = fruit_coord[0][0]
    snakey = fruit_coord[0][1]
    if correct_ans == "optA":
        answer = 1
    if correct_ans == "optB":
        answer = 2
    if correct_ans == "optC":
        answer = 3
    if correct_ans == "optD":
        answer = 4
    i = 1
    while i < 5:
        if snakex >= (fruit_coord[i][0]-25) and snakex <= (fruit_coord[i][0]+35) and snakey >= (fruit_coord[i][1]-25) and snakey <= (fruit_coord[i][1]+45):
            # if fruit eaten is not the answer
            if i != answer:
                return 1
            # if fruit eaten is the answer
            else:
                return 2
        i += 1
    # if snake hits the wall
    if snakex == 0 or snakex == 800 or snakey == 0 or snakey == 600:
        return 3
    return 0

def end_screen(result):
    """
    Display ending screen based on game result.

    Parameters:
    - result (bool): True for win, False for loss.

    Returns:
    None
    """
    # Play relative sound effects
    if result == False:
        pygame.mixer.init()
        pygame.mixer.music.load("sound/LossSound.mp3")
        pygame.mixer.music.play(0)
    else:
        pygame.mixer.init()
        pygame.mixer.music.load("sound/LevelComplete.mp3")
        pygame.mixer.music.play(0)
    while True:
        MOUSE_POS = pygame.mouse.get_pos()

        if result == True:
            SCREEN.blit(WIN_SCREEN, (0, 0))
            progress_surface = get_font(15).render("Your progress has been saved!", True, "White")
            SCREEN.blit(progress_surface, (240, 440))
        else:
            SCREEN.blit(LOST_SCREEN, (0, 0))

        # Button to return to title screen
        RETURN = Button(image=pygame.image.load("images/scroll_button.png"), pos=(SCREEN_WIDTH / 2, 520),
                        text_input="TITLE SCREEN", font=get_font(18), base_colour="#b51f09", hovering_colour="White")
        RETURN.changeColour(MOUSE_POS)
        RETURN.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RETURN.checkInput(MOUSE_POS):
                    play_music("sound/SnakeSumsMusic.mp3")
                    return

        pygame.display.update()

def response(correct, question, answer):
    """
    Display response screen after answering a question.

    Parameters:
    - correct (bool): True if answer was correct, False otherwise.
    - question (str): The question text.
    - answer (str): The correct answer.

    Returns:
    None
    """
    SCREEN.blit(OVERLAY, (0, 0))
    SCREEN.blit(QBOX, (141, 115))

    shadow = get_font(25).render("Press Space To Continue", True, GREEN4)
    main = get_font(25).render("Press Space To Continue", True, WHITE)
    SCREEN.blit(shadow, [199, 525])
    SCREEN.blit(main, [197, 523])
    
    # Display correct answer
    q = get_font(25).render(question, True, BLACK)
    ans = get_font(25).render("Correct Answer: " + str(answer), True, BLACK)
    SCREEN.blit(q, [328, 308])
    SCREEN.blit(ans, [245, 387])

    if correct == False:
        shadow = get_font(50).render("Nice Try!", True, GREEN4)
        main = get_font(50).render("Nice Try!", True, WHITE)
        SCREEN.blit(shadow, [256, 212])
        SCREEN.blit(main, [256, 210])
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            end_screen(False)
            return True
    else:
        shadow = get_font(50).render("Good Job!", True, GREEN4)
        main = get_font(50).render("Good Job!", True, WHITE)
        SCREEN.blit(shadow, [245, 212])
        SCREEN.blit(main, [243, 210])
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            end_screen(True)
            return True

def correct(question, answer):
    """
    Display screen for correct answer.

    Parameters:
    - question (str): The question text.
    - answer (str): The correct answer.

    Returns:
    None
    """
    shadow = get_font(50).render("Good Job!", True, GREEN4)
    main = get_font(50).render("Good Job!", True, WHITE)
    SCREEN.blit(shadow, [245, 212])
    SCREEN.blit(main, [243, 210])
    q = get_font(25).render(question, True, BLACK)
    ans = get_font(25).render("Correct Answer: " + str(answer), True, BLACK)
    SCREEN.blit(q, [328, 308])
    SCREEN.blit(ans, [245, 387])

def play_music(file):
    """
    Play music during the game.

    Parameters:
    - file (str): The file path of the music file.

    Returns:
    None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def game(user):
    """
    Main game function for Snake Sums, takes care of event handling.

    Runs the game loop, handles gameplay, questions, and user input.

    Parameters:
    - user (Player): The player object containing user information.

    Returns:
    None
    """
    no_run = 1
    done = 0
    result = False
    fruit_delay = 4
    run = True
    pause = True
    snake_pause = True
    level = int(user.get_add())  # get addition level from the user
    select = 0

    # Initialize questions, options, and answer
    currQNA = Question(user).generate_question("+")  # gets question and the answer
    currQ = currQNA[0]
    correct_ans = currQNA[1]
    optionList = options(correct_ans)  # creates list of answer options

    # Initialize change in coordinates
    x1_change = 0
    y1_change = 0

    # List of snake body parts coordinates
    snake_list = []
    snake_len = 1

    # Randomize and create coordinates for each orange
    fruit_coord = fruit_coordinates(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    # Delay the question screen
    elements_delay_counter = 5

    # Adjust counter according to level, 10 seconds for < 5 and 30 seconds otherwise
    if level < 5:
        count_down = 600
        timer_down = 10
    else:
        count_down = 1800
        timer_down = 30

    while run:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        MOUSE_POS = pygame.mouse.get_pos()
        # Event handling, stop run if quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.checkInput(MOUSE_POS):
                  return
                elif FRUIT_AB.checkInput(MOUSE_POS):
                  select = 1
                  pause = False
                elif FRUIT_BB.checkInput(MOUSE_POS):
                  select = 2
                  pause = False
                elif FRUIT_CB.checkInput(MOUSE_POS):
                  select = 3
                  pause = False
                elif FRUIT_DB.checkInput(MOUSE_POS):
                  select = 4
                  pause = False

        # Control snake movement when not paused
        if not pause:
            # Refresh the direction changes if snake was paused
            if snake_pause:
                x1_change = 0
                y1_change = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    snake_pause = False
                    x1_change = -snake_block
                    y1_change = 0
                elif keys[pygame.K_RIGHT]:
                    snake_pause = False
                    x1_change = snake_block
                    y1_change = 0
                elif keys[pygame.K_UP]:
                    snake_pause = False
                    y1_change = -snake_block
                    x1_change = 0
                elif keys[pygame.K_DOWN]:
                    snake_pause = False
                    y1_change = snake_block
                    x1_change = 0
            else:
                # Check for key presses
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    x1_change = -snake_block
                    y1_change = 0
                elif keys[pygame.K_RIGHT]:
                    x1_change = snake_block
                    y1_change = 0
                elif keys[pygame.K_UP]:
                    y1_change = -snake_block
                    x1_change = 0
                elif keys[pygame.K_DOWN]:
                    y1_change = snake_block
                    x1_change = 0

            # Update snake position
            if not snake_pause:
                fruit_coord[0][0] += x1_change
                fruit_coord[0][1] += y1_change

            snake_list.append([fruit_coord[0][0], fruit_coord[0][1]])

            # If snake length exceeds current length, remove the tail
            if len(snake_list) > snake_len:
                del snake_list[0]

        SCREEN.blit(BACKGROUND, (0, 0))
        if elements_delay_counter > 0:
            elements_delay_counter -= 1
            pause = True
        elif no_run == 1:
            # Generate question screen
            if count_down > 0 and pause == True and timer_down > 0 and result is False:
                snake_pause = True
                if count_down == 600:
                    currQNA = Question(user).generate_question("+")
                    currQ = currQNA[0]
                    correct_ans = currQNA[1]
                    optionList = options(correct_ans)
                count_down -= 1
                SCREEN.blit(OVERLAY, (0, 0))
                SCREEN.blit(QBOX, (141, 115))
                time_left(timer_down)
                shadow = get_font(65).render(currQ, True, GOLD3)
                main = get_font(65).render(currQ, True, WHITE)
                if level < 5:
                    SCREEN.blit(shadow, [242, 182])
                    SCREEN.blit(main, [240, 180])
                else:
                    SCREEN.blit(shadow, [202, 182])
                    SCREEN.blit(main, [200, 180])

                shadow = get_font(25).render("Select Your Answer", True, GREEN4)
                main = get_font(25).render("Select Your Answer", True, WHITE)
                SCREEN.blit(shadow, [235, 525])
                SCREEN.blit(main, [233, 523])

                SCREEN.blit(optionList[0], [315, 290])
                SCREEN.blit(optionList[1], [315, 395])
                SCREEN.blit(optionList[2], [505, 290])
                SCREEN.blit(optionList[3], [505, 395])
                SCREEN.blit(FRUIT_A, [245, 280])
                SCREEN.blit(FRUIT_B, [245, 385])
                SCREEN.blit(FRUIT_C, [438, 280])
                SCREEN.blit(FRUIT_D, [438, 385])

                # Hovering effect for each option
                FRUIT_AB = Button(FRUIT_A, pos=(270, 305), text_input="", font=get_font(
                    22), base_colour="White", hovering_colour="#b51f09")
                FRUIT_AB.update(SCREEN)
                FRUIT_BB = Button(FRUIT_B, pos=(270, 410), text_input="", font=get_font(
                    22), base_colour="White", hovering_colour="#b51f09")
                FRUIT_BB.update(SCREEN)
                FRUIT_CB = Button(FRUIT_C, pos=(463, 305), text_input="", font=get_font(
                    22), base_colour="White", hovering_colour="#b51f09")
                FRUIT_CB.update(SCREEN)
                FRUIT_DB = Button(FRUIT_D, pos=(463, 410), text_input="", font=get_font(
                    22), base_colour="White", hovering_colour="#b51f09")
                FRUIT_DB.update(SCREEN)

                if (235 < MOUSE_X < 315 and 260 < MOUSE_Y < 350):
                    SCREEN.blit(FRUIT_BORDER, [240, 275])
                    SCREEN.blit(FRUIT_A, [245, 280])
                elif (235 < MOUSE_X < 315 and 375 < MOUSE_Y < 445):
                    SCREEN.blit(FRUIT_BORDER, [240, 380])
                    SCREEN.blit(FRUIT_B, [245, 385])
                elif (428 < MOUSE_X < 498 and 260 < MOUSE_Y < 350):
                    SCREEN.blit(FRUIT_BORDER, [433, 275])
                    SCREEN.blit(FRUIT_C, [438, 280])
                elif (428 < MOUSE_X < 498 and 375 < MOUSE_Y < 445):
                    SCREEN.blit(FRUIT_BORDER, [433, 380])
                    SCREEN.blit(FRUIT_D, [438, 385])
                if count_down % 10 == 0 and timer_down > 0:
                    timer_down -= 1
                snake_pause = True

            # generate correct screen
            elif result is True:
                SCREEN.blit(OVERLAY, (0, 0))
                SCREEN.blit(QBOX, (141, 115))
                shadow = get_font(25).render(
                    "Press Space To Continue", True, GREEN4)
                main = get_font(25).render(
                    "Press Space To Continue", True, WHITE)
                SCREEN.blit(shadow, [199, 525])
                SCREEN.blit(main, [197, 523])
                correct(currQ, correct_ans)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    result = False
                    fruit_delay = 4
                    count_down = 600
            else:
                pause = False

            # Display game play screen
            if pause == False:
                # Go through delay
                if fruit_delay > 0:
                    fruit_delay -= 1
                else:
                    snake(snake_block, snake_list)
                    current_score(snake_len - 1)
                    current_level(int(user.get_add()))

                    # Display white border below selected option
                    if select == 1:
                        SCREEN.blit(
                            FRUIT_BORDER, ((fruit_coord[1][0]) - 5, (fruit_coord[1][1]) - 5))
                    elif select == 2:
                        SCREEN.blit(
                            FRUIT_BORDER, ((fruit_coord[2][0]) - 5, (fruit_coord[2][1]) - 5))
                    elif select == 3:
                        SCREEN.blit(
                            FRUIT_BORDER, ((fruit_coord[3][0]) - 5, (fruit_coord[3][1]) - 5))
                    elif select == 4:
                        SCREEN.blit(
                            FRUIT_BORDER, ((fruit_coord[4][0]) - 5, (fruit_coord[4][1]) - 5))
                        
                    SCREEN.blit(FRUIT_A, (fruit_coord[1][0], fruit_coord[1][1]))
                    SCREEN.blit(FRUIT_B, (fruit_coord[2][0], fruit_coord[2][1]))
                    SCREEN.blit(FRUIT_C, (fruit_coord[3][0], fruit_coord[3][1]))
                    SCREEN.blit(FRUIT_D, (fruit_coord[4][0], fruit_coord[4][1]))

        done = fruit_eaten(fruit_coord, optionList[4])
        BACK = Button(image="images/back_button.png", pos=(40, 25), text_input="",
                      font=get_font(22), base_colour="White", hovering_colour="#b51f09")
        BACK.update(SCREEN)

        if (10 < MOUSE_X < 45 and 10 < MOUSE_Y < 40):
            SCREEN.blit(RESIZED_BACK, (-120, -126))
        if done == 2:
            # Win game
            if (snake_len - 1) == 4:
                result = False
                update = response(True, currQ, correct_ans)
                elements_delay_counter = 1
                if update == True:
                    new_score = int(user.get_add()) + 1
                    user.update_add(str(new_score))
                    return
            # Play another round below level five
            elif level < 5 and no_run == 1:
                fruit_coord = fruit_coordinates(fruit_coord[0][0], fruit_coord[0][1])
                snake_len += 1
                elements_delay_counter = 1
                fruit_delay = 4
                count_down = 600
                timer_down = 10
                select = 0
                result = True
            # Play another round above level five
            elif no_run == 1:
                fruit_coord = fruit_coordinates(fruit_coord[0][0], fruit_coord[0][1])
                snake_len += 1
                elements_delay_counter = 1
                fruit_delay = 4
                count_down = 1800
                timer_down = 30
                select = 0
                result = True
        # Lose game
        elif done == 1:
            result = False
            no_run = 0
            update = response(False, currQ, correct_ans)
            elements_delay_counter = 1
            if update == True:
                return
        elif done == 3:
            end_screen(False)
            return

        pygame.display.flip()

        clock.tick(snake_speed)

    pygame.quit()

def snake_sums(username, password):
    """
    Initializes and displays the Snake Sums start screen, allowing the player to start the game, 
    view instructions, or return to the main menu. This function serves as the entry point to the game, 
    setting up the environment, and managing player interactions with the game's initial options.

    Upon selecting an option, the function either launches the game loop, displays the game instructions, or exits back to the main menu. 
    It also initializes and plays the background music for the start screen.

    Parameters:
    - username (str): The player's username, used for loading and saving player data.
    - password (str): The player's password, used for authentication when loading and saving data.

    Returns:
    None
    """
    play_music("sound/SnakeSumsMusic.mp3")
    user = Player(name=username, password=password)
    user.load_player()
    # Main game loop
    run = True
    while run:
        # display start screen
        SCREEN.blit(START_SCREEN, (0, 0))
        MOUSE_POS = pygame.mouse.get_pos()

        START_BUTTON = Button(image=pygame.image.load("images/scroll_button.png"), pos=(395, 250),
                              text_input="START GAME", font=get_font(22), base_colour="#b51f09", hovering_colour="White")
        INSTRUCTION_BUTTON = Button(image=pygame.image.load("images/scroll_button.png"), pos=(
            395, 380), text_input="INSTRUCTIONS", font=get_font(22), base_colour="#b51f09", hovering_colour="White")
        RETURN_BUTTON = Button(image=pygame.image.load("images/scroll_button.png"), pos=(395, 510),
                               text_input="BACK TO MENU", font=get_font(22), base_colour="#b51f09", hovering_colour="White")

        for button in [START_BUTTON, INSTRUCTION_BUTTON, RETURN_BUTTON]:
            button.changeColour(MOUSE_POS)
            button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkInput(MOUSE_POS):
                    game(user)
                elif INSTRUCTION_BUTTON.checkInput(MOUSE_POS):
                    instruction1()
                elif RETURN_BUTTON.checkInput(MOUSE_POS):
                    run = False
                    break

        # Update the display
        pygame.display.update()

    # Quit back to the game map
    pygame.mixer.music.stop()
    return