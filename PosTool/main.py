import pygame
import load
import sys
import entities
from screen import screen
from pygame.locals import *

# TODO: Rather than basing selection status posdisplaysake it so that the
# status is only updaposdisplaysItem.selection boolean

# global constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def deselector(selectionlist, poslist):
    for item in selectionlist.sprites():
        item.ref.selected = False
    selectionlist.empty()
    poslist.empty()


def selector(selectionlist, poslist, item):
    item.selected = True
    selectionlist.add(entities.SelectItem(item))
    poslist.add(entities.TextPos(item, 18, WHITE, BLACK))


def selectbot(selectionlist, poslist, item=None):
    # if the selection has been ban boxed
    if isinstance(item, (list, tuple)):
        deselector(selectionlist, poslist)

        for i in item:
            selector(selectionlist, poslist, i)

    # single-item selections
    elif item:
        if item.selected is False:
            deselector(selectionlist, poslist)

            selector(selectionlist, poslist, item)
            item.grab()
        else:
            for i in selectionlist.sprites():
                i.ref.grab()

    # nothing was selected
    else:
        deselector(selectionlist, poslist)


def main():
    # load the icon to display up on the top left
    icon, icon_rect = load.image('cursor.bmp', WHITE)
    pygame.display.set_icon(icon)

    # pretty background
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    screen.blit(background, (0, 0))

    # construct some test game objects
    test1 = entities.Item('button_unpressed_green-240x60.bmp')
    test2 = entities.Item('menu.bmp')
    test3 = entities.Item('button_unpressed_red-52x60.bmp')
    items = pygame.sprite.RenderClear((test1, test2, test3))
    posdisplays = pygame.sprite.RenderClear()
    selections = pygame.sprite.RenderClear()
    clock = pygame.time.Clock()

    # FPS info
    fps = entities.TextFPS(clock, 24, BLACK)

    # dragbox
    selectbox = None

    # main loop
    while True:
        clock.tick(60)

        for e in pygame.event.get():

            # ===========================================================
            # -------------------- MOUSE BUTTON DOWN --------------------
            # ===========================================================
            if e.type == MOUSEBUTTONDOWN:

                # ====================== LEFT CLICK =====================
                if e.button == 1:
                    no_select = True
                    pos = pygame.mouse.get_pos()

                    for item in reversed(items.sprites()):
                        if item.rect.collidepoint(pos):
                            selectbot(selections, posdisplays, item)
                            no_select = False
                            break

                    if no_select:
                        selectbox = entities.SelectBox()

            # ===========================================================
            # --------------------- MOUSE BUTTON UP ---------------------
            # ===========================================================
            elif e.type == MOUSEBUTTONUP:
                for item in selections.sprites():
                    item.ref.ungrab()

                if selectbox:
                    result = []

                    for item in items.sprites():
                        if selectbox.rect.colliderect(item.rect):
                            result.append(item)
                    screen.blit(background, selectbox.rect, selectbox.rect)
                    selectbox = None

                    if result:
                        selectbot(selections, posdisplays, result)
                    else:
                        selectbot(selections, posdisplays)

            # ===========================================================
            # ------------------------- KEY DOWN ------------------------
            # ===========================================================
            elif e.type == KEYDOWN:

                # ======================== DELETE =======================
                if e.key == K_DELETE:
                    for item in selections.sprites():
                        item.ref.kill()

                    selections.empty()
                    posdisplays.empty()

                # ======================== ESCAPE =======================
                elif e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # ===========================================================
            # --------------------------- QUIT --------------------------
            # ===========================================================
            elif e.type == QUIT:
                pygame.quit()
                sys.exit()

        # clear necessary wizzles
        items.clear(screen, background)
        posdisplays.clear(screen, background)
        screen.blit(background, fps.rect, fps.rect)
        if selectbox:
            screen.blit(background, selectbox.rect, selectbox.rect)

        items.update()
        posdisplays.update()
        selections.update()
        fps.update()

        # redraw the shizzles
        items.draw(screen)
        selections.draw(screen)
        posdisplays.draw(screen)
        screen.blit(fps.image, fps.rect)
        if selectbox:
            selectbox.update()
            screen.blit(selectbox.image, selectbox.rect)

        # update
        pygame.display.update()

if __name__ == "__main__":
    main()
