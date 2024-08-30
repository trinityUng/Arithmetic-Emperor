"""
This module implements the logic and the requirements to run the Game Map. This screen 
displays the player's name, stats, and the temples/buttons to take the user to each 
mini-game. The user is also able to go back to the main menu from here as well.
"""
# Import appropriate libraries
import pygame, sys
from Button import Button
from Player import Player
from RunningArmy import running_army
from SnakeSums import snake_sums
from CookingGame import cooking_game
from SandwichStack import sandwich_stack
from ArithmeticEmperor import arithmetic_emperor

# Initialize Pygame
pygame.init()

# Initialize the base screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DIGIT DYNASTY')

# Initialize the screen backgrounds
BACKGROUND = pygame.image.load("images/Map Screen.png")
LOCK_BACKGROUND = pygame.image.load("images/lock_map_screen.png")

# Initalize smaller assets and features
LEFTTEMP = pygame.image.load("images/templeleft.png")
MULTTEMP = pygame.image.load("images/templeright.png")
TOPTEMP = pygame.image.load("images/templetop.png")
BOTTOMTEMP = pygame.image.load("images/templebottom.png")
MIDDLETEMP = pygame.image.load("images/templemiddle.png")
LOCKBOSS = pygame.image.load("images/lock_boss.png")
RESIZED_LEFTTEMP = pygame.transform.scale(LEFTTEMP, (110, 110))
RESIZED_MULTTEMP = pygame.transform.scale(MULTTEMP, (110, 110))
RESIZED_TOPTEMP = pygame.transform.scale(TOPTEMP, (103, 103))
RESIZED_BOTTOMTEMP = pygame.transform.scale(BOTTOMTEMP, (120, 120))
RESIZED_MIDDLETEMP = pygame.transform.scale(MIDDLETEMP, (150, 150))
RESIZED_LOCKBOSS = pygame.transform.scale(LOCKBOSS, (120, 120))
RESIZED_BACK = pygame.image.load("images/resized_back.png")

def play_music(file):
    """
    Loads and plays a music file in a continuous loop.

    Parameters:
    - file (str): Path to the music file to be played.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def get_font(font, size):
    """
    Loads and returns a Pygame font object based on a given font name and size.

    Parameters:
    - font (str): A string representing the font name. If the font is "Sawarabi" or "Shojumaru", a specific font fle is loaded
    - size (int): The size of the font in points

    Returns:
    A Pygame font object.
    """
    if font == "Sawarabi":
        return pygame.font.Font("fonts/SawarabiMincho-Regular.ttf", size)
    elif font == "Shojumaru":
        return pygame.font.Font("fonts/Shojumaru-Regular.ttf", size)

def load_map(username, password):
  """
  Displays the game map and handles interactions with various elements on it. Based on the player's progress,
  different parts of the map are unlocked. Handles the navigation between different game levels and the main menu.

  Parameters:
  - username (str): The username of the player, used to load and track their progress.
  - password (str): The password of the player, used for verification purposes.

  This function contains the game loop, which continuously checks for events (such as mouse clicks) and updates the display accordingly.
  """
  run = True
  no_entry = False
  while run:
    # Create a new player instance and obtain the current player's information
    player = Player(username, password)
    player.load_player()

    # Create buttons for each temple to take the user ot the respective mini-game
    MULTTEMP = Button(pygame.image.load("images/templeright.png"), pos = (600, 131), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
    TOPTEMP = Button(pygame.image.load("images/templetop.png"), pos = (372, 32), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
    MIDTEMP = Button(pygame.image.load("images/templemiddle.png"), pos = (350, 220), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
    LOCKTEMP = Button(RESIZED_LOCKBOSS, pos = (350, 220), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
    BOTTEMP = Button(RESIZED_MIDDLETEMP, pos = (340, 352), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
    LEFTTEMP = Button(pygame.image.load("images/templeleft.png"), pos = (160, 160), text_input="", font=get_font("Shojumaru", 15), base_colour="White", hovering_colour="#b51f09")

    # Check for events and if the user exits the whole game, exit the system
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return
    
    # Draw the background image onto the screen
    # If the player's ability powers are too low, display the locked middle temple screen
    if int(player.get_add()) >= (int(player.get_bosses()) + 1) * 5 and int(player.get_sub()) >= (int(player.get_bosses()) + 1) * 5 and int(player.get_mul()) >= (int(player.get_bosses()) + 1) * 5 and int(player.get_div()) >= (int(player.get_bosses()) + 1) * 5:
       SCREEN.blit(BACKGROUND, (0, 0))
    else:
      # Otherwise, display the unlocked middle temple screen
       SCREEN.blit(LOCK_BACKGROUND, (0, 0))

    # Get the current mouse position
    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
    MOUSE_POS = pygame.mouse.get_pos()
    
    # Create the back button to return to the main menu
    Back_Button = Button(pygame.image.load("images/back_button.png"), pos = (70, 55), text_input = "", font = get_font("Shojumaru", 15), base_colour = "White", hovering_colour = "#b51f09")
    Back_Button.update(SCREEN)

    # If the user hovers over the back button, resize it and if they click on it, take them back to the main menu
    if (40<MOUSE_X<75 and 40<MOUSE_Y<70):
        SCREEN.blit(RESIZED_BACK, (-90,-96))
        if event.type == pygame.MOUSEBUTTONDOWN:
          if Back_Button.checkInput(MOUSE_POS):
            return
          
    # Logic for the Cooking Game temple
    if (133<MOUSE_X<180 and 139<MOUSE_Y<202):
      SCREEN.blit(RESIZED_LEFTTEMP, (110, 92))
      if event.type == pygame.MOUSEBUTTONDOWN:
         if LEFTTEMP.checkInput(MOUSE_POS):
            pygame.mixer.music.stop()
            cooking_game(username, password)
            play_music("sound/EDM.mp3")

    # Logic for the Snake Game temple
    if (372<MOUSE_X<419 and 32<MOUSE_Y<95):
      SCREEN.blit(RESIZED_TOPTEMP, (348, -2))
      if event.type == pygame.MOUSEBUTTONDOWN:
         if TOPTEMP.checkInput(MOUSE_POS):
            pygame.mixer.music.stop()
            snake_sums(username, password)
            play_music("sound/EDM.mp3")
    
    # Logic for the Running Army temple
    if (600<MOUSE_X<647 and 131<MOUSE_Y<194):
      SCREEN.blit(RESIZED_MULTTEMP, (582, 90))
      if event.type == pygame.MOUSEBUTTONDOWN:
        if MULTTEMP.checkInput(MOUSE_POS):
            pygame.mixer.music.stop()
            running_army(username, password)
            play_music("sound/EDM.mp3")
    
    # Logic for the Sandwich Stack temple
    if (363<MOUSE_X<410 and 383<MOUSE_Y<446):
      SCREEN.blit(RESIZED_BOTTOMTEMP, (340, 352))
      if event.type == pygame.MOUSEBUTTONDOWN:
         if BOTTEMP.checkInput(MOUSE_POS):
            pygame.mixer.music.stop()
            sandwich_stack(username, password)
            play_music("sound/EDM.mp3")
    
    # Logic for the boss battle temple (Arithmetic Emperor)
    # If the player's ability powers are too low, do not allow them to enter the boss battle
    if int(player.get_add()) >= (int(player.get_bosses()) + 1) * 5 and int(player.get_sub()) >= (int(player.get_bosses()) + 1) * 5 and int(player.get_mul()) >= (int(player.get_bosses()) + 1) * 5 and int(player.get_div()) >= (int(player.get_bosses()) + 1) * 5:
      if (350<MOUSE_X<450 and 220<MOUSE_Y<380):
        SCREEN.blit(RESIZED_MIDDLETEMP, (323, 180))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if MIDTEMP.checkInput(MOUSE_POS):
              pygame.mixer.music.stop()
              arithmetic_emperor(username, password)
              play_music("sound/EDM.mp3")
              
    else:
       # Otherwise, let them go into the boss battle
       if (350<MOUSE_X<450 and 220<MOUSE_Y<380):
        SCREEN.blit(RESIZED_LOCKBOSS, (342, 203))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if LOCKTEMP.checkInput(MOUSE_POS):
              no_entry = True

    # Create a new player instance and load their new stats
    player = Player(username, password)
    player.load_player()

    # Logic for displaying the player's information on the screen
    font = get_font("Shojumaru", 18)
    name_surface = font.render(f"{player.get_name()}'s Game", True, "#a6d9db")
    add_surface = font.render(f"Addition: {player.get_add()}", True, "White")
    sub_surface = font.render(f"Subtraction: {player.get_sub()}", True, "White")
    mul_surface = font.render(f"Multiplication: {player.get_mul()}", True, "White")
    div_surface = font.render(f"Division: {player.get_div()}", True, "White")
    SCREEN.blit(name_surface, (580, 485))
    SCREEN.blit(add_surface, (580, 505))
    SCREEN.blit(sub_surface, (580, 525))
    SCREEN.blit(mul_surface, (580, 545))
    SCREEN.blit(div_surface, (580, 565))

    # If the player's stats are too low, display a "no entry" text
    if no_entry:
      font = get_font('Shojumaru', 18)
      text_surface = font.render(f'Your ability powers', True, "White")
      text2_surface = font.render(f'must be level {str((int(player.get_bosses()) + 1) * 5)} to enter.', True, 'white')
      SCREEN.blit(text_surface, (20, 545))
      SCREEN.blit(text2_surface, (20, 565))
    
    # Update the screen
    pygame.display.update()

  pygame.quit()