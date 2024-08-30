"""
This module implements the logic and the requirements to create buttons.
"""
# Import appropriate libraries
import pygame

class Button():
    """
    A class to create interactive buttons with Pygame. Supports both text and image-based buttons.

    Attributes:
    - image (pygame.Surface or None): The image for the button. If None, a text-based button is created.
    - pos (tuple): The position of the button (x, y).
    - text_input (str): The text displayed on the button. Ignored if an image is provided.
    - font (pygame.font.Font): The font used for the button's text.
    - base_colour (str): The base colour of the button's text.
    - hovering_colour (str): The colour of the button's text when hovered over.
    """
    def __init__(self, image = None, pos = (0,0), text_input = "", font = 0, base_colour = "Black", hovering_colour = "White"):
        """
        Initializes the Button object.

        Parameters:
        - image (pygame.Surface or None): The image for the button. Optional; defaults to None.
        - pos (tuple): The position of the button (x, y).
        - text_input (str): The text displayed on the button. Ignored if an image is provided.
        - font (pygame.font.Font): The font used for the button's text.
        - base_colour (str): The base colour of the button's text.
        - hovering_colour (str): The colour of the button's text when hovered over.
        """
        # Check if a path to an image has been given
        if isinstance(image, str):
            self.image = pygame.image.load(image) # Load the image
        # Otherwise, no image path was given
        else:
            # Not a string, directly assign it to "self.image"
            self.image = image
        self.x_pos, self.y_pos = pos            # Obtain the x and y coordinates of the button's position
        self.font = font                        # Obtain the font for the button
        self.base_colour, self.hovering_colour = base_colour, hovering_colour # Obtain the base and hovering colours of the text
        self.text_input = text_input            # Obtain the text input
        # If a font was given then render the text
        if self.font:
            self.text = self.font.render(self.text_input, True, pygame.Color(self.base_colour))
        else:
            # Otherwise, no text will be displayed on the button
            self.text = None
        # If there is no image
        if self.image is None:
            self.image = self.text # Render the text to be used as a button
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos)) # Create a rectangle around the image

    def update(self, SCREEN):
        """
        Draws the button (and its text, if applicable) onto the given surface.

        Parameters:
        - SCREEN (pygame.Surface): The surface on which to draw the button.
        """
        # Check if an image was given for the button
        if self.image is not None:
            # If yes, then place it on the screen
            SCREEN.blit(self.image, self.rect)
        if self.text:
            # If there is text, then place it on the screen
            text_rect = self.text.get_rect(center = self.rect.center)
            SCREEN.blit(self.text, text_rect)

            # Shadow offset
            shadow_offset = 2

            # Draw shadow first
            shadow_color = (135, 135, 135)  # Black shadow
            # Place the text with the shadow on the screen
            shadow_text = self.font.render(self.text_input, True, shadow_color)
            shadow_rect = shadow_text.get_rect(center=(self.rect.centerx + shadow_offset, self.rect.centery + shadow_offset))
            SCREEN.blit(shadow_text, shadow_rect)

            # Draw the actual text
            SCREEN.blit(self.text, text_rect)

    def checkInput(self, position):
        """
        Checks if the given position collides with the button.

        Parameters:
        - position (tuple): The (x, y) position to check.

        Returns:
        - bool: True if the position collides with the button, False otherwise.
        """
        # Check if the mouse collides with the button
        return self.rect.collidepoint(position)
    
    def changeColour(self, position):
        """
        Changes the button's text colour based on the hover state.

        Parameters:
        - position (tuple): The (x, y) position used to determine hover state.
        """
        # If the mouse hovers over the button
        if self.rect.collidepoint(position):
            if self.font:
                # Change the colour of the button
                self.text = self.font.render(self.text_input, True, pygame.Color(self.hovering_colour))
            else:
                # If it not overing, keep it at the base colour
                if self.font:
                    self.text = self.font.render(self.text_input, True, pygame.Color(self.base_colour))