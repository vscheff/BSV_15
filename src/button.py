from pygame import event, Rect
from pygame.locals import K_BACKSPACE
from typing import Callable

MAX_TEXT_LEN = 8


# Used by the GUI to hold attributes related to in-game menu buttons
# attr   rect - Rect object representing the area of the button
# attr  color - tuple of RGB values representing the color of the button
# attr   text - string to display on top of the button
# attr   func - function to call when the button is pressed
# attr   args - arguments to pass into the button's function
# attr kwargs - keyword arguments to pass into the button's function
class Button:
    def __init__(self, rect: Rect, color: tuple, text: str, func: Callable, args: tuple = (), kwargs: dict = None):
        self.rect = rect
        self.color = color
        self.text = text
        self.func = func
        self.args = args
        self.kwargs = kwargs if kwargs is not None else {}

    # Called when this button is pressed
    def press(self):
        self.func(*self.args, **self.kwargs)


# Used by the GUI to hold attributes related to in-game text boxes
# attr active_color - color for the background of the text box when it is accepting user input
class TextBox(Button):
    def __init__(self, rect: Rect, active_color: tuple, inactive_color: tuple,
                 text: str, func: Callable, args: tuple = (), kwargs: dict = None):

        super().__init__(rect, inactive_color, text, func, args, kwargs)

        self.active_color = active_color

    # Handles key presses when the text box is active
    #  param key_event - KEYUP event
    # return      True - if button needs to be redrawn
    # return     False - if button does not need to be redrawn
    def handle_key(self, key_event: event) -> bool:
        if key_event.key == K_BACKSPACE:
            self.text = self.text[:-1]
            return True

        if len(self.text) == MAX_TEXT_LEN:
            return False

        if (char := key_event.unicode).isnumeric():
            self.text += char
            return True

        return False
