import pygame, sys, math
from precode import Vector2D, intersect_rectangles, intersect_rectangle_line
from config import *

#Classes for drawable objects

class Drawable(object):
    """A drawable object"""

    def __init__(self):
        """default initialization of the ADT"""

        print("please don't try to initialize an object of type ADT.")

    def draw(self, layer):
        """Default drawing method for this kind of datatype.

        layer is the surface to be drawn to."""

        print("please don't try to draw an object of type ADT.")

    def erase(self, color, layer):
        """Draws the calling object onto layer using color
        without changing its own color (_color)."""

        temp = self._color
        self._color = color
        self.draw(layer)
        self._color = temp

    def getPos(self):
        """Getter for _pos"""
        return self._pos

    def setPos(self, value):
        """Setter for _x"""
        self._pos = value

    def getColor(self):
        """Getter for _color"""
        return self._color

    def setColor(self, value):
        """Setter for _color"""
        self._color = value

class Rectangle(Drawable):
    """A class for general rectangle objects"""

    def __init__(self, width, height, color, x = 0, y = 0):
        """Setting up variables for the rectangle.

        x, y:           x- and y-components used for a Vector2D object
                        pointing to the upper left corner of the rectangle.
        width, height:  Width and height of the rectangle
        color:          Color of the rectangle"""

        self._w = width             #width
        self._h = height            #height
        self._pos = Vector2D(x, y)  #coordinates for upper left corner
        self._color = color         #Frequently used colors should be defined in the config file

    def draw(self, layer, offset = Vector2D(0, 0)):
        """Draws the rectangle.

        layer is the surface being drawn to.
        offset is an offset between the rectangle's position (absolute) and
        the position of the rectangle on a specific surface (relative)."""

        pygame.draw.rect(layer, self._color,(int(self._pos.x + offset.x), int(self._pos.y + offset.y), self._w, self._h))

    def objectCollision(self, other):   #TODO: should be updated
        """Checks for collision between self and other where other can be represented as
        a rectangle or other is an object of the Circle class.

        other is another rectangular object with variables _pos, _w and _h
        (position as a Vector2D, width and height) or an object of class Circle

        Returns True if the rectangle collides with the other object.
        False is returned otherwise"""

        if isinstance(other, Circle):   #TODO: See if this needs to be altered
            collision = precode.intersect_rectangle_circle(self._pos, self._w, self._h, other._pos, other._radius, Vector2D(1,1))
        else:
            collision = intersect_rectangles(self._pos, self._w, self._h,
                                             other._pos, other._w, other._h)

        if collision:
            return True
        else:
            return False

    def getW(self):
        """Getter for _w"""
        return self._w
    
    def setW(self, value):
        """Setter for _w"""
        self._w = value
        
    def getH(self):
        "Getter for _h"""
        return self._h

    def setH(self, value):
        "Setter for _h"""
        self._h = value

class Circle(Drawable):
    """A class for general circle objects"""

    def __init__(self, posx, posy, radius, color):
        """Setting up variables for the circle.

        posx, posy: x- and y-components used for a Vector2D object
                    pointing to the center of the circle.
        radius:     Radius of the circle
        color:      Color of the circle"""

        self._pos = Vector2D(posx, posy)
        self._radius = radius
        self._color = color

    def draw(self, layer):
        """Draws the circle onto a surface.

        layer is the surface being drawn to."""

        pygame.draw.circle(layer, self._color, (int(self._pos.x), int(self._pos.y)), self._radius)

    def getRadius(self):
        """Getter for _radius"""
        return self._radius

    def setRadius(self, value):
        """Setter for _radius"""
        self._radius = value

class Line(Drawable):
    """A class for a straight line"""

    def __init__(self, posx, posy, length, width, angle, color):
        """Setting up variables for the line.

        posx, posy: x- and y-components for the startpoint of the line.
        length:     Length of the line
        angle:      Clockwise angle relative to positive x.
        color:      Color of the line."""

        self._pos = Vector2D(posx, posy)
        self._length = length
        self._width = width
        self._angle = angle
        self._color = color

    def draw(self, layer):
        """Draws the line onto a surface.

        layer is the surface being drawn to."""

        pygame.draw.line(layer, self._color, (self._pos.x, self._pos.y), (self._pos.x + math.cos(self._angle) * self._length, self._pos.y + math.sin(self._angle)*self._length), self._width)

    def getLength(self):
        """Getter for _length"""
        return self._length

    def setLength(self, value):
        """Setter for _length"""
        self._length = value

    def getAngle(self):
        """Getter for _angle"""
        return self._angle

    def setAngle(self, value):
        """Setter for _angle"""
        self._angle = value

class Arc(Drawable):
    """A class for a curved line"""

    def __init__(self, posx, posy, length, width, angle, span, color):
        """Settin up variables for the arc.

        posx, posy: x and y-components for the centre point.
        length:     Length from the centre point to the arc.
        angle:      Clockwise angle relative to positive x for the start of the arc.
        span:       Number of radians the arc spans across
        color:      Color of the arc."""

        self._pos = Vector2D(posx, posy)
        self._length = length
        self._width = width
        self._angle = angle
        self._span = span
        self._color = color

    def draw(self, layer):
        """Draws the arc onto a surface.

        layer is the surface being drawn to."""

        pygame.draw.arc(layer, self._color, (self._pos.x - self._length, self._pos.y - self._length, 2 * self._length, 2 * self._length), self._angle, self._angle + self._span, self._width)

    def getLength(self):
        """Getter for _length"""
        return self._length

    def setLength(self, value):
        """Setter for _length"""
        self._length = value

    def getAngle(self):
        """Getter for _angle"""
        return self._angle

    def setAngle(self, value):
        """Setter for _angle"""
        self._angle = value

#Classes for moveable objects

class MovingObject(Drawable):
    """A moveable object"""

    def move(self):
        """Moves the object"""

        self._pos += self._velocity

    def collide(self, width, height, leftwall_x = 0, ceiling_y = 0):
        """Changes velocity and position of the object if it hits a wall.
        Currently assumes a rectangular object with _pos a Vector2D
        pointing to its upper left corner. It also produces approximate results
        for circular objects.

        leftwall_x: Minimum x-component of the object's position
        ceiling_y:  Minimum y-component of the object's position
        width:      Difference between minimum x-component and right wall
        height:     Difference between minimum y-component and floor

        Returns True if a collision occurs. False otherwise"""

        collision = False

        if isinstance(self, Circle):
            w = self._radius
            h = self._radius
        else:
            w = self._w
            h = self._w
            
        if self._pos.x + w > width:
            self._velocity.x *= -1
            self._pos.x += self._velocity.x
            collision = True
        if self._pos.x < 0:
            self._velocity.x *= -1
            self._pos.x += self._velocity.x
            collision = True
        if self._pos.y < 0:
            self._velocity.y *= -1
            self._pos.y += self._velocity.y
            collision = True
        if self._pos.y + h > height:
            self._velocity.y *= -1	
            self._pos.y += self._velocity.y
            collision = True

        return collision


class Supercar(Rectangle, MovingObject):
    """a class for a supercar (moving sprite on a layer)"""

    def __init__(self, pos, speed, color, width, length, rotation = 0,
                 wcolor = BLACK, bgcolor = TRANSPARENT):
        """Setting up variables for the supercar.

        pos:        A vector2D object pointing to the upper left corner of the
                    layer the car is going to be drawn onto.
        speed:      A Vector2D object representing the car's velocity
        color:      The color of the rectangle representing the car's body.
        width:      The width of the car (must be less than length)
        length:     The length of the car (and dimension of its surface)
        rotation:   The direction the car is pointing in degrees. 0 means right,
                    and positive numbers signifies clockwise rotation
        bgcolor:    Background color of the surface the car is drawn onto."""

        if(width >= length):
            print("The supercar must have a height(length) greater than its width.")
        Rectangle.__init__(self, length, length, color, pos.x, pos.y)

        self._width = width
        self._velocity = speed
        self._thrust = False
        self._leftTurn = False
        self._rightTurn = False
        self._rotation = rotation
        self._bgcolor = bgcolor
        self._wcolor = wcolor
        self._layer = self.draw()
        self._spawnlocation = self._pos
        self._keys = self.makeControls()
        self._laps = 5          #Laps to go
        self._checkpoints = -1  #Index of latest checkpoint
        self._frames = 0       #Number of frames for this lap
        self._fastest = -1      #Fastest lap
        self._latest = 0       #Latest lap

    def draw(self):
        """Generates a surface with the supercar drawn onto it.

        returns the surface"""

        surface = pygame.Surface((self._w, self._h)).convert_alpha()
        surface.fill(self._bgcolor)
        self._drawWheels(surface)
        self._drawBody(surface)
        #pygame.draw.polygon(surface, self._color, self._points)

        return surface

    def checkpoint(self, points):
        """When intersecting with a checkpoint, handle appropriately"""

        self._frames += 1

        if self._checkpoints < 0:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[0]._pos, points[0]._length, points[0]._angle):
                self._checkpoints = 0
                self._frames = 0    #Consider using fractions for higher accuracy
        elif self._checkpoints == len(points) - 1:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[0]._pos, points[0]._length, points[0]._angle):
                self._laps -= 1
                self._checkpoints = 0
                self._latest = round((self._frames + 1) / FPS, 2)
                if self._fastest < 0 or self._latest < self._fastest:
                    self._fastest = self._latest
                #print(str(self._fastest), str(self._latest))
                self._frames = 0
        else:
            if intersect_rectangle_line(self._pos, self._w, self._h,
                                        points[self._checkpoints + 1]._pos, points[self._checkpoints + 1]._length, points[self._checkpoints + 1]._angle):
                self._checkpoints += 1

        #for i in range(len(points)):
        #    if intersect_rectangle_line(self._pos, self._w, self._h,
        #                                points[i]._pos, points[i]._length, points[i]._angle):
        #        print(str(i))

    def _drawWheels(self, layer):
        """Draws wheels onto layer"""

        offset = self._h / 5
        width = self._h / 6
        border = self._w / 8  #To prevent the car from being misshaped when being rotated on the layer

        pygame.draw.rect(layer, self._wcolor, (border, offset, self._w - 2 * border, width))
        pygame.draw.rect(layer, self._wcolor, (border, self._h - (offset + width), self._w - 2 * border, width))

    def _drawBody(self, layer):
        """Draws the car's body onto layer."""

        offset = self._w / 5
        border = self._w / 8  #To prevent the car from being misshaped when being rotated on the layer

        pygame.draw.rect(layer, self._color, (offset, border, self._w - 2 * offset, self._h - 2 * border))

    def makeControls(self):
        """Generates a list containing the keys the player can use (as a tuple).

        First element is a surface supposed to hold a key image
        Second element is text to accompany the image
        Third element is a pygame key constant for the corresponding key
        
        Returns the list of tuples.
        """

        return ([(IMAGE, KEYTEXT[0], pygame.K_LEFT),
                 (IMAGE, KEYTEXT[1], pygame.K_RIGHT),
                 (IMAGE, KEYTEXT[2], pygame.K_UP)])

    def update(self, anglespeed, speedlimit, keys, obstacles, checkpoints):
        """Updates the car's velocity and rotation based on user input and
        speed limit.

        anglespeed: Number of degrees the car turns when getting appropriate user input.
        speedlimit: Maximal speed for the car
        keys:       list of lists where the third element (index 2) needs to be a
                    pygame key constant corresponding to a legal input from the player.
        
        Returns nothing"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if keys == 0:
                pass
            else:
                if event.type == pygame.KEYDOWN:
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

        self.bounce()
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

        return

    def heading(self):
        """Determines the direction the car is pointing.

        Returns a Vector2D object representing a unit vector in that direction."""

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

    def bounce(self):
        """Changes the velocity of the supercar when hitting the screen boundary. Returns True if changed, False otherwise."""

        if self._pos.x < 0:
            self._velocity.x *= -1
            self._pos.x *= -1
            #self._thrust = False    #Make sure that the player can't accelerate directly after an impact
        elif self._pos.x > RES_X - self._w:
            self._velocity.x *= -1
            self._pos.x = (2 * (RES_X - self._w)) - self._pos.x
            #self._thrust = False

        if self._pos.y < 0:
            self._velocity.y *= -1
            self._pos.y *= -1
            #self._thrust = False
        elif self._pos.y > RES_Y - self._h:
            self._velocity.y *= -1
            self._pos.y = (2 * (RES_Y - self._h)) - self._pos.y
            #self._thrust = False
