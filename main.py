#!/usr/bin/env python3
import pygame
from collections import namedtuple
from collections.abc import Sequence
from consts import (PIXEL_SIZE, PIXEL)
#from typing import Callable
from widgets import (Button, Entity, Colors, MouseInfo, Point, GameData, States)
from engine import MicroEngine
from random import randrange
#from enum import (auto, Enum)

"""
===============================================================================================
==================================== GAME =====================================================
"""
def _open_image_scaled(file, size):
    """ Opens a image, resizing for the 'size' parameter. """
    return pygame.transform.scale(pygame.image.load(file), size).convert()

class Menu(Entity):
    def __init__(self, screen, font):
        """ Contains the surfaces, widgets and atributes of the Menu. """
        self.width = 600
        self.height = 600
        self.start_button_position = ((self.width/2),(self.height/2)) # Setting 'start_button' position.
        self.start_button_width = 100
        self.start_button_height = 10
        self.start_button = Button(screen, font, "Start", self.start_button_position, "update") # Creating button.
        self._hub_background = _open_image_scaled("images/grass_background_dark.jpg", (self.width, self.height)) # Loading the hub background.

    def reset(self):
        pygame.display.set_caption("Hub") # Naming the screen.

    def process_inputs(self, ctx, mouse, keys):
        self.start_button.process_inputs(ctx, mouse, keys)
    
    def update(self, ctx):
        print('Olá, mundo!')
    
    def draw(self, screen: pygame.Surface, shared):
        self.start_button.draw(screen, shared)
        pygame.display.update()

class SnakeGame(Entity):
    """
        A class representing the snake game.
    """
    def __init__(self) -> None:
        """ It's game itself, contains all surfaces and atributtes. """
        self.width = 600
        self.height = 600
        self.pixels: list[Point] = [] # List of the pixels that represents the snake.
        self._background = _open_image_scaled("images/grass_background_dark.jpg", (self.width, self.height)) # Loading background.
        self._snake_skin = _open_image_scaled("images/snake_skin_2.jpg", PIXEL) # Loading snake skin.
        self._food_skin = _open_image_scaled("images/food_skin.png", PIXEL) # Loading food skin.
        self._score_surface = None
        self._snake_size = 0

    def process_inputs(self, mouse: MouseInfo, keys: Sequence[bool]):
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = Point(0, PIXEL_SIZE)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = Point(0, -PIXEL_SIZE)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed = Point(PIXEL_SIZE, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed = Point(-PIXEL_SIZE, 0)

    def update(self, ctx) -> None:
        """ Update game entities."""
        # Checking if the snake position surpassed the screen limit.
        if self.snake_position.x <= 0:
            self.snake_position = Point(self.width - PIXEL_SIZE, self.snake_position.y)
        elif self.snake_position.x >= self.width:
            self.snake_position = Point(PIXEL_SIZE, self.snake_position.y)
        if self.snake_position.y <= 0:
            self.snake_position = Point(self.snake_position.x, self.height - PIXEL_SIZE)
        elif self.snake_position.y >= self.height:
            self.snake_position = Point(self.snake_position.x, PIXEL_SIZE)
        # End Check.

        self.snake_position = Point(self.snake_position.x + self.speed.x,
                                    self.snake_position.y + self.speed.y) # Tuple that define the snake position.

        # Animation.
        self.pixels.append(self.snake_position)
        if len(self.pixels) > self.snake_size:
            del self.pixels[0]
        # End Animation.

        # Checking snake's collision with itself.
        for pixel in self.pixels[:-1]:
            if pixel == self.snake_position:
                self.reset()
                return
        # End Check.

        # Increasing 1 pixel at the snake, if it's position is tha same as the food's position.
        if self.snake_position == self.food_position:
            self.snake_size += 1
            while True:
                define_food_postion = self._random_position()
                if define_food_postion not in self.pixels: # Preventing that a food spawn on the same pixel as the snake.
                    self.food_position = define_food_postion
                    break
        # End Increment.

    def draw(self) -> None:
        """ Draws necessary entities to the screen. """
        self.screen.blit(self._background, pygame.Rect(0, 0, self.width, self.height)) # Drawing background.
        self.screen.blit(self._food_skin, pygame.Rect(self.food_position, PIXEL)) # Drawing food.

        for pixel in self.pixels:
            self.screen.blit(self._snake_skin, pygame.Rect(pixel, PIXEL)) # Drawing snake.

        self.screen.blit(self._score_surface, (1, 1)) # Drawing score.

        pygame.display.update()

    def reset(self) -> None:
        """ (Re)initializes game entities. """
        pygame.display.set_caption("Snake Game") # Naming the screen.
        self.snake_position = Point(self.width / 2, self.height / 2) # Showing the snake in the center of the screen.
        while True:
            define_food_postion = self._random_position()
            if define_food_postion not in self.pixels: # Preventing that a food spawn on the same pixel as the snake.
                self.food_position = define_food_postion
                break
        self.pixels.clear()
        self.snake_size = 1
        self.speed = Point(0, 0) # Setting the speed at 'x' and 'y' axis as 0. (ta certo, "axis"/"eixo"?)

    @property
    def snake_size(self):
        return self._snake_size
    @snake_size.setter
    def snake_size(self, value):
        # Checking 'self._snake_size's value.
        if self._snake_size != value:
            self._score_surface = self.font.render(
                f'Pontos: {value - 1}', False, Colors.RED) # Shows the score.
        # End Check.

        self._snake_size = value

    def _random_position(self) -> Point:
        """ Returns a tuple containing two random numbers in a interval """
        x = round(randrange((PIXEL_SIZE*2), (self.width-PIXEL_SIZE) - PIXEL_SIZE) / float(PIXEL_SIZE)) * float(PIXEL_SIZE)
        y = round(randrange((PIXEL_SIZE*2), (self.height-PIXEL_SIZE) - PIXEL_SIZE) / float(PIXEL_SIZE)) * float(PIXEL_SIZE)
        return Point(x, y)

# Ensures that 'SnakeGame' class be runned imediatly, if the '__main__' module be imported.
if __name__ == "__main__":
    engine = MicroEngine()
    font = pygame.font.SysFont("Helvetica", 25)
    menu = Menu(engine.screen, font)
    engine.shared = GameData(font=font, states=States(menu, SnakeGame()))
    engine.state = menu
    engine.run()