#Imports

##External
import pygame, sys, math
from precode import Vector2D, intersect_rectangles, intersect_rectangle_circle

##General methods
from library import *

##Global constants
from drawconf import *

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

    def bounce(self, room):
        """Changes velocity and position of the object if it hits a wall.

        Currently assumes a rectangular object with _pos a Vector2D
        pointing to its upper left corner. It also produces approximate results
        for circular objects.
        The argument represents a room (as a Rectangle) that contains the object.
        The method should not be used if there's a chance that the object has moved
        so far outside the boundaries that it's still outside after the adjustments.
        Using a room with negative coordinates is also not advisable (not tested).

        room:   A Rectangle object that should contain the moving object.

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
            
        if self._pos.x <= room._pos.x:
            self._velocity.x *= -1
            self._pos.x = 2 * room._pos.x - self._pos.x
            collision = True
        elif self._pos.x + w >= room._pos.x + room._w:
            self._velocity.x *= -1
            self._pos.x = 2 * (room._pos.x + room._w) - (self._pos.x + 2 * w)
            
        if self._pos.y <= room._pos.y:
            self._velocity.y *= -1
            self._pos.y = 2 * room._pos.y - self._pos.y
            collision = True
        elif self._pos.y + h >= room._pos.y + room._h:
            self._velocity.y *= -1
            self._pos.y = 2 * (room._pos.y + room._h) - (self._pos.y + 2 * h)
            collision = True

        return collision
