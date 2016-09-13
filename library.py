"""A collection of functions. Originally used in the game "Mayhem in space".

Created by Jon Simonsen
Initial version dated 26 April 2013

13.09.16: Added framesToSec (jsi)
"""

import pygame

def makeFont(font, size):
    """Generate a pygame font.

    Returns the font object.
    """

    font = pygame.font.SysFont(font, size)
    return font

def rotate_center(layer, angle):
    """Rotates a pygame surface while keeping its center and size

    layer: The layer to be rotated
    angle: The counter-clockwise rotation in degrees

    Returns the resulting surface.
    """

    #The method is derived from an existing method from the pygame.org homepage
    newlayer = pygame.transform.rotate(layer, angle)
    rectangle = layer.get_rect()
    rectangle.center = newlayer.get_rect().center
    newlayer = newlayer.subsurface(rectangle)
    return newlayer

def framesToSec(frames, fps):
    """Convert a number of frames to a number of seconds with two decimals.

    frames: The number of frames
    fps: Frames per second

    Returns the number of seconds it takes to display the frames (as a float).
    """

    return round((frames / fps), 2)
