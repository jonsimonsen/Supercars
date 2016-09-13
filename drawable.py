import pygame, sys, math
from precode import Vector2D, intersect_rectangles, intersect_rectangle_line
from config import *
from library import *

#Classes for drawable objects

class Drawable(object):
    """A drawable object (as an abstract data type)."""

    def __init__(self):
        """default initialization of the ADT."""

        print("please don't try to initialize an object of type ADT.")

    def draw(self, layer):
        """Default drawing method for this kind of datatype.

        layer: The surface to be drawn to.
        """

        print("please don't try to draw an object of type ADT.")

    def erase(self, color, layer):
        """Draws the object. To actually erase it, the given color must match the background color.

        color: The color to draw the object with. To erase, this should match the background.
        layer: The layer to draw the object onto.
        """

        #To avoid permanently changing the object, its actual color must be stored until it has been drawn with the given color.
        temp = self._color
        self._color = color
        self.draw(layer)
        self._color = temp

    def getPos(self):
        """Getter for _pos."""
        return self._pos

    def setPos(self, value):
        """Setter for _pos."""
        self._pos = value

    def getColor(self):
        """Getter for _color."""
        return self._color

    def setColor(self, value):
        """Setter for _color."""
        self._color = value

class Rectangle(Drawable):
    """A general rectangle object."""

    def __init__(self, width, height, color, x = 0, y = 0):
        """Create a rectangle.

        x, y:           x- and y-components used for a Vector2D object
                        pointing to the upper left corner of the rectangle.
        width, height:  Width and height of the rectangle.
        color:          Color of the rectangle.
        """

        self._w = width             #width
        self._h = height            #height
        self._pos = Vector2D(x, y)  #coordinates for upper left corner
        self._color = color         #Frequently used colors should be defined in the config file

    def draw(self, layer, offset = Vector2D(0, 0)):
        """Draws the rectangle.

        layer:  The surface being drawn to.
        offset: An offset between the rectangle's position (absolute) and
                the position of the rectangle on a specific surface (relative).
        """

        pygame.draw.rect(layer, self._color,(int(self._pos.x + offset.x), int(self._pos.y + offset.y), self._w, self._h))

    def objectCollision(self, other):   #TODO: should be updated
        """Checks for collision between the rectangle and another object.

        other:  Another object. It is assumed that this is a rectangle or a circle.
                A type error will be raised if it isn't.

        Returns True if the rectangle collides with the other object. False otherwise.
        """

        if isinstance(other, Circle):   #TODO: See if this needs to be altered
            collision = precode.intersect_rectangle_circle(self._pos, self._w, self._h, other._pos, other._radius, Vector2D(1,1))
        elif isinstance(other, Rectangle):
            collision = intersect_rectangles(self._pos, self._w, self._h,
                                             other._pos, other._w, other._h)
        else:
            raise TypeError("other must be an object of class Rectangle, class Circle or a subclass of these.")

        if collision:
            return True
        else:
            return False

    def getW(self):
        """Getter for _w."""
        return self._w
    
    def setW(self, value):
        """Setter for _w."""
        self._w = value
        
    def getH(self):
        "Getter for _h."""
        return self._h

    def setH(self, value):
        "Setter for _h."""
        self._h = value

class Circle(Drawable):
    """A general circle object."""

    def __init__(self, posx, posy, radius, color):
        """Create a circle.

        posx, posy: x- and y-components used for a Vector2D object
                    pointing to the center of the circle.
        radius:     Radius of the circle.
        color:      Color of the circle.
        """

        self._pos = Vector2D(posx, posy)
        self._radius = radius
        self._color = color

    def draw(self, layer):
        """Draws the circle.

        layer: The surface being drawn to.
        """

        pygame.draw.circle(layer, self._color, (int(self._pos.x), int(self._pos.y)), self._radius)

    def getRadius(self):
        """Getter for _radius."""
        return self._radius

    def setRadius(self, value):
        """Setter for _radius."""
        self._radius = value

#A base class for Line and Arc could be considered.

class Line(Drawable):
    """A straight line."""

    def __init__(self, posx, posy, length, width, angle, color):
        """Create a straight line.

        posx, posy: x- and y-components for the startpoint of the line.
        length:     Length of the line.
        width:      Width of the line.
        angle:      Clockwise angle relative to positive x.
        color:      Color of the line.
        """

        self._pos = Vector2D(posx, posy)
        self._length = length
        self._width = width
        self._angle = angle
        self._color = color

    def draw(self, layer):
        """Draws the line.

        layer: The surface being drawn to.
        """

        pygame.draw.line(layer, self._color, (self._pos.x, self._pos.y),
                         (self._pos.x + math.cos(self._angle) * self._length, self._pos.y + math.sin(self._angle)*self._length),
                         self._width)

    def getLength(self):
        """Getter for _length."""
        return self._length

    def setLength(self, value):
        """Setter for _length."""
        self._length = value

    def getWidth(self):
        """Getter for _width."""
        return self._width

    def setWidth(self, value):
        """Setter for _width."""
        self._width = value

    def getAngle(self):
        """Getter for _angle."""
        return self._angle

    def setAngle(self, value):
        """Setter for _angle."""
        self._angle = value

class Arc(Drawable):
    """A curved line (circular curvature)."""

    def __init__(self, posx, posy, length, width, angle, span, color):
        """Create an arc.

        posx, posy: x and y-components for the center point.
        length:     Length from the centre point to the arc.
        width:      Width of the arc. Grows towards the center point.
        angle:      Clockwise angle relative to positive x for the start of the arc.
        span:       Number of radians the arc spans across.
        color:      Color of the arc.
        """

        self._pos = Vector2D(posx, posy)
        self._length = length
        self._width = width
        self._angle = angle
        self._span = span
        self._color = color

    def draw(self, layer):
        """Draws the arc.

        layer: The surface being drawn to.
        """

        pygame.draw.arc(layer, self._color,
                        (self._pos.x - self._length, self._pos.y - self._length, 2 * self._length, 2 * self._length),
                        self._angle, self._angle + self._span, self._width)

    def getLength(self):
        """Getter for _length."""
        return self._length

    def setLength(self, value):
        """Setter for _length."""
        self._length = value

    def getWidth(self):
        """Getter for _width."""
        return self._width

    def setWidth(self, value):
        """Setter for _width."""
        self._width = value

    def getAngle(self):
        """Getter for _angle."""
        return self._angle

    def setAngle(self, value):
        """Setter for _angle."""
        self._angle = value

    def getSpan(self):
        """Getter for _span."""
        return self._span

    def setSpan(self, value):
        """Setter for _span."""
        self._span = value

#Classes for moveable objects

class MovingObject(Drawable):
    """A moveable object."""

    def move(self):
        """Moves the object."""

        self._pos += self._velocity

    def bounce(self, width, height, leftwall_x = 0, ceiling_y = 0):
        """Changes velocity and position of the object if it hits a wall.

        Currently assumes a rectangular object with _pos a Vector2D
        pointing to its upper left corner. It also produces approximate results
        for circular objects.
        The arguments represents the boundaries of a room that contains the object.
        The method should not be used if there's a chance that the object has moved
        so far outside the boundaries that it's still outside after the adjustments.
        If the moving object has a reasonable velocity compared to the dimensions of the room,
        the method should work as intended.

        leftwall_x: Minimum x-component of the object's position
        ceiling_y:  Minimum y-component of the object's position
        width:      Difference between minimum x-component and right wall
        height:     Difference between minimum y-component and floor

        Returns True if a collision occurs. False otherwise
        """

        collision = False

        if isinstance(self, Circle):
            w = self._radius
            h = self._radius
        elif isinstance(self, Rectangle):
            w = self._w
            h = self._h
        else:
            raise TypeError("The moving object must be a Rectangle or a Circle.")
            
        if self._pos.x <= leftwall_x:
            self._velocity.x *= -1
            self._pos.x = 2 * leftwall_x - self._pos.x
            collision = True
        elif self._pos.x + w >= leftwall_x + width:
            self._velocity.x *= -1
            self._pos.x = 2 * (leftwall_x + width) - (self._pos.x + 2 * w)
            
        if self._pos.y <= ceiling_y:
            self._velocity.y *= -1
            self._pos.y = 2 * ceiling_y - self._pos.y
            collision = True
        elif self._pos.y + h >= ceiling_y + height:
            self._velocity.y *= -1
            self._pos.y = 2 * (ceiling_y + height) - (self._pos.y + 2 * h)
            collision = True

        return collision

class Supercar(Rectangle, MovingObject):
    """A supercar (moving sprite on a layer)."""

    def __init__(self, pos, speed, color, width, length, rotation = 0,
                 wcolor = BLACK, bgcolor = TRANSPARENT):
        """Create a supercar.

        pos:        A vector2D object pointing to the upper left corner of the
                    layer the car is going to be drawn onto.
        speed:      A Vector2D object representing the car's velocity.
        color:      The color of the rectangle representing the car's body.
        width:      The width of the car (must be less than length).
        length:     The length of the car (and dimension of its surface).
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
        self._rotation = rotation
        self._wcolor = wcolor
        self._bgcolor = bgcolor
        
        self._layer = self._makeLayer()
        self._keys = self._makeControls()        
        self._thrust = False
        self._leftTurn = False
        self._rightTurn = False
        
        self._running = False       #Wait for the player to start moving before starting the clock
        self._laps = 10             #Laps to go
        self._checkpoints = -1      #Index of latest checkpoint
        self._frames = 0            #Number of frames for this lap
        self._fastestLap = -1       #Fastest lap time
        self._latestLap = 0         #Latest lap time
        self._totalLap = 0          #Total lap time

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

        offset = self._h / 5
        width = self._h / 6
        border = self._w / 8  #To prevent the car from being misshaped when being rotated on the layer

        pygame.draw.rect(layer, self._wcolor, (border, offset, self._w - 2 * border, width))
        pygame.draw.rect(layer, self._wcolor, (border, self._h - (offset + width), self._w - 2 * border, width))

    def _drawBody(self, layer):
        """Draws the car's body.

        layer: The surface being drawn to.
        """

        offset = self._w / 5
        border = self._w / 8  #To prevent the car from being misshaped when being rotated on the layer

        pygame.draw.rect(layer, self._color, (offset, border, self._w - 2 * offset, self._h - 2 * border))

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

    def draw(self, layer):
        """Draws the car (actually draws the car's layer onto another layer).

        layer: Layer to draw the car onto.
        """

        carlayer = rotate_center(self._layer, CAR_ROTATION - self._rotation)
        layer.blit(carlayer, (self._pos.x, self._pos.y))

    def checkpoint(self, points):
        """Handles intersection between the car and a checkpoint.

        points: A list of checkpoints that the car must cross in chronological order on every lap.
        """

        self._frames += 1

        if self._checkpoints < 0:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[0]._pos, points[0]._length, points[0]._angle):
                self._checkpoints = 0
                self._totalLap = round((self._frames) / FPS, 2)
                self._frames = 0    #Consider using fractions for higher accuracy
        elif self._checkpoints == len(points) - 1:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[0]._pos, points[0]._length, points[0]._angle):
                self._laps -= 1
                self._checkpoints = 0
                self._latestLap = round((self._frames + 1) / FPS, 2)
                if self._fastestLap < 0 or self._latestLap < self._fastestLap:
                    self._fastestLap = self._latestLap
                #print(str(self._fastest), str(self._latest))
                self._totalLap += self._latestLap
                self._frames = 0
        else:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[self._checkpoints + 1]._pos, points[self._checkpoints + 1]._length,
                                        points[self._checkpoints + 1]._angle):
                self._checkpoints += 1

        #for i in range(len(points)):
        #    if intersect_rectangle_line(self._pos, self._w, self._h,
        #                                points[i]._pos, points[i]._length, points[i]._angle):
        #        print(str(i))

    def update(self, anglespeed, speedlimit, keys, obstacles, checkpoints):
        """Updates the car's velocity and rotation based on user input and
        speed limit.

        anglespeed: Number of degrees the car turns when getting appropriate user input.
        speedlimit: Maximal speed for the car
        keys:       list of lists where the third element (index 2) needs to be a
                    pygame key constant corresponding to a legal input from the player.
        
        Returns True if there are more laps to drive. False otherwise."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if keys == 0:
                pass
            else:
                if event.type == pygame.KEYDOWN:
                    self._running = True    #Make sure that the clock has started
                    if pygame.key.get_pressed()[keys[0][2]]:
                        self._leftTurn = True
                    if pygame.key.get_pressed()[keys[1][2]]:
                        self._rightTurn = True
                    if pygame.key.get_pressed()[keys[2][2]]:
                        self._thrust = True
                elif event.type == pygame.KEYUP:
                    if not pygame.key.get_pressed()[keys[0][2]]:
                        self._leftTurn = False
                    if not pygame.key.get_pressed()[keys[1][2]]:
                        self._rightTurn = False
                    if not pygame.key.get_pressed()[keys[2][2]]:
                        self._thrust = False

        if self._running:
            self.bounce(RES_X, RES_Y)
            self.collide(obstacles)
            self.checkpoint(checkpoints)
                    
            if self._leftTurn and self._rightTurn:
                pass
            elif self._leftTurn:
                self._rotation -= anglespeed
            elif self._rightTurn:
                self._rotation += anglespeed

            if self._thrust == True:
                self._velocity += self.heading()

            self.limit_velocity()

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
        """Limits the velocity of the supercar based on SPEEDLIMIT."""

        if self._velocity.magnitude() > SPEEDLIMIT:
            self._velocity = self._velocity.normalized() * SPEEDLIMIT

    def collide(self, obstacles):
        """Changes the velocity of the supercar when hitting one of the obstacles."""

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
