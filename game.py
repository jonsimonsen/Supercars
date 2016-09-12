import pygame, sys, os, math
from pygame.locals import *
from drawable import *
from config import *
from library import *
from precode import Vector2D

#Since several of the methods in the Game class could be used in several games,
#it's an idea to make a base class that this one can inherit from.

class Game(object):
    """A class for running the Supercars game."""

    def __init__(self):
        """Create a new game of Supercars."""

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
        """Make a menu near the center of the screen. Will overwrite previously drawn objects."""

        i = [('laps to go:'), ('fastest:'), ('latest:'), ('total time:')]
        j = [str(self._car._laps), str(self._car._fastestLap), str(self._car._latestLap), str(self._car._totalLap)]

        pygame.draw.rect(self._screen, LGRAY, (MENU_X, MENU_Y, MENU_W, MENU_H))

        textbox = self.makeTextbox('Supercars', BLACK, font = makeFont(FONT, BIGSIZE))
        self._screen.blit(textbox, (MENU_HEAD_X, MENU_HEAD_Y))
        
        item_posx = MENU_HEAD_X + 15
        item_posy = MENU_COL_Y

        for label in i:
            textbox = self.makeTextbox(label, BLACK)
            item_posy += 2 * textbox.get_height()
            self._screen.blit(textbox, (item_posx, item_posy))

        item_posx += 80
        item_posy = MENU_COL_Y

        for info in j:
            textbox = self.makeTextbox(info, WHITE, BLACK)
            item_posy += 2 * textbox.get_height()
            self._screen.blit(textbox, (item_posx, item_posy))            

    def makeFont(self, font, size):
        """Initialize the font for game text.

        font: Type of font.
        size: Size of font.

        returns the font (as a pygame font).
        """

        font = pygame.font.SysFont(font, size)
        return font

    def makeTextbox(self, message, color, bgcolor = None, font = None):
        """Make a textbox displaying message.

        message: A text string to be displayed.
        color: The color to display the text with.
        bgcolor: A color for the textbox. The textbox will be transparent if no color is given.
        font: A font to use in the textbox. Will use the default font for the class if no other font is given.

        returns the textbox as a rendered pygame font.
        """

        if font == None:
            font = self._font
        if bgcolor == None:
            return font.render(message, True, color)
        else:
            return font.render(message, True, color, bgcolor)
        
    def makeGround(self):
        """Makes a (default) track for the game.

        Returns a list of the drawables that the track is made of.
        """

        areas = list()

        #Make asphalt
        areas.append(Circle(300, 300, 300, BLACK))
        areas.append(Rectangle(RES_X - 600, 200, BLACK, 300, 0))
        areas.append(Circle(300, RES_Y - 300, 300, BLACK))
        areas.append(Rectangle(200, RES_Y - 600, BLACK, 0, 300))
        areas.append(Circle(RES_X - 300, RES_Y - 300, 300, BLACK))
        areas.append(Rectangle(RES_X - 600, 200, BLACK, 300, RES_Y - 200))
        areas.append(Circle(RES_X - 300, 300, 300, BLACK))
        areas.append(Rectangle(200, RES_Y - 600, BLACK, RES_X - 200, 300))

        #Make markings
        areas.append(Arc(300, 300, 200 + (MARK_WIDTH / 2), MARK_WIDTH, math.pi / 2, math.pi / 2, MARK_COLOR))
        areas.append(Arc(300, RES_Y - 300, 200 + (MARK_WIDTH / 2), MARK_WIDTH, math.pi, math.pi / 2, MARK_COLOR))
        areas.append(Arc(RES_X - 300, RES_Y - 300, 200 + (MARK_WIDTH / 2), MARK_WIDTH, math.pi * 3 / 2, math.pi / 2, MARK_COLOR))
        areas.append(Arc(RES_X - 300, 300, 200 + (MARK_WIDTH / 2), MARK_WIDTH, 0, math.pi / 2, MARK_COLOR))
        areas.append(Line(RES_X - 320, 100, RES_X - 640, MARK_WIDTH, math.pi, MARK_COLOR))
        areas.append(Line(100, 320, RES_Y - 640, MARK_WIDTH, math.pi / 2, MARK_COLOR))
        areas.append(Line(320, RES_Y - 100, RES_X - 640, MARK_WIDTH, 0, MARK_COLOR))
        areas.append(Line(RES_X - 100, RES_Y - 320, RES_Y - 640, MARK_WIDTH, math.pi * 3 / 2, MARK_COLOR))

        #make grass
        areas.append(Rectangle(RES_X - 600, RES_Y - 400, GREEN, 300, 200))
        areas.append(Rectangle(RES_X - 400, RES_Y - 600, GREEN, 200, 300))
        
        return areas

    def makeObstacles(self):
        """Makes (default) obstacles for the game.

        Returns a list of the drawables representing these obstacles.
        """

        obstacles = list()

        obstacles.append(Circle(300, 300, 100, BLUE))
        obstacles.append(Circle(300, RES_Y - 300, 100, BLUE))
        obstacles.append(Circle(RES_X - 300, RES_Y - 300, 100, BLUE))
        obstacles.append(Circle(RES_X - 300, 300, 100, BLUE))

        return obstacles

    def makeCheckpoints(self):
        """Generate the (default) checkpoints that cars have to cross on each lap.

        Return a list of the checkpoint lines. The first element is supposed to be the start/finish line.
        """

        cp = list()

        cp.append(Line(RES_X / 2, 200, 200, 8, math.pi * 3 / 2, YELLOW))
        cp.append(Line(300, 200, 200, 4, math.pi * 3 / 2, TRANSPARENT))
        cp.append(Line(200, 300, 200, 4, math.pi, TRANSPARENT))
        cp.append(Line(200, RES_Y - 300, 200, 4, math.pi, TRANSPARENT))
        cp.append(Line(300, RES_Y - 200, 200, 4, math.pi / 2, TRANSPARENT))
        cp.append(Line(RES_X - 300, RES_Y - 200, 200, 4, math.pi / 2, TRANSPARENT))
        cp.append(Line(RES_X - 200, RES_Y - 300, 200, 4, 0, TRANSPARENT))
        cp.append(Line(RES_X - 200, 300, 200, 4, 0, TRANSPARENT))
        cp.append(Line(RES_X - 300, 200, 200, 4, math.pi * 3 / 2, TRANSPARENT))

        return cp

    def makeScreen(self):
        """Initializes and returns the pygame display (game window)."""

        #Centering the display on screen (taken from pygame FAQ)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        #Starting pygame and setting up the display(game window)

        pygame.init()
        gamescreen = pygame.display.set_mode((RES_X, RES_Y))
        pygame.display.set_caption(CAPTION)
  
        return gamescreen

    def run(self):
        """Runs the game until there are no laps to go or the user terminates it.

        At a later stage, it would be desirable if the user can decide when the game stops running.
        """

        running = True

        while running:
            running = self._car.update(ROTATION_STEP, SPEEDLIMIT, self._car._keys, self._obstacles, self._checkpoints)
 
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

        #Make sure the user can see the final results
        self._clock.tick(QPS)
        return

if __name__ == '__main__':
    game = Game()
