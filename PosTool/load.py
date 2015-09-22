import os
import pygame
from screen import screen
from pygame.locals import *

if not pygame.font:
    print "Warning, fonts disabled."
if not pygame.mixer:
    print "Warning, sounds disabled."

path = '..\data'


class LoadError(Exception):
    pass


def image(name, colorkey):
    fullname = os.path.join(path, name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Error, could not load image:', name
        raise LoadError(message)

    image = image.convert()

    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))

        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()


def sound(name):
    class NoneSound(object):
        def play(self):
            pass

    if not pygame.mixer:
        return NoneSound()

    fullname = os.path.join(path, name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Error, could not load sound:', wav
        raise LoadError(message)

    return sound
