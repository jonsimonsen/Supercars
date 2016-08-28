import pygame, sys, os, math
from pygame.locals import *
from drawable import *
from config import *
from library import *
from precode import Vector2D

class Game(object):
    """A class for running Supercars"""

    def __init__(self):
        """Setting up variables for the game"""

        self._screen = self.makeScreen()    #initialize game window
        self._clock = pygame.time.Clock()   #Initialising game clock(used to make the animation run smoothly)
        self._car = Supercar(Vector2D(int((RES_X - WIDTH) / 2), int((RES_Y - LENGTH) / 2)),
                             Vector2D(0, 0), RED, WIDTH, LENGTH, 180)

        self.run()

    def makeScreen(self):
        """Initializes the pygame display (game window)"""

        #Centering the display on screen (taken from pygame FAQ)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        #Starting pygame and setting up the display(game window)

        pygame.init()
        gamescreen = pygame.display.set_mode((RES_X, RES_Y))
        pygame.display.set_caption(CAPTION)

        return gamescreen

    def run(self):
        """Running the game"""
        while True:
            self._car.update(ROTATION_STEP, SPEEDLIMIT, self._car._keys)

            #clearing the layer and redrawing the background
            pygame.draw.rect(self._screen, LGRAY, (0, 0, RES_X, RES_Y))

            carlayer = rotate_center(self._car._layer,
                                     -(self._car._rotation - CAR_ROTATION))
            self._screen.blit(carlayer, (self._car._pos.x, self._car._pos.y))
            self._clock.tick(FPS)
            pygame.display.update()

            self._car.move()

        return

if __name__ == '__main__':
    game = Game()
