import pygame
from collections import namedtuple
from collections.abc import Sequence
from typing import Callable
from engine import MicroEngine
from utilities import (Colors, MouseInfo, Point)

class Entity:
    """Represents a generic entity."""
    __slots__ = ()
    def reset(self):
        """(Re)initializes this entity state."""
        pass
    def process_inputs(self, ctx: "MicroEngine", mouse: MouseInfo, keys: Sequence[bool]):
        """Process user inputs.
        ctx: MicroEngine: The micro engine.
        mouse: MouseInfo: Basic mouse information (left, middle, right and position).
        keys: Sequence[bool]: The keyboard state. See `pygame.key.get_pressed` for reference."""
        pass
    def update(self, ctx: "MicroEngine"):
        """Updates this entity state.
        ctx: MicroEngine: The micro engine."""
        pass
    def draw(self, dest: pygame.Surface, shared=None):
        """Draws this entity to a surface.
        dest: Surface: The destination surface to draw this entity.
        shared: Shared data by all entities."""
        pass

GameData = namedtuple("GameData", ("font", "states"))
States = namedtuple("States", ("menu", "game"))
"""Contains shared state data."""

"""
===============================================================================================
=================================== BUTTON ====================================================
"""
class Button(Entity):
    __slots__ = "dest", "font", "position", "_on_click", "_text" # Setting 'Button' slots.
    """Big-Null's Button."""
    def __init__(self, dest: pygame.Surface, font: pygame.font.Font, text: str, position: Point, on_click: Callable[['Button'], None]):
        self.dest = dest
        self.font = font
        self._text = text
        self.position = position
        self._on_click = on_click # Sets the callback.

    def on_click(self):
        self._on_click(self)
    __call__ = on_click

    def process_inputs(self, ctx, mouse, _):
        """ Check the left_mouse_button event, and get the position (x,y) of the click;
            comparing with the 'rect()' (button) position. """
        # Checking button press.
        if mouse.left:
            if (
                # Checking if 'x' and 'y' position is in `position`.
                mouse.x >= self.position.x and mouse.x <= self.position.x + self._rect_size.x and
                mouse.y >= self.position.y and mouse.y <= self.position.y + self._rect_size.y
            ):
                self.on_click() # Calling the function that must be executed after the button press.
        # End of Check.
            
    def draw(self, screen, _=None):
        """ Simple make the button appears in the 'self.dest' position. """
        self.dest.blit(self._text_surface, self.dest)

    """ Getting and Giving text that must be in the button. """
    @property
    def text(self):
        return self._text
    @text.setter # The 'setter' method give the 'text(self, value)' function's instructions to the 'text(self)' property.
    def text(self, value):
        value = value.strip()
        if self._text != value: # Checking if the value of inserted text is different than 'self._text' content.
            self._text_surface = self.font.render(value, False, Colors.WHITE) # Creating text.
            self._rect_size = Point(*self._text_surface.get_size()) # Resizing the 'self._rect_size' to text size.
        self._text = value

def button(dest: pygame.Surface, font: pygame.font.Font, text: str, position: Point):
    """Constructs a button from a callable. The arguments are the same as in Button.__init__."""
    return lambda f: Button(dest, font, text, position, f)