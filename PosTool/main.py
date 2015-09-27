import pygame
import load
import sys
import entities
from screen import screen
from pygame.locals import *

# TODO: Rather than basing selection status in a list, make it so that the
# status is only updated via the Item.selection boolean

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

    # construct some test game objects
    test1 = entities.Item('button_unpressed_green-240x60.bmp')
    test2 = entities.Item('menu.bmp')
    test3 = entities.Item('button_unpressed_red-52x60.bmp')
    testgroup = pygame.sprite.RenderClear((test1, test2, test3))
    testgrouppos = pygame.sprite.RenderClear()
    testgroupselect = pygame.sprite.RenderClear()
    clock = pygame.time.Clock()

    # FPS info
    fps_font, fps_surf, fps_rect = None, None, None
    fps_font = pygame.font.Font(None, 32)
    fps_surf = fps_font.render('FPS: ???', True, BLACK)
    fps_rect = fps_surf.get_rect()

    # dragbox
    selectbox = None

    # main loop
    while True:
        clock.tick(60)

        for e in pygame.event.get():

            # =========== MOUSE CLICKED EVENTS ===========
            if e.type == MOUSEBUTTONDOWN:

                # did a thing get grabbed?
                if e.button == 1:
                    pos = pygame.mouse.get_pos()
                    sprite_count = len(testgroup.sprites())

                    # check which object got grabbed
                    # TO DO: fix grabbing to select the topmost object first
                    for i in xrange(sprite_count):
                        thing = testgroup.sprites()[sprite_count-i-1]

                        if thing.rect.collidepoint(pos):
                            if not thing.selected:
                                for selection in testgroupselect.sprites():
                                    selection.ref.selected = False

                                testgroupselect.empty()

                            testgroupselect.add(entities.SelectItem(thing))
                            testgrouppos.add(entities.TextPos(thing))
                            thing.selected = True

                            for thing in testgroupselect.sprites():
                                thing.ref.grab()
                            break

                        # if nothing was selected, do a dragbox
                        elif i == sprite_count-1:
                            selectbox = entities.SelectBox()

            # ========== MOUSE UNCLICKED EVENTS ==========
            elif e.type == MOUSEBUTTONUP:

                # did grabbing stop?
                for thing in testgroup.sprites():
                    thing.ungrab()

                if len(testgrouppos.sprites()) == 1:
                    testgrouppos.empty()

                if selectbox:
                    no_select = True
                    for thing in testgroup.sprites():
                        if selectbox.rect.colliderect(thing):
                            testgroupselect.add(entities.SelectItem(thing))
                            thing.selected = True
                            no_select = False

                    if no_select:
                        for thing in testgroupselect.sprites():
                            thing.selected = False

                        testgroupselect.empty()

                    selectbox = None

            # ============ KEY PRESSED EVENTS ============
            elif e.type == KEYDOWN:

                # display all positional data
                if e.key == K_LCTRL:
                    for thing in testgroup.sprites():
                        testgrouppos.add(entities.TextPos(thing))

                # delete stuff
                if e.key == K_DELETE:
                    for thing in testgroupselect.sprites():
                        thing.ref.kill()

                    testgroupselect.empty()

            # =========== KEY UNPRESSED EVENTS ===========
            elif e.type == KEYUP:
                if e.key == K_LCTRL:
                    testgrouppos.empty()
                elif e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # =============== OTHER EVENTS ===============
            elif e.type == QUIT:
                pygame.quit()
                sys.exit()

        # clear necessary wizzles
        testgroup.clear(screen, background)
        testgrouppos.clear(screen, background)
        screen.blit(background, fps_rect)
        if selectbox:
            screen.blit(background, selectbox.rect, selectbox.rect)

        testgroup.update()
        testgrouppos.update()
        testgroupselect.update()
        fps_surf = fps_font.render('FPS: ' + str(int(clock.get_fps())),
                                   True, BLACK)
        fps_rect = fps_surf.get_rect()

        # redraw the shizzles
        testgroup.draw(screen)
        testgroupselect.draw(screen)
        testgrouppos.draw(screen)
        screen.blit(fps_surf, fps_rect)
        if selectbox:
            selectbox.update()
            screen.blit(selectbox.image, selectbox.rect)

        # update
        pygame.display.update()

if __name__ == "__main__":
    main()
