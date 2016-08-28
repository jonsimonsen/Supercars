"""A collection of functions. Originally used in the game "Mayhem in space".

Created by Jon Simonsen
Current version dated 26 April 2013"""

import pygame

def makeFont(font, size):
    """Generates a pygame font.

    Returns the font object."""

    font = pygame.font.SysFont(font, size)
    return font

def rotate_center(layer, angle):
    """Rotates a pygame surface while keeping its center and size

    layer is the layer to be rotated
    angle is the counter-clockwise rotation in degrees

    Returns the resulting surface."""

    #The method is derived from an existing method from the pygame.org homepage
    newlayer = pygame.transform.rotate(layer, angle)
    rectangle = layer.get_rect()
    rectangle.center = newlayer.get_rect().center
    newlayer = newlayer.subsurface(rectangle)
    return newlayer
