#Imports

##External
import pygame, sys, os, math, time
from pygame.locals import *
from precode import Vector2D

##General methods
from library import *

##Classes and global constants
from supercar import *
from drawable import *
from drawconf import *
from config import *

#Since several of the methods in the Game class could be used in several games,
#it's an idea to make a base class that this one can inherit from.

class Game(object):
    """A class for running the Supercars game."""

    def __init__(self):
        """Create a new game of Supercars."""

        self._player = self._makePlayer()           #Prompt the user for a name
        self._track = DEF_TRACK                     #Using a default track until the game gets more advanced
        self._makeTrack()
        self._screen = self._makeScreen()           #Initialize game window
        self._clock = pygame.time.Clock()           #Initialising game clock(used to make the animation run smoothly)
        
        #self._ground = self._makeGround()           #Create background
        self._obstacles = self._makeObstacles()     #Create obstacles
        self._checkpoints = self._makeCheckpoints() #Create checkpoints
        self._font = makeFont(FONT, FONTSIZE)       #Create a standard font

        #Make a car for the player
        keys = self._makeControls()
        self._car = Supercar(Vector2D(int(RES_X / 2 + WIDTH), int((ROAD_WIDTH - WIDTH) / 2)),
                             Vector2D(0, 0), SPEEDLIMIT, RED, WIDTH, LENGTH, Rectangle(RES_X, RES_Y, TRANSPARENT),
                             keys, CAR_ROTATION, bgcolor = WHITE)

        self.run()  #Run the game

    def _makePlayer(self):
        """Prompts the player for a name, and returns it. Does not support names longer than 16 characters."""

        name = input('Please enter your name (max. %d characters):' % MAX_NAMELEN)

        #If the name is too long, discard the last part
        if len(name) > MAX_NAMELEN:
            name = name[:MAX_NAMELEN]
        elif len(name) < 1:
            name = DEF_NAME

        print('Welcome, %s' % name)
        time.sleep(DISPLAY_DELAY)
        return name

    def _makeScreen(self):
        """Initializes and returns the pygame display (game window)."""

        #Centering the display on screen (taken from pygame FAQ)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        #Starting pygame and setting up the display(game window)

        pygame.init()
        gamescreen = pygame.display.set_mode((RES_X, RES_Y))
        pygame.display.set_caption(CAPTION)
  
        return gamescreen

    def _makeTrack(self):
        """Makes the track by reading it from file."""

        fileName = 'Tracks/' + self._track + '.txt'
        trackFile = open(fileName)
        line = ''

        while(line[:8] != '#asphalt'):
            line = trackFile.readline()

        acolor = eval(trackFile.readline().rstrip())
        nextLine = trackFile.readline()
        areas = list()
        alen = Vector2D(0, 0)
        awid = 0

        while(nextLine[:6] != '#marks'):
            elems = list(filter(None, nextLine.split('\t')))
            if elems:
                if elems[0] == 'C':
                    print(elems[1], elems[2], elems[3])
                    areas.append(Circle(eval(elems[1]), eval(elems[2]), int(elems[3]), acolor))
                elif elems[0] == 'R':
                    areas.append(Rectangle(eval(elems[1]), eval(elems[2]), acolor, eval(elems[3]), eval(elems[4])))
                elif elems[0][0] == 'L':
                    llen = alen.shiftQuadrant(int(elems[0][1]))
                    lscale = (aoff + (awid / 2)) / llen.magnitude()
                    if elems[0][2] == 'l':
                        dx = -(llen.y * lscale)
                        dy = llen.x * lscale
                    elif elems[0][2] == 'r':
                        dx = llen.y * lscale
                        dy = -(llen.x * lscale)
                    else:
                        pass
                    areas.append(Line(eval(elems[1]) + dx, eval(elems[2]) + dy, llen.magnitude(), awid, llen.getAngle(), acolor))
                elif elems[0] == 'len':
                    alen = Vector2D(eval(elems[1]), eval(elems[2]))
                elif elems[0] == 'wid':
                    awid = int(elems[1])
                elif elems[0] == 'off':
                    aoff = int(elems[1])
                else:
                    #Should throw some exception/error
                    pass
            nextLine = trackFile.readline()

        mcolor = eval(trackFile.readline().rstrip())
        mwidth = eval(trackFile.readline().rstrip())
        nextLine = trackFile.readline()

        while(nextLine[:6] != '#grass'):
            elems = list(filter(None, nextLine.split('\t')))
            if elems:
                if elems[0] == 'A':
                    print(elems[1], elems[2], elems[3], elems[4], elems[5])
                    areas.append(Arc(eval(elems[1]), eval(elems[2]), int(elems[3]) + mwidth / 2, mwidth, int(elems[4]) * math.pi / 2,
                                     int(elems[5]) * math.pi / 2, mcolor))
                elif elems[0] == 'L':
                    areas.append(Line(eval(elems[1]), eval(elems[2]), eval(elems[3]), mwidth, int(elems[4]) * math.pi / 2, mcolor))
                else:
                    #error/exception
                    pass

            nextLine = trackFile.readline()

        gcolor = eval(trackFile.readline().rstrip())
        nextLine = trackFile.readline()

        while(nextLine[:10] != '#obstacles'):
            elems = list(filter(None, nextLine.split('\t')))
            if elems:
                if elems[0] == 'R':
                    areas.append(Rectangle(eval(elems[1]), eval(elems[2]), gcolor, int(elems[3]), int(elems[4])))
                else:
                    #error/exception
                    pass

            nextLine = trackFile.readline()

        self._ground = areas

        #Make obstacles and checkpoints...
        
        trackFile.close()

    def _makeGround(self):
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

        #Make grass
        areas.append(Rectangle(RES_X - 600, RES_Y - 400, GREEN, 300, 200))
        areas.append(Rectangle(RES_X - 400, RES_Y - 600, GREEN, 200, 300))
        
        return areas

    def _makeObstacles(self):
        """Makes (default) obstacles for the game.

        Returns a list of the drawables representing these obstacles.
        """

        obstacles = list()

        obstacles.append(Circle(300, 300, 100, BLUE))
        obstacles.append(Circle(300, RES_Y - 300, 100, BLUE))
        obstacles.append(Circle(RES_X - 300, RES_Y - 300, 100, BLUE))
        obstacles.append(Circle(RES_X - 300, 300, 100, BLUE))
        obstacles.append(Circle(MID_X, RES_Y - 300, 100, BLUE))

        return obstacles

    def _makeCheckpoints(self):
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

    def _makeControls(self):
        """Generates a list containing the keys the player can use (as a tuple).

        First element is a surface supposed to hold a key image.
        Second element is text to accompany the image.
        Third element is a pygame key constant for the corresponding key.
        
        Returns the list of tuples.
        """

        return ([(IMAGE, KEYTEXT[0], pygame.K_LEFT),
                 (IMAGE, KEYTEXT[1], pygame.K_RIGHT),
                 (IMAGE, KEYTEXT[2], pygame.K_UP)])

    def makeMenu(self):
        """Make a menu near the center of the screen. Will overwrite previously drawn objects."""

        #Lists of output
        i = [('laps to go:'), ('fastest:'), ('latest:'), ('total time:')]
        j = [str(self._car._laps), str(framesToSec(self._car.getFastestLap(), FPS)),
             str(framesToSec(self._car.getLatestLap(), FPS)), str(framesToSec(self._car.getTotalLap(), FPS))]

        #Draw a background and a header for the menu
        pygame.draw.rect(self._screen, LGRAY, (MENU_X, MENU_Y, MENU_W, MENU_H))
        textbox = self.makeTextbox(CAPTION, BLACK, font = makeFont(FONT, BIGSIZE))
        self._screen.blit(textbox, (MENU_HEAD_X, MENU_HEAD_Y))

        #Left column
        item_posx = MENU_COL_X
        item_posy = MENU_COL_Y

        for label in i:
            textbox = self.makeTextbox(label, BLACK)
            item_posy += 2 * textbox.get_height()
            self._screen.blit(textbox, (item_posx, item_posy))

        #Right column
        item_posx += COLSPAN
        item_posy = MENU_COL_Y

        for info in j:
            textbox = self.makeTextbox(info, WHITE, BLACK)
            item_posy += 2 * textbox.get_height()
            self._screen.blit(textbox, (item_posx, item_posy))            

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
        
    def run(self):
        """Runs the game until there are no laps to go or the user terminates it.

        At a later stage, it would be desirable if the user can decide when the game stops running.
        """

        running = True

        while running:
            running = self._car.update(ROTATION_STEP, self._obstacles, self._checkpoints)
 
            #clearing the layer and redrawing the background
            pygame.draw.rect(self._screen, LGRAY, (0, 0, RES_X, RES_Y))

            #Drawing the foreground/objects
            for area in self._ground:
                area.draw(self._screen)
            for thing in self._obstacles:
                thing.draw(self._screen)
            for cp in self._checkpoints:
                cp.draw(self._screen)

            self.makeMenu()
            self._car.draw(self._screen)

            #Wait for a while before updating the display window.
            self._clock.tick(FPS)
            pygame.display.update()

        self._updateScores()

        #Make sure the user can see the final results
        self._clock.tick(QPS)
        return

    def _updateScores(self):
        """Update high score lists if necessary."""

        candidate = self._car.getTotalLap()
        pos = 0
        lines = list()
        filename = 'Tracks/' + self._track + '_hi.txt'
        readFile = open(filename)

        for line in readFile:
            if candidate >= int(line.split()[0]):
                pos += 1
            lines.append(line)
            print('-' + line + '-')

        if pos < MAX_SCORES:
            lines.insert(pos, '{:6d} {:s}\n'.format(candidate, self._player))

        self._showScores(lines, pos)
        readFile.close()

        #Write scores to the files
        writeFile = open(filename, 'w')

        for line in lines[:10]:
            writeFile.write(line)

        writeFile.close()

    def _showScores(self, lines, pos):
        """Show the high scores.

        lines: A list of lines that contain highscores with a given format.
        pos: The position of a new score (if none, this should be equal to MAX_SCORES)

        The first element in the line, should be the total number of frames.
        The second should be the name of the player.
        """

        #Draw a background and a header for the menu
        pygame.draw.rect(self._screen, LGRAY, (MENU_X, MENU_Y, MENU_W, MENU_H))
        textbox = self.makeTextbox((SCORE_CAPT + self._track + ':'), BLACK)
        self._screen.blit(textbox, (MENU_HEAD_X, MENU_HEAD_Y))
        count = 0
        for line in lines[:10]:
            frames = line[0:6]
            name = line[7:23].rstrip()
            
            if count == pos:
                leftbox = self.makeTextbox(name, YELLOW, BLACK)
                rightbox = self.makeTextbox('{:5.2f}'.format(framesToSec(int(frames), FPS)), YELLOW, BLACK)
            else:
                leftbox = self.makeTextbox(name, WHITE, BLACK)
                rightbox = self.makeTextbox('{:5.2f}'.format(framesToSec(int(frames), FPS)), WHITE, BLACK)
                
            self._screen.blit(leftbox, (MENU_COL_X, MENU_COL_Y + (count + 1) * int(1.2 * textbox.get_height())))
            self._screen.blit(rightbox, (MENU_COL_X + COLSPAN, MENU_COL_Y + (count + 1) * int(1.2 * textbox.get_height())))
            count += 1
        pygame.display.update()

if __name__ == '__main__':
    game = Game()
