# Import appropriate libraries
import pygame, sys, csv
from Button import Button
from GameMap import load_map
from Player import Player

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

gong = pygame.mixer.Sound("sound/Gong.mp3")

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DIGIT DYNASTY')
BACKGROUND = pygame.image.load("images/background.png")
WELCOME_SCREEN = pygame.image.load("images/Welcome Screen.png")
LOGIN = pygame.image.load("images/login_screen.png")
SIGNUP = pygame.image.load("images/sign_up_screen.png")
HIGH_SCORE = pygame.image.load("images/leaderboard_screen.png")
INSTRUCTIONS = pygame.image.load("images/instructions_screen.png")
BACK = pygame.image.load("images/back_button.png")
RESIZED_BACK = pygame.image.load("images/resized_back.png")
APPLE = pygame.transform.scale(pygame.image.load("images/apple.png"), (60, 60))
RESIZED_APPLE = pygame.transform.scale(pygame.image.load("images/apple.png"), (80, 80))
INSTRUCTOR_DASHBOARD_LOGIN = pygame.image.load("images/Instructor dashboard login.png")
INSTRUCTOR_DASHBOARD = pygame.image.load("images/Instructor dashboard.png")

def get_font(font, size):
    """
    Get the Pygame font object based on the font name and size.

    Parameters:
    - font (str): The name of the font.
    - size (int): The size of the font.

    Returns:
    - pygame.font.Font: The Pygame font object.
    """
    if font == "Sawarabi":
        return pygame.font.Font("fonts/SawarabiMincho-Regular.ttf", size)
    elif font == "Shojumaru":
        return pygame.font.Font("fonts/Shojumaru-Regular.ttf", size)

def input_box(SCREEN, input_rect, text, font, active = False, is_password = False):
    """
    Create an input box on the screen.

    Parameters:
    - SCREEN (pygame.Surface): The Pygame surface to draw on.
    - input_rect (pygame.Rect): The rectangle defining the input box.
    - text (str): The text to display in the input box.
    - font (pygame.font.Font): The font object for the text.
    - active (bool): Whether the input box is active.
    - is_password (bool): Whether the input is for a password (displayed as *).

    Returns:
    None
    """
    colour_active = pygame.Color('black')
    colour_passive = pygame.Color('gray15')
    colour = colour_active if active else colour_passive
    box = pygame.Surface((input_rect.width, input_rect.height), pygame.SRCALPHA)
    box.fill((255, 255, 255, 10))
    SCREEN.blit(box, input_rect.topleft)

    if active:
        pygame.draw.rect(SCREEN, colour, input_rect, 2)

    display_text = ''.join('*' for _ in text) if is_password else text

    text_surface = font.render(display_text, True, pygame.Color('black'))
    text_width, _ = text_surface.get_size()

    if text_width > input_rect.width - 10:
        trim_chars = 0
        for trim_chars in range(len(display_text)):
            partial_text = font.render(display_text[trim_chars:], True, pygame.Color('black'))
            partial_text_width, _ = partial_text.get_size()
            if partial_text_width <= input_rect.width - 10:
                break
        text_surface = font.render(display_text[trim_chars:], True, pygame.Color('black'))

    SCREEN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

def append_to_csv(username, password):
    """
    Append a new player's information to the CSV file.

    Parameters:
    - username (str): The username of the player.
    - password (str): The password of the player.

    Returns:
    None
    """
    name = username
    password = password
    addition = "0"
    subtraction = "0"
    multiplication = "0"
    division = "0"
    bosses = "0"

    # CSV file path
    csv_file = "data.csv"

    # Data row to append
    row = [name, password, addition, subtraction, multiplication, division, bosses]

    # Write to the CSV file
    with open(csv_file, 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def username_exists(username, filepath = "data.csv"):
    """
    Check if a username already exists in the CSV file.

    Parameters:
    - username (str): The username to check.
    - filepath (str): The path to the CSV file.

    Returns:
    - bool: True if the username exists, False otherwise.
    """
    with open("data.csv", newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if username == row[0]:
                return True
    return False

def validate_username(username):
    """
    Validate the format of a username.

    Parameters:
    - username (str): The username to validate.

    Returns:
    - bool: True if the username is valid, False otherwise.
    """
    if not username.isalnum():
        return False
    return True

def validate_password(password):
    """
    Validate the format of a password.

    Parameters:
    - password (str): The password to validate.

    Returns:
    - bool: True if the password is valid, False otherwise.
    """
    if len(password) < 8 or len(password) > 16:
        return False
    if not password.isalnum():
        return False
    return True

def start_game():
    """
    Start the game and handle user input for new player registration.

    Parameters:
    None

    Returns:
    None
    """
    username = ''
    password = ''
    username_active = False
    password_active = False
    existing_player = False
    valid_password = True
    valid_username = True
    no_entry = False
    input_font = get_font("Sawarabi",35)

    username_rect = pygame.Rect(254, 237, 300, 50)
    password_rect = pygame.Rect(254, 378, 300, 50)

    while True:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(SIGNUP, (0, 0))
        
        START_BACK = Button(image = "images/back_button.png", pos = (70, 55), text_input = "", font = get_font("Shojumaru",22), base_colour = "White", hovering_colour = "#b51f09")
        START_BACK.update(SCREEN)

        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))

        input_box(SCREEN, username_rect, username, input_font, active = username_active)
        input_box(SCREEN, password_rect, password, input_font, active = password_active, is_password = True)

        PLAY_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 531), text_input = "PLAY", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BACK.checkInput(GAME_MOUSE_POS):
                    return
                elif PLAY_BUTTON.checkInput(GAME_MOUSE_POS):
                    no_entry = False
                    existing_player = False
                    valid_username = True
                    valid_password = True

                    if username == "" or password == "":
                        no_entry = True
                    elif username_exists(username):
                        existing_player = True
                    elif not validate_username(username):
                        valid_username = False
                    elif not validate_password(password):
                        valid_password = False
                    else:
                        append_to_csv(username, password)
                        gong.play()
                        load_map(username, password)
                        return
                elif username_rect.collidepoint(event.pos):
                    username_active = not username_active
                    password_active = False
                elif password_rect.collidepoint(event.pos):
                    password_active = not password_active
                    username_active = False
                else:
                    username_active = False
                    password_active = False
            if event.type== pygame.KEYDOWN:
                if username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif password_active:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        if no_entry:
            font = get_font('Shojumaru', 13)
            text_surface = font.render('Enter a username and a password.', True, 'white')
            SCREEN.blit(text_surface, (249, 455))
        elif existing_player:
            font = get_font('Shojumaru', 13)
            text_surface = font.render('Existing player. Enter a new username or log in.', True, 'white')
            SCREEN.blit(text_surface, (185, 455))
        elif not valid_username and valid_password:
            font = get_font('Shojumaru', 13)
            text_surface = font.render('Your username can only have letters and/or numbers.', True, 'white')
            SCREEN.blit(text_surface, (160, 455))
        elif not valid_password and valid_username:
            font = get_font('Shojumaru', 13)
            text_surface = font.render('Your password should be 8 - 16 characters and only have letters and/or numbers.', True, 'white')
            SCREEN.blit(text_surface, (45, 455))
        elif not valid_password and not valid_username:
            font = get_font('Shojumaru', 13)
            text_surface = font.render('Error with username and password.', True, 'white')
            SCREEN.blit(text_surface, (249, 455))
        
        PLAY_BUTTON.changeColour(GAME_MOUSE_POS)
        PLAY_BUTTON.update(SCREEN)
        pygame.display.flip()             

def load_player(input_username, input_password):
    """
    Load player information from the data.csv file based on username and password.

    Parameters:
    - input_username (str): The input username.
    - input_password (str): The input password.

    Returns:
    - dict or None: A dictionary containing player information if found, else None.
        Contains:
            - 'Name': The player's username.
            - 'Addition': The player's addition score.
            - 'Subtraction': The player's subtraction score.
            - 'Multiplication': The player's multiplication score.
            - 'Division': The player's division score.
            - 'Bosses': The player's bosses defeated.
    """
    with open("data.csv", newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            username, password = row[0], row[1]

            if username == input_username and password == input_password:
                player_info = {
                    'Name': username,
                    'Addition': row[2],
                    'Subtraction': row[3],
                    'Multiplication': row[4],
                    'Division': row[5],
                    'Bosses': row[6],
                }
                return player_info
    return None

def play_music(file):
    """
    Play background music.

    Parameters:
    - file (str): The path to the music file.

    Returns:
    None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def debug_mode(username, password): 
    """
    Enter debug mode for player skills modification.

    Parameters:
    - username (str): The player's username.
    - password (str): The player's password.

    Returns:
    None
    """
    player = Player(username, password)
    input_font = get_font("Sawarabi", 35)
    
    # input for each box 
    add_input = '0' 
    sub_input = '0' 
    mult_input = '0' 
    div_input = '0' 
    boss_input = '0' 
    
    # check if box is clicked 
    add_active = False 
    sub_active = False 
    mult_active = False 
    div_active = False 
    boss_active = False 
    
    # pos then size 
    add_rect = pygame.Rect(420, 100, 100, 50) 
    sub_rect = pygame.Rect(420, 180, 100, 50) 
    mult_rect = pygame.Rect(420, 260, 100, 50) 
    div_rect = pygame.Rect(420, 340, 100, 50) 
    boss_rect = pygame.Rect(420, 420, 100, 50) 
    
    while True: 
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos() 
        SCREEN.blit(BACKGROUND, (0, 0)) 
        START_BACK = Button(image="images/back_button.png", pos=(70, 55), text_input="", font=get_font("Shojumaru", 22), base_colour="White", hovering_colour="#b51f09") 
        START_BACK.update(SCREEN) 
        
        if (40 < MOUSE_X < 75 and 40 < MOUSE_Y < 70): 
            SCREEN.blit(RESIZED_BACK, (-90, -96)) 
            
        PLAY_BUTTON = Button(image=pygame.image.load("images/scroll_button.png"), pos=(395, 531), text_input="PLAY", font=get_font("Shojumaru", 22), base_colour="#b51f09", hovering_colour="White") 
        subtitles = ["Addition Score:", "Subtraction Score:", "Multiplication Score:", "Division Score:", "Boss Battle Score:"] 
        y_coordinate = 115 
        for i, line in enumerate(subtitles): 
            subtitle_text = get_font('Shojumaru', 20).render(line, True, "white") 
            inputRect = subtitle_text.get_rect() 
            inputRect.right = SCREEN_WIDTH // 2 
            
            # Adjust position for each line 
            inputRect.y = y_coordinate 
            y_coordinate += 80 
            SCREEN.blit(subtitle_text, inputRect) 
            
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.mixer.music.stop() 
                pygame.quit() 
                sys.exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if START_BACK.checkInput(event.pos): 
                    return 
                elif add_rect.collidepoint(event.pos): 
                    add_active = not add_active 
                    sub_active = False 
                    mult_active = False 
                    div_active = False 
                    boss_active = False 
                elif sub_rect.collidepoint(event.pos): 
                    sub_active = not sub_active 
                    add_active = False 
                    mult_active = False 
                    div_active = False 
                    boss_active = False 
                elif mult_rect.collidepoint(event.pos): 
                    mult_active = not mult_active 
                    add_active = False 
                    sub_active = False 
                    div_active = False 
                    boss_active = False 
                elif div_rect.collidepoint(event.pos): 
                    div_active = not div_active 
                    add_active = False 
                    sub_active = False 
                    mult_active = False 
                    boss_active = False 
                elif boss_rect.collidepoint(event.pos): 
                    boss_active = not boss_active 
                    add_active = False 
                    sub_active = False 
                    mult_active = False 
                    div_active = False 
                elif PLAY_BUTTON.checkInput(event.pos): 
                    load_map(username, password) 
                else: 
                    add_active = False 
                    sub_active = False 
                    mult_active = False 
                    div_active = False 
                    boss_active = False 
            if event.type == pygame.KEYDOWN:
                if add_active:
                    if event.key == pygame.K_BACKSPACE:
                        add_input = add_input[:-1]
                    elif event.unicode.isdigit():
                        add_input += event.unicode
                elif sub_active:
                    if event.key == pygame.K_BACKSPACE:
                        sub_input = sub_input[:-1]
                    elif event.unicode.isdigit():
                        sub_input += event.unicode
                elif mult_active:
                    if event.key == pygame.K_BACKSPACE:
                        mult_input = mult_input[:-1]
                    elif event.unicode.isdigit():
                        mult_input += event.unicode
                elif div_active:
                    if event.key == pygame.K_BACKSPACE:
                        div_input = div_input[:-1]
                    elif event.unicode.isdigit():
                        div_input += event.unicode
                elif boss_active:
                    if event.key == pygame.K_BACKSPACE:
                        boss_input = boss_input[:-1]
                    elif event.unicode.isdigit():
                        boss_input += event.unicode
            
        # Update player scores if input is numeric, otherwise set to 0
        player.update_add(add_input if add_input.isdigit() else '0') 
        player.update_sub(sub_input if sub_input.isdigit() else '0') 
        player.update_mul(mult_input if mult_input.isdigit() else '0') 
        player.update_div(div_input if div_input.isdigit() else '0') 
        player.update_bosses(boss_input if boss_input.isdigit() else '0')
        
        input_box(SCREEN, add_rect, add_input, input_font, active=add_active) 
        input_box(SCREEN, sub_rect, sub_input, input_font, active=sub_active) 
        input_box(SCREEN, mult_rect, mult_input, input_font, active=mult_active) 
        input_box(SCREEN, div_rect, div_input, input_font, active=div_active) 
        input_box(SCREEN, boss_rect, boss_input, input_font, active=boss_active) 
        
        PLAY_BUTTON.update(SCREEN) 
        
        pygame.display.update() 

def load_game():
    """
    Load game screen for entering username and password.

    Parameters:
    None

    Returns:
    None
    """
    username = ''
    password = ''
    username_active = False
    password_active = False
    player_not_found = False
    input_font = get_font("Sawarabi",35)

    username_rect = pygame.Rect(254, 237, 300, 50)
    password_rect = pygame.Rect(254, 378, 300, 50)

    while True:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(LOGIN, (0, 0))
        
        LOAD_BACK = Button(image = "images/back_button.png", pos = (70, 55), text_input = "", font = get_font("Shojumaru",22), base_colour = "White", hovering_colour = "#b51f09")
        LOAD_BACK.update(SCREEN)

        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))

        PLAY_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 531), text_input = "PLAY", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOAD_BACK.checkInput(GAME_MOUSE_POS):
                    return
                elif PLAY_BUTTON.checkInput(GAME_MOUSE_POS):
                    player_not_found = False
                    input_username = username
                    input_password = password

                    player_info = load_player(input_username, input_password)

                    if player_info:
                        if input_username == "ADMIN" and input_password == "DD2024":
                            debug_mode(input_username, input_password)
                        else:
                            gong.play()
                            load_map(input_username, input_password)
                        return
                    else:
                        player_not_found = True

                elif username_rect.collidepoint(event.pos):
                    username_active = not username_active
                    password_active = False
                elif password_rect.collidepoint(event.pos):
                    password_active = not password_active
                    username_active = False
                else:
                    username_active = False
                    password_active = False
            if event.type== pygame.KEYDOWN:
                if username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif password_active:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        input_box(SCREEN, username_rect, username, input_font, active = username_active)
        input_box(SCREEN, password_rect, password, input_font, active = password_active, is_password = True)
        
        if player_not_found:
            font = get_font('Shojumaru', 15)
            text_surface = font.render('Player not found. Try again.', True, 'white')
            SCREEN.blit(text_surface, (255, 455))

        PLAY_BUTTON.update(SCREEN)
        pygame.display.flip()

def high_score():
    """
    Display the high score table.

    Parameters:
    None

    Returns:
    None
    """
    # Define constants for layout
    HEADER_SIZE = 17
    SCORE_SIZE = 20
    DETAILS_SIZE = 15
    HEADER_Y = 200
    START_Y = HEADER_Y + 30
    RANK_X = 100
    USERNAME_X = 190
    BOSSES_X = 340
    SKILLS_X = 570
    ROW_HEIGHT = 60

    header_font = get_font("Shojumaru", HEADER_SIZE)
    score_font = get_font("Shojumaru", SCORE_SIZE)
    details_font = get_font("Shojumaru", DETAILS_SIZE)

    black = pygame.Color('black')

    while True:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        MAX_USERNAME_WIDTH = 120

        SCREEN.blit(HIGH_SCORE, (0, 0))

        headers = ["Rank", "Username", "Bosses Defeated", "Skill Levels"]
        header_texts = [header_font.render(header, True, black) for header in headers]
        SCREEN.blit(header_texts[0], (RANK_X, HEADER_Y))
        SCREEN.blit(header_texts[1], (USERNAME_X, HEADER_Y))
        SCREEN.blit(header_texts[2], (BOSSES_X, HEADER_Y))
        SCREEN.blit(header_texts[3], (SKILLS_X, HEADER_Y))

        with open("data.csv", newline = '') as csvfile:
            reader = csv.reader(csvfile)
            player_scores = [(row[0], int(row[6]), int(row[2]), int(row[3]), int(row[4]), int(row[5])) for row in reader]

        sorted_scores = sorted(player_scores, key=lambda x: (-x[1], -sum(x[2:])))

        for i, (name, bosses, addition, subtraction, multiplication, division) in enumerate(sorted_scores[:5]):
            rank_text = score_font.render(str(i + 1), True, black)
            name_surface = score_font.render(name, True, black)
            if name_surface.get_width() > MAX_USERNAME_WIDTH:
                while name_surface.get_width() > MAX_USERNAME_WIDTH:
                    name = name[:-1]
                    name_surface = score_font.render(name + '...', True, black)
                name = name + '...'
            name_text = score_font.render(name, True, black)
            bosses_text = score_font.render(str(bosses), True, black)
            add_sub_text = details_font.render(f" +   {addition}    -  {subtraction}", True, black)
            mul_div_text = details_font.render(f"x   {multiplication}    ÷  {division}", True, black)

            row_y = START_Y + i * ROW_HEIGHT

            SCREEN.blit(rank_text, (RANK_X + 20, row_y))
            SCREEN.blit(name_text, (USERNAME_X + 10, row_y))
            SCREEN.blit(bosses_text, (BOSSES_X + 90, row_y))
            SCREEN.blit(add_sub_text, (SKILLS_X + 25, row_y))
            SCREEN.blit(mul_div_text, (SKILLS_X + 24, row_y + 18))

        SCORE_BACK = Button(image = "images/back_button.png", pos = (70, 55), text_input = "", font = get_font("Shojumaru",15), base_colour = "White", hovering_colour = "#b51f09")
        SCORE_BACK.update(SCREEN)

        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCORE_BACK.checkInput(GAME_MOUSE_POS):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

def instructions():
    """
    Display the instructions screen.

    Parameters:
    None

    Returns:
    None
    """
    while True:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(INSTRUCTIONS, (0, 0))
        
        INSTRUCTIONS_BACK = Button(image = "images/back_button.png", pos = (70, 55), text_input = "", font = get_font("Shojumaru",15), base_colour = "White", hovering_colour = "#b51f09")
        INSTRUCTIONS_BACK.update(SCREEN)

        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkInput(GAME_MOUSE_POS):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

def instructor_dashboard():
    """
    Display the instructor dashboard screen.

    Parameters:
    None

    Returns:
    None
    """
    while True:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(INSTRUCTOR_DASHBOARD, (0, 0))
        
        INSTRUCTIONS_BACK = Button(image = "images/back_button.png", pos = (70, 55), text_input = "", font = get_font("Shojumaru",15), base_colour = "White", hovering_colour = "#b51f09")
        INSTRUCTIONS_BACK.update(SCREEN)

        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRUCTIONS_BACK.checkInput(GAME_MOUSE_POS):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def instructor_dashboard_login():
    """
    Display the login screen for the instructor dashboard.

    Parameters:
    None

    Returns:
    None
    """
    password = ''
    password_active = False
    player_not_found = False
    input_font = get_font("Sawarabi",35)

    password_rect = pygame.Rect(254, 304, 300, 50)

    while True:
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(INSTRUCTOR_DASHBOARD_LOGIN, (0, 0))
        
        LOAD_BACK = Button(image = "images/back_button.png", pos = (70, 55), text_input = "", font = get_font("Shojumaru",22), base_colour = "White", hovering_colour = "#b51f09")
        LOAD_BACK.update(SCREEN)

        if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
            SCREEN.blit(RESIZED_BACK, (-90,-96))

        PLAY_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 531), text_input = "PLAY", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOAD_BACK.checkInput(GAME_MOUSE_POS):
                    return
                if password_rect.collidepoint(event.pos):
                    password_active = not password_active
                else:
                    password_active = False
                if PLAY_BUTTON.checkInput(GAME_MOUSE_POS):
                    player_not_found = False
                    input_password = password

                    if input_password == "ddinstructor123":
                        instructor_dashboard()
                    else:
                        player_not_found = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if password_active:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        input_box(SCREEN, password_rect, password, input_font, active = password_active, is_password = True)
        
        if player_not_found:
            font = get_font('Shojumaru', 15)
            text_surface = font.render('Player not found. Try again.', True, 'white')
            SCREEN.blit(text_surface, (255, 455))

        PLAY_BUTTON.update(SCREEN)
        pygame.display.flip()

def welcome_screen():
    """
    Display the welcome screen.

    Parameters:
    None

    Returns:
    None
    """
    run = True
    while run:
        SCREEN.blit(WELCOME_SCREEN, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        pygame.display.update()

def main_menu():
    """
    Display the main menu screen.
    
    Parameters:
    None
    
    Returns:
    None
    """
    play_music("sound/EDM.mp3")
    welcome_screen()

    while True:
        SCREEN.blit(BACKGROUND, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()

        START_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 75), text_input = "NEW GAME", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")
        LOAD_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 189), text_input = "LOAD GAME", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")
        HIGH_SCORE_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 303), text_input = "HIGH SCORES", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")
        INSTRUCTIONS_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 417), text_input = "INSTRUCTIONS", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")
        EXIT_BUTTON = Button(image = pygame.image.load("images/scroll_button.png"), pos = (395, 531), text_input = "EXIT", font = get_font("Shojumaru",22), base_colour = "#b51f09", hovering_colour = "White")
        TEACHER_BUTTON = Button(image = APPLE, pos = (40, 40), text_input = "", font = get_font("Shojumaru",15), base_colour = "White", hovering_colour = "#b51f09")
                
        for button in [START_BUTTON, LOAD_BUTTON, HIGH_SCORE_BUTTON, INSTRUCTIONS_BUTTON, EXIT_BUTTON, TEACHER_BUTTON]:
            button.changeColour(MENU_MOUSE_POS)
            button.update(SCREEN)

        if (20<MOUSE_X<80 and 20<MOUSE_Y<80):
            SCREEN.blit(RESIZED_APPLE, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkInput(MENU_MOUSE_POS):
                    start_game()
                if LOAD_BUTTON.checkInput(MENU_MOUSE_POS):
                    load_game()
                if HIGH_SCORE_BUTTON.checkInput(MENU_MOUSE_POS):
                    high_score()
                if INSTRUCTIONS_BUTTON.checkInput(MENU_MOUSE_POS):
                    instructions()
                if TEACHER_BUTTON.checkInput(MENU_MOUSE_POS):
                    instructor_dashboard_login()
                if EXIT_BUTTON.checkInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()