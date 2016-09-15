#Imports

##External
import pygame, math
from precode import Vector2D, intersect_rectangle_line

##General methods
from library import *

##Classes and global constants
from drawable import *
from drawconf import *

class Supercar(Rectangle, MovingObject):
    """A supercar (moving sprite on a layer)."""

    def __init__(self, pos, speed, speedlimit, color, width, length, room, keys, rotation = 0,
                 wcolor = BLACK, bgcolor = TRANSPARENT):
        """Create a supercar.

        pos:        A vector2D object pointing to the upper left corner of the
                    layer the car is going to be drawn onto.
        speed:      A Vector2D object representing the car's velocity.
        speedlimit: The maximum magnitude allowable for the car's velocity.
        color:      The color of the rectangle representing the car's body.
        width:      The width of the car (must be less than length).
        length:     The length of the car (and dimension of its surface).
        room:       A rectangle that is supposed to contain the supercar.
        keys:       list of lists where the third element (index 2) needs to be a
                    pygame key constant corresponding to a legal input from the player.
        rotation:   The direction the car is pointing in degrees. 0 means right,
                    and positive numbers signifies clockwise rotation.
        wcolor:     The color of the car's wheels.
        bgcolor:    Background color of the surface the car is drawn onto.
        """

        if(width >= length):
            print("The supercar must have a height(length) greater than its width.")
        Rectangle.__init__(self, length, length, color, pos.x, pos.y)

        self._width = width
        self._velocity = speed
        self._maxSpeed = speedlimit
        self._setRoom(room)
        self._rotation = rotation
        self._noRotation = rotation     #To keep track of the initial rotation
        self._wcolor = wcolor
        self._bgcolor = bgcolor
        
        self._layer = self._makeLayer()
        self._keys = keys        
        self._thrust = False
        self._leftTurn = False
        self._rightTurn = False
        
        self._running = False       #Wait for the player to start moving before starting the clock
        self._laps = 3              #Laps to go
        self._lastCP = -1           #Index of latest checkpoint
        self._frames = 0            #Number of frames for this lap
        self._fastestLap = 0        #Fastest lap time
        self._latestLap = 0         #Latest lap time
        self._totalLap = 0          #Total lap time

    def getFastestLap(self):
        """Getter for _fastestLap."""
        return self._fastestLap

    def getLatestLap(self):
        """Getter for _latestLap."""
        return self._latestLap

    def getTotalLap(self):
        """Getter for _totalLap."""
        return self._totalLap

    def _setRoom(self, room):
        """Set the car's _room attribute. Should only be called from __init__.

        room: A rectangle object that represents a room the car should be contained in.

        Raises a TypeError if the argument is not a Rectangle.
        """
        
        if not isinstance(room, Rectangle):
            raise TypeError("Argument error. room must be an object of the Rectangle class.")
        else:
            self._room = room

    def _makeLayer(self):
        """Generates a surface with the supercar drawn onto it.

        Returns the surface.
        """

        surface = pygame.Surface((self._w, self._h)).convert_alpha()
        surface.fill(self._bgcolor)
        self._drawWheels(surface)
        self._drawBody(surface)

        return surface

    def _drawWheels(self, layer):
        """Draws wheels.

        layer: The surface being drawn to.
        """

        offset = self._w / 5
        width = self._w / 6
        border = self._h / 8  #To prevent the car from being misshaped when being rotated on the layer

        pygame.draw.rect(layer, self._wcolor, (offset, border, width, self._h - 2 * border))
        pygame.draw.rect(layer, self._wcolor, (self._w - (offset + width), border, width, self._h - 2 * border))

    def _drawBody(self, layer):
        """Draws the car's body.

        layer: The surface being drawn to.
        """

        offset = self._h / 5
        border = self._w / 8  #To prevent the car from being misshaped when being rotated on the layer

        pygame.draw.rect(layer, self._color, (border, offset, self._w - 2 * border, self._h - 2 * offset))

    def draw(self, layer):
        """Draws the car (actually draws the car's layer onto another layer).

        layer: Layer to draw the car onto.
        """

        carlayer = rotate_center(self._layer, self._noRotation - self._rotation)
        layer.blit(carlayer, (self._pos.x, self._pos.y))

    def checkpoint(self, points):
        """Handles intersection between the car and a checkpoint.

        points: A list of checkpoints that the car must cross in chronological order on every lap.

        The method keeps the attributes _latestLap, _fastestLap, _totalLap and _laps updated.
        It resets the attribute _frames when crossing the first checkpoint,
        and updates _lastCP when crossing any checkpoint.
        """

        if self._lastCP < 0:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[0]._pos, points[0]._length, points[0]._angle):
                self._lastCP = 0
                self._totalLap = self._frames
                self._frames = 0
        elif self._lastCP == len(points) - 1:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[0]._pos, points[0]._length, points[0]._angle):
                self._laps -= 1
                self._lastCP = 0
                self._latestLap = self._frames
                if self._fastestLap <= 0 or self._latestLap < self._fastestLap:
                    self._fastestLap = self._latestLap
                self._totalLap += self._latestLap
                self._frames = 0
        else:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[self._lastCP + 1]._pos, points[self._lastCP + 1]._length,
                                        points[self._lastCP + 1]._angle):
                self._lastCP += 1

        #for i in range(len(points)):
        #    if intersect_rectangle_line(self._pos, self._w, self._h,
        #                                points[i]._pos, points[i]._length, points[i]._angle):
        #        print(str(i))

    def update(self, anglespeed, obstacles, checkpoints):
        """Updates the car's attributes based on user input and other objects.

        anglespeed:     Number of degrees the car turns when getting appropriate user input.
        obstacles:      A list of obstacles that the car can interact (collide) with.
        checkpoints:    A list of lines that the car must cross in chronological order to finish a lap.
        
        Returns True if there are more laps to drive. False otherwise.
        """

        for event in pygame.event.get():
            #Check if the user has terminated the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Handle key events
            if event.type == pygame.KEYDOWN:
                self._running = True    #Make sure that the clock has started
                if pygame.key.get_pressed()[self._keys[0][2]]:
                    self._leftTurn = True
                if pygame.key.get_pressed()[self._keys[1][2]]:
                    self._rightTurn = True
                if pygame.key.get_pressed()[self._keys[2][2]]:
                    self._thrust = True
            elif event.type == pygame.KEYUP:
                if not pygame.key.get_pressed()[self._keys[0][2]]:
                    self._leftTurn = False
                if not pygame.key.get_pressed()[self._keys[1][2]]:
                    self._rightTurn = False
                if not pygame.key.get_pressed()[self._keys[2][2]]:
                    self._thrust = False

        if self._running:
            #Handle interaction with other game objects
            self.bounce(self._room)
            self.collide(obstacles)
            self.checkpoint(checkpoints)

            #Update direction and velocity based on user input
            if self._leftTurn and self._rightTurn:
                pass
            elif self._leftTurn:
                self._rotation -= anglespeed
            elif self._rightTurn:
                self._rotation += anglespeed

            if self._thrust == True:
                self._velocity += self.heading()

            #Limit the velocity and move the car
            self.limit_velocity()
            self.move()
            self._frames += 1

        if self._laps <= 0:
            return False
        else:
            return True

    def heading(self):
        """Determines the direction the car is pointing.

        Returns a Vector2D object representing a unit vector in that direction.
        """

        return (Vector2D(math.cos(self._rotation * math.pi / 180),
                         math.sin(self._rotation * math.pi / 180)))

    def limit_velocity(self):
        """Limits the velocity of the supercar based on its _maxSpeed."""

        if self._velocity.magnitude() > self._maxSpeed:
            self._velocity = self._velocity.normalized() * self._maxSpeed

    def collide(self, obstacles):
        """Changes the velocity of the supercar when hitting an obstacle.

        obstacles: The list of obstacles that the car can collide with.

        The method only handles circular obstacles at the moment.
        It is advised to avoid obstacles close to each other or to the borders of _room,
        since hitting multiple objects between two updates is not taken into consideration by the method.
        Additionally, the change in velocity is not very scientific (assumes a head-on elastic collision).
        """

        for thing in obstacles:
            if isinstance(thing, Circle):
                #Test if intersection is possible
                delta = Vector2D(self._w / 2, self._h / 2)
                dist = thing._pos - (self._pos + delta)
                if dist.magnitude() < thing._radius + delta.magnitude():
                    #Check each corner for intersection
                    ul = thing._pos - self._pos
                    ur = thing._pos - (self._pos + Vector2D(self._w, 0))
                    bl = thing._pos - (self._pos + Vector2D(0, self._h))
                    br = thing._pos - (self._pos + Vector2D(self._w, self._h))
                    corners = (ul, ur, bl, br)

                    for pos in corners:
                        if pos.magnitude() < thing._radius:
                            self._pos = self._pos - self._velocity
                            self._velocity *= -1
                            break
