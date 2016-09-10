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
        self._car = Supercar(Vector2D(int((RES_X - WIDTH) / 2) + 40, 80),
                             Vector2D(0, 0), RED, WIDTH, LENGTH, 180, bgcolor = WHITE)
        self._ground = self.makeGround()
        self._obstacles = self.makeObstacles()
        self._checkpoints = self.makeCheckpoints()
        self._font = self.makeFont(FONT, FONTSIZE)

        self.run()

    def makeMenu(self):
        """Makes a menu near the center of the screen."""

        i = [('laps:'), ('fastest:'), ('latest:'), ('total:')]
        j = [str(self._car._laps), str(self._car._fastestLap), str(self._car._latestLap), str(self._car._totalLap)]

        pygame.draw.rect(self._screen, LGRAY, (RES_X / 2 - 150, RES_Y / 2 - 100, 300, 200))

        textbox = self.makeTextbox('Supercars', BLACK, font = makeFont(FONT, BIGSIZE))
        self._screen.blit(textbox, (RES_X / 2 - 75, RES_Y / 2 - 90))
        
        item_posx = RES_X / 2 - 60
        item_posy = RES_Y / 2 - 80

        for label in i:
            textbox = self.makeTextbox(label, BLACK)
            item_posy += 2 * textbox.get_height()
            self._screen.blit(textbox, (item_posx, item_posy))

        item_posx += 80
        item_posy = RES_Y / 2 - 80

        for info in j:
            textbox = self.makeTextbox(info, WHITE, BLACK)
            item_posy += 2 * textbox.get_height()
            self._screen.blit(textbox, (item_posx, item_posy))            

    def makeFont(self, font, size):
        """Initialize the font for game text"""

        font = pygame.font.SysFont(font, size)
        return font

    def makeTextbox(self, message, color, bgcolor = None, font = None):
        """Make a textbox displaying message"""

        if font == None:
            font = self._font
        if bgcolor == None:
            return font.render(message, True, color)
        else:
            return font.render(message, True, color, bgcolor)
        
    def makeGround(self):
        """Makes a track for the game."""

        areas = list()

        #Make asphalt
        #lines.append((RES_X - 300, 100, RES_X - 600, 200, math.pi, BLACK))
        #lines.append(Arc(300, 300, 300, 200, math.pi / 2, math.pi / 2, BLACK))
        areas.append(Circle(300, 300, 300, BLACK))
        areas.append(Rectangle(RES_X - 600, 200, BLACK, 300, 0))
        #lines.append(Line(100, 300, RES_Y - 600, 200, math.pi / 2, BLACK))
        #lines.append(Arc(300, RES_Y - 300, 300, 200, math.pi, math.pi / 2, BLACK))
        areas.append(Circle(300, RES_Y - 300, 300, BLACK))
        areas.append(Rectangle(200, RES_Y - 600, BLACK, 0, 300))
        #lines.append(Line(300, RES_Y - 100, RES_X - 600, 200, 0, BLACK))
        #lines.append(Arc(RES_X - 300, RES_Y - 300, 300, 200, math.pi * 3 / 2, math.pi / 2, BLACK))
        areas.append(Circle(RES_X - 300, RES_Y - 300, 300, BLACK))
        areas.append(Rectangle(RES_X - 600, 200, BLACK, 300, RES_Y - 200))
        #lines.append(Line(RES_X - 100, RES_Y - 300, RES_Y - 600, 200, math.pi * 3 / 2, BLACK))
        #lines.append(Arc(RES_X - 300, 300, 300, 200, 0, math.pi / 2, BLACK))
        areas.append(Circle(RES_X - 300, 300, 300, BLACK))
        areas.append(Rectangle(200, RES_Y - 600, BLACK, RES_X - 200, 300))

        #make grass
        areas.append(Rectangle(RES_X - 600, RES_Y - 400, GREEN, 300, 200))
        areas.append(Rectangle(RES_X - 400, RES_Y - 600, GREEN, 200, 300))
        
        return areas

    def makeObstacles(self):
        """Makes obstacles for the game."""

        obstacles = list()

        obstacles.append(Circle(300, 300, 100, BLUE))
        obstacles.append(Circle(300, RES_Y - 300, 100, BLUE))
        obstacles.append(Circle(RES_X - 300, RES_Y - 300, 100, BLUE))
        obstacles.append(Circle(RES_X - 300, 300, 100, BLUE))

        return obstacles

    def makeCheckpoints(self):
        """Generate the checkpoints that cars have to cross on each lap."""

        cp = list()

        cp.append(Line(RES_X / 2, 200, 200, 10, math.pi * 3 / 2, WHITE))
        cp.append(Line(300, 200, 200, 4, math.pi * 3 / 2, YELLOW))
        cp.append(Line(200, 300, 200, 4, math.pi, YELLOW))
        cp.append(Line(200, RES_Y - 300, 200, 4, math.pi, YELLOW))
        cp.append(Line(300, RES_Y - 200, 200, 4, math.pi / 2, YELLOW))
        cp.append(Line(RES_X - 300, RES_Y - 200, 200, 4, math.pi / 2, YELLOW))
        cp.append(Line(RES_X - 200, RES_Y - 300, 200, 4, 0, YELLOW))
        cp.append(Line(RES_X - 200, 300, 200, 4, 0, YELLOW))
        cp.append(Line(RES_X - 300, 200, 200, 4, math.pi * 3 / 2, YELLOW))

        return cp

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
            self._car.update(ROTATION_STEP, SPEEDLIMIT, self._car._keys, self._obstacles, self._checkpoints)
 
            #clearing the layer and redrawing the background
            pygame.draw.rect(self._screen, LGRAY, (0, 0, RES_X, RES_Y))

            carlayer = rotate_center(self._car._layer,
                                     -(self._car._rotation - CAR_ROTATION))
            for area in self._ground:
                area.draw(self._screen)
            for thing in self._obstacles:
                thing.draw(self._screen)
            for cp in self._checkpoints:
                cp.draw(self._screen)

            self.makeMenu()
                
            self._screen.blit(carlayer, (self._car._pos.x, self._car._pos.y))
            self._clock.tick(FPS)
            pygame.display.update()

            self._car.move()

        return

if __name__ == '__main__':
    game = Game()
