import pygame
import entities
from screen import screen
from pygame.locals import *


def right_click(options):
    # save the current screen as the background
    background = screen.copy()
    font_size = 18

    menu = pygame.sprite.RenderUpdates()
    origin_pos = pygame.mouse.get_pos()

    for i in xrange(len(options)):
        result = entities.TextMenu(options[i], font_size, 200)
        row_pos = i * font_size
        result.rect.topleft = (origin_pos[0], origin_pos[1]+row_pos)

        menu.add(result)

    looping = True
    result = None
    drawitems = []

    while looping:
        for e in pygame.event.get():
            # ===========================================================
            # -------------------- MOUSE BUTTON DOWN --------------------
            # ===========================================================
            if e.type == MOUSEBUTTONDOWN:
                # ==================== LEFT CLICK ===================
                if e.button == 1:
                    pos = pygame.mouse.get_pos()

                    for item in menu.sprites():
                        if item.rect.collidepoint(pos):
                            result = item.text

                    looping = False

                # =================== RIGHT CLICK ===================
                if e.button == 3:
                    looping = False
                    result = -1

        menu.clear(screen, background)
        menu.update()
        drawitems = menu.draw(screen)

        pygame.display.update(drawitems)

    menu.clear(screen, background)
    pygame.display.update()

    return result
