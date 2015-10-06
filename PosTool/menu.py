import pygame
import entities
from screen import screen
from pygame.locals import *


def right_click(options):
    # save the current screen as the background
    background = screen

    menu = pygame.sprite.RenderUpdates()
    origin_pos = pygame.mouse.get_pos()

    for i in xrange(options):
        result = entities.TextMenu(options[i], 18, 200)
        result.rect.topleft = (origin_pos[0], origin_pos[1]+i*18)

        menu.add(result)
