from pygame import Rect
from typing import Callable

class Button:
    def __init__(self, rect: Rect, color: tuple, text: str, func: Callable, *args, **kwargs):
        self.rect = rect
        self.color = color
        self.text = text
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def press(self):
        self.func(*self.args, **self.kwargs)


