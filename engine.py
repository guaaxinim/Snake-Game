import pygame
from consts import FPS
from utilities import MouseInfo

"""
===============================================================================================
=================================== ENGINE ====================================================
"""
class MicroEngine:
    __slots__ = "_clock", "_state", "playing", "screen", "shared", "screen_width", "screen_height"
    def __init__(self):
        self.playing = False
        self.shared = None
        self._state = None
        pygame.init() # Initializing 'pygame' modules.
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) # Creating screen using 'self.width' and 'self.height' dimensions.
        self._clock = pygame.time.Clock() # Games speed execution; FPS.
    
    def run(self) -> None:
        """ Runs the game loop in a fixed framerate.
        Also handles KeyboardInterrupt and app closing."""
        self.playing = True
        try:
            while self.playing:
                # Checking the QUIT event.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.playing = False
                        return
                # End Check.
                self.state.process_inputs(
                    self,
                    MouseInfo(*pygame.mouse.get_pressed(), *pygame.mouse.get_pos()),
                    pygame.key.get_pressed()
                )
                self.state.update(self)
                self.state.draw(self.screen, self.shared)
                self._clock.tick(FPS)
        except KeyboardInterrupt:   # 'KeyboardInterrupt' prevent something from being "CTRL + C'd" from the terminal.
            self.playing = False # Interrupts the loop, closing the game.  

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value):
        value.reset()
        self._state = value