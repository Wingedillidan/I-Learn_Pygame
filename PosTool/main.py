import pygame
import load
import sys
import entities
import menu
from screen import screen
from pygame.locals import *

pygame.init()

# global settings
grid_size = 10

# global constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main():
    # load the icon to display up on the top left
    icon, icon_rect = load.image('cursor.bmp', WHITE)
    pygame.display.set_icon(icon)

    # pretty background
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    screen.blit(background, (0, 0))
    pygame.display.update()

    # construct some test game objects
    test1 = entities.Item('button_unpressed_green-240x60.bmp', grid_size)
    test2 = entities.Item('menu.bmp', grid_size)
    test3 = entities.Item('button_unpressed_red-52x60.bmp', grid_size)
    items = pygame.sprite.RenderUpdates((test1, test2, test3))
    for i in xrange(25):
        thing = entities.Item('button_unpressed_red-52x60.bmp', grid_size)
        items.add(thing)
    posdisplays = pygame.sprite.RenderUpdates()
    selections = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    # dirty rects
    dirtyitems = []
    dirtyselections = []
    dirtypos = []
    dirtystats = []

    # FPS info
    fps = entities.TextFPS(clock, 24, BLACK)

    # dragbox
    selectbox = None

    # delays
    nudge_delay = 0

    # main loop
    while True:
        clock.tick(60)

        # ===============================================================
        # ------------------------- HOLDED KEYS -------------------------
        # ===============================================================

        if selections.sprites():
            if not nudge_delay:
                keys = pygame.key.get_pressed()
                result = []

                # ====================== MOVEMENTZ ======================
                if keys[K_LEFT] or keys[K_a]:
                    result.append('left')
                if keys[K_RIGHT] or keys[K_d]:
                    result.append('right')
                if keys[K_UP] or keys[K_w]:
                    result.append('up')
                if keys[K_DOWN] or keys[K_s]:
                    result.append('down')

                for item in selections.sprites():
                    item.ref.nudge = result

                nudge_delay = 3
            else:
                nudge_delay -= 1

        for e in pygame.event.get():
            # ===========================================================
            # -------------------- MOUSE BUTTON DOWN --------------------
            # ===========================================================
            if e.type == MOUSEBUTTONDOWN:
                nudge_delay = 3

                # ==================== LEFT CLICK ===================
                if e.button == 1:
                    keys = pygame.key.get_pressed()
                    ctrl = False
                    no_select = True
                    pos = pygame.mouse.get_pos()

                    if keys[K_LCTRL]:
                        ctrl = True

                    for item in reversed(items.sprites()):
                        if item.rect.collidepoint(pos):
                            load.selectbot(selections, posdisplays, item, ctrl)
                            no_select = False
                            break

                    if no_select:
                        selectbox = entities.SelectBox()

                # =================== RIGHT CLICK ===================
                if e.button == 3:
                    menu.right_click(['test'])

            # ===========================================================
            # --------------------- MOUSE BUTTON UP ---------------------
            # ===========================================================
            elif e.type == MOUSEBUTTONUP:
                for item in selections.sprites():
                    item.ref.ungrab()

                if selectbox:
                    keys = pygame.key.get_pressed()
                    ctrl = False
                    result = []

                    for item in items.sprites():
                        if selectbox.rect.colliderect(item.rect):
                            result.append(item)

                    screen.blit(background, selectbox.rect, selectbox.rect)
                    selectbox = None

                    if keys[K_LCTRL]:
                        ctrl = True
                    load.selectbot(selections, posdisplays, result, ctrl)

            # ===========================================================
            # ------------------------- KEY DOWN ------------------------
            # ===========================================================
            elif e.type == KEYDOWN:

                # ====================== DELETE =====================
                if e.key == K_DELETE:
                    for item in selections.sprites():
                        item.ref.kill()

                    selections.empty()
                    posdisplays.empty()

                # ====================== ESCAPE =====================
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
            dirtystats = [selectbox.rect, None]
            screen.blit(background, selectbox.rect, selectbox.rect)

        items.update()
        posdisplays.update()
        selections.update()
        fps.update()

        dirtyitems = items.draw(screen)
        dirtyselections = selections.draw(screen)
        dirtypos = posdisplays.draw(screen)
        screen.blit(fps.image, fps.rect)
        if selectbox:
            selectbox.update()
            dirtystats[1] = selectbox.rect
            screen.blit(selectbox.image, selectbox.rect)

        # update
        pygame.display.update(dirtyitems)
        pygame.display.update(dirtypos)
        pygame.display.update(dirtyselections)
        pygame.display.update(dirtystats)

if __name__ == "__main__":
    main()
