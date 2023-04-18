from pygame import Rect
from typing import Callable


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
