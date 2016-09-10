#!/usr/bin/env python

""" Pre-code for INF-1400

Based on (an earlier version of) code that can be found at:
https://source.uit.no/ifi-courses/inf-1400-2016-resources/blob/master/assignments/assignment1/precode.py

September 2016 Revision 5 (Jon Simonsen)
Added intersect_rectangle_line method. Can probably be optimized and tested better.

28 August 2016 Revision 4 (Jon Simonsen)
Added a fix to make it compatible with Python 3
(mainly using parentheses in print statements).

25 April 2013 Revision 3 (Jon Simonsen)
Added intersect_rectangles method.

22 January 2012 Revision 2 (Martin Ernstsen):
Reraise exception after showing error message.

11 February 2011 Revision 1 (Martin Ernstsen):
Fixed bug in intersect_circle. Updated docstrings to Python standard.
Improved __mul__. Added some exception handling. Put example code in separate
function.

"""

import pygame
import math


class Vector2D(object):
    """ Implements a two dimensional vector. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "Vector(%s, %s)" % (self.x, self.y)
            
    def __add__(self, b):
        """ Addition. Returns a new vector. """
        return Vector2D(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        """ Subtraction. Returns a new vector. """
        return Vector2D(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        """ Multiplication by a scalar
        
        Note that the scalar must be to the right.
        
        """
        try:
            b = float(b)
            return Vector2D(self.x * b, self.y * b)
        except ValueError:
            print("Oops! Right value must be a float")
            raise

    def magnitude(self):
        """ Returns the magnitude of the vector. """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        """ Returns a new vector with the same direction but magnitude 1. """
        try:
            m = self.magnitude()
            return Vector2D(self.x / m, self.y / m)
        except ZeroDivisionError:
            print("Oops! Cannot normalize a zero-vector")
            raise

    def copy(self):
        """ Returns a copy of the vector. """
        return Vector2D(self.x, self.y)
        
        
def intersect_rectangle_circle(rec_pos, sx, sy, circle_pos, circle_radius, circle_speed):
    """ Determine if a rectangle and a circle intersects.
    
    Only works for a rectangle aligned with the axes.
    
    Parameters:
    rec_pos     - A Vector2D representing the position of the rectangles upper,
                  left corner.
    sx          - Width of rectangle.
    sy          - Height of rectangle.
    circle_pos  - A Vector2D representing the circle's position.
    circle_radius - The circle's radius.
    circle_speed - A Vector2D representing the circles speed.
    
    Returns:
    False if no intersection. If the rectangle and the circle intersect, returns
    a normalized Vector2D pointing in the direction the circle will move after
    the collision.
    
    """

    # Position of the walls relative to the ball
    top    = (rec_pos.y     ) - circle_pos.y
    bottom = (rec_pos.y + sy) - circle_pos.y 
    left   = (rec_pos.x     ) - circle_pos.x
    right  = (rec_pos.x + sx) - circle_pos.x

    r = circle_radius 
    intersecting = left <= r and top <= r and right >= -r and bottom >= -r

    if intersecting:
        # Now need to figure out the vector to return.
        # should be just a matter of flipping x and y of the ball?

        impulse = circle_speed.normalized()

        if abs(left) < r and impulse.x > 0:
            impulse.x = -impulse.x
        if abs(right) < r and impulse.x < 0:
            impulse.x = -impulse.x
        if abs(top) < r and impulse.y > 0:
            impulse.y = -impulse.y
        if abs(bottom) < r and impulse.y < 0:
            impulse.y = -impulse.y
            
        #print "Impact", circle_speed, impulse.normalized()

        return impulse.normalized()
    return False


def intersect_circles(a_pos, a_radius, b_pos, b_radius):
    """ Determine if two circles intersect.
    
    Parameters:
    a_pos       - A Vector2D representing circle A's position
    a_radius    - Circle A's radius
    b_pos       - A Vector2D representing circle B's position
    b_radius    - Circle B's radius
    
    Returns:
    False if no intersection. If the circles intersect, returns a normalized
    Vector2D pointing from circle A to circle B.
    
    """
    # vector from A to B 
    dp1p2 = b_pos - a_pos
    
    if a_radius + b_radius >= dp1p2.magnitude():
        return dp1p2.normalized()
    else:
        return False

def intersect_rectangles(a_pos, a_w, a_h, b_pos, b_w, b_h):
    """Determines if two rectangles intersect.

    Parameters:
    a_pos   - A Vector2D representing the position of rectangle a's upper,
                left corner.
    a_w     - Width of rectangle a.
    a_h     - Height of rectangle a.
    b_pos   - A Vector2D representing the position of rectangle b's upper,
              left corner.
    b_w     - Width of rectangle b.
    b_h     - Height of rectangle b.

    Returns:
    True if the rectangles intersect. False otherwise.

    """

    if (((a_pos.x >= b_pos.x and a_pos.x + a_w <= b_pos.x + b_w) or
         (a_pos.x < b_pos.x and a_pos.x + a_w > b_pos.x) or
         (a_pos.x < b_pos.x + b_w and a_pos.x + a_w > b_pos.x + b_w)) and

        ((a_pos.y >= b_pos.y and a_pos.y + a_h <= b_pos.y + b_h) or
         (a_pos.y < b_pos.y and a_pos.y + a_h > b_pos.y) or
         (a_pos.y < b_pos.y + b_h and a_pos.y + a_h > b_pos.y + b_h))):

        return True
    else:
        return False

def intersect_rectangle_line(rec_pos, sx, sy, l_pos, l_len, l_angle):
    """Determines if the rectangle intersects the line.

    Parameters:
    rec_pos   - A Vector2D representing the position of the rectangles upper,
                left corner.
    sx     - Width of the rectangle.
    sy     - Height of the rectangle.
    l_pos   - A Vector2D representing the position of the line's start point.
    l_len     - Length of the line.
    l_angle     - Angle of the line.

    Returns:
    True if the rectangle intersects the line. False otherwise.

    """

    if l_angle == 0:
        if(rec_pos.y < l_pos.y and l_pos.y < rec_pos.y + sy and
           rec_pos.x + sx > l_pos.x and rec_pos.x < l_pos.x + l_len):
            return True
        else:
            return False
    elif l_angle == math.pi / 2:
        if(rec_pos.x < l_pos.x and l_pos.x < rec_pos.x + sx and
           rec_pos.y + sy > l_pos.y and rec_pos.y < l_pos.y + l_len):
            return True
        else:
            return False
    elif l_angle == math.pi:
        if(rec_pos.y < l_pos.y and l_pos.y < rec_pos.y + sy and
           rec_pos.x < l_pos.x and rec_pos.x + sx > l_pos.x - l_len):
            return True
        else:
            return False
    elif l_angle == math.pi * 3 / 2:
        if(rec_pos.x < l_pos.x and l_pos.x < rec_pos.x + sx and
           rec_pos.y < l_pos.y and rec_pos.y + sy > l_pos.y - l_len):
            return True
        else:
            return False
        
    elif l_angle < math.pi:
        if(rec_pos.y > l_pos.y):
            dy_top = rec_pos.y - l_pos.y
            dlen_top = dy_top / math.sin(l_angle)
            dy_bottom = rec_pos.y + sy - l_pos.y
            dlen_bottom = dy_bottom / math.sin(l_angle)
        elif(rec_pos.y + sy > l_pos.y):
            dy_top = 0
            dlen_top = 0
            dy_bottom = rec_pos.y + sy - l_pos.y
            dlen_bottom = dy_bottom / math.sin(l_angle)
        else:
            return False

        if dlen_top >= l_len:
            return False
        
        if dlen_bottom > l_len:
            dlen_bottom = l_len
            dy_bottom = l_len * math.sin(l_angle)

        if l_angle < math.pi / 2:
            if(rec_pos.x + sx <= l_pos.x + dy_top / math.tan(l_angle) or
               rec_pos.x >= l_pos.x + dy_bottom / math.tan(l_angle)):
                return False
            else:
                return True
        else:
            if(rec_pos.x >= l_pos.x + dy_top / math.tan(l_angle) or
               rec_pos.x + sx <= l_pos.x + dy_bottom / math.tan(l_angle)):
                return False
            else:
                return True
    elif l_angle < 2 * math.pi:
        if(rec_pos.y + sy < l_pos.y):
            dy_bottom = (rec_pos.y + sy) - l_pos.y
            dlen_bottom = dy_bottom / math.sin(l_angle)
            dy_top = rec_pos.y - l_pos.y
            dlen_top = dy_top / math.sin(l_angle)
        elif(rec_pos.y < l_pos.y):
            dy_bottom = 0
            dlen_bottom = 0
            dy_top = rec_pos.y - l_pos.y
            dlen_top = dy_top / math.sin(l_angle)
        else:
            return False

        if dlen_bottom >= l_len:
            return False

        if dlen_top > l_len:
            dlen_top = l_len
            dy_top = l_len * math.sin(l_angle)

        if l_angle < math.pi * 3 / 2:
            if(rec_pos.x + sx <= l_pos.x + dy_top / math.tan(l_angle) or
               rec_pos.x >= l_pos.x + dy_bottom / math.tan(l_angle)):
                return False
            else:
                return True
        else:
            if(rec_pos.x >= l_pos.x + dy_top / math.tan(l.angle) or
               rec_pos.x + sx <= l_pos.x + dy_bottom / math.tan(l_angle)):
                return False
            else:
                return True

def example_code():
    """ Example showing the use of the above code. """
    
    screen_res = (640,480)
    pygame.init()

    ra_pos = Vector2D(320, 320) # Rectangle A position
    ra_sx = ra_sy = 20 # Rectangle A size

    rb_pos = Vector2D(250, 250) # Rectangle B position
    rb_sx = rb_sy = 10 # Rectangle B stretch

    # Tracks the mouse cursor
    a_pos = Vector2D(10, 10) # Circle A position
    a_radius = 6 # Circle A radius
    a_speed = Vector2D(5,5) # Circle A speed

    b_pos = Vector2D(150, 150) # Circle B position
    b_radius = 10 # Circle B radius
    b_speed = Vector2D(5,5) # Circle B speed

    screen = pygame.display.set_mode(screen_res)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
        pygame.draw.rect(screen, (0,0,0), (0, 0, screen.get_width(), screen.get_height()))
        time_passed = clock.tick(30) # limit to 30FPS 
        time_passed_seconds = time_passed / 1000.0   # convert to seconds

        x, y = pygame.mouse.get_pos()
        a_pos = Vector2D(x, y)

        pygame.draw.rect(screen, (255,255,255), (ra_pos.x, ra_pos.y, ra_sx, ra_sy))
        pygame.draw.rect(screen, (255,255,255), (rb_pos.x, rb_pos.y, rb_sx, rb_sy))
        pygame.draw.circle(screen, (255,255,255), (b_pos.x, b_pos.y), b_radius) # other circle
        pygame.draw.circle(screen, (255,0,0),     (a_pos.x, a_pos.y), a_radius) # mouse

        def draw_vec_from_ball(vec, col):
            """ Draw a vector from the mouse controlled circle. """
            pygame.draw.line(screen, col,  (a_pos.x, a_pos.y), (a_pos.x + vec.x * 20, a_pos.y + vec.y * 20), 3)

        # Draw speed vector
        draw_vec_from_ball(a_speed, (255,255,0))

        # The big rectangle        
        impulse = intersect_rectangle_circle(ra_pos, ra_sx, ra_sy, a_pos, a_radius, a_speed)
        if impulse:
            draw_vec_from_ball(impulse, (0, 255,255))
    
        # The small rectangle
        impulse = intersect_rectangle_circle(rb_pos, rb_sx, rb_sy, a_pos, a_radius, a_speed)
        if impulse:
            draw_vec_from_ball(impulse, (0, 255,255))

        # The circle
        impulse = intersect_circles(a_pos, a_radius, b_pos, b_radius)
        if impulse:
            draw_vec_from_ball(impulse, (0, 255,255))

        pygame.display.update()
    
    
if __name__ == '__main__':
    example_code()
