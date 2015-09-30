import os
import pygame
import entities
from pygame.locals import *

if not pygame.font:
    print "Warning, fonts disabled."
if not pygame.mixer:
    print "Warning, sounds disabled."

path = '..\data'

# global constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


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


def _deselector(selectionlist, poslist, ctrl):
    if not ctrl:
        for item in selectionlist.sprites():
            item.ref.selected = False
        selectionlist.empty()
        poslist.empty()


def _selector(selectionlist, poslist, item):
    item.selected = True
    selectionlist.add(entities.SelectItem(item))
    poslist.add(entities.TextPos(item, 18, WHITE, BLACK))


def selectbot(selectionlist, poslist, item=None, ctrl=False):
    # if the selection has been ban boxed
    if isinstance(item, (list, tuple)):
        _deselector(selectionlist, poslist, ctrl)

        for i in item:
            _selector(selectionlist, poslist, i)

    # single-item selections
    elif item:
        if item.selected is False:
            _deselector(selectionlist, poslist, ctrl)

            _selector(selectionlist, poslist, item)
            item.grab()
        else:
            for i in selectionlist.sprites():
                i.ref.grab()

    # nothing was selected
    else:
        _deselector(selectionlist, poslist, ctrl)
