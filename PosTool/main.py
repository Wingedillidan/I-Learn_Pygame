import pygame
import load
import sys
from screen import screen
from pygame.locals import *

# global settings
grid_size = 5

# global constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Entity(pygame.sprite.Sprite):
    """A game object class for cases where objects need to be clicked,
    dragged, and move based on cursor position"""

    def __init__(self, name, colorkey=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load.image(name, colorkey)
        self.original = self.image
        self.grabbed = False
        self.name = name

        # where the cursor is in relation to the object's top left pixel
        self.dx = 0
        self.dy = 0

    def update(self):
        if self.grabbed:
            pos = pygame.mouse.get_pos()
            gridx = pos[0]-self.dx
            gridy = pos[1]-self.dy

            if grid_size > 1:
                gridx = gridx - (gridx % grid_size)
                gridy = gridy - (gridy % grid_size)

            if not self.rect.topleft == (gridx, gridy):
                old_rect = self.rect.copy()
                self.rect.topleft = gridx, gridy
                return old_rect, self.rect

    def grab(self):
        self.grabbed = True

        # dx, dy enable the object to be moved smoothly and without it
        # jumping to a preset movement point (uhhh, do I need this comment?)
        pos = pygame.mouse.get_pos()
        self.dx = pos[0] - self.rect.x
        self.dy = pos[1] - self.rect.y

    def ungrab(self):
        self.grabbed = False


class Entity_Text(pygame.sprite.Sprite):
    """generates text surfaces/rects/sprites"""

    def __init__(self, size, color, background):
        # initiate pygame.sprite
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.background = background
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render('...', True, color)
        self.rect = self.image.get_rect()


class EntityPos(Entity_Text):
    """Displays position information relative to the given reference object
    in the form of text on the topright corner of the object."""

    def __init__(self, gameobj, size=18, color=WHITE, background=BLACK):
        super(EntityPos, self).__init__(size, color, background)
        self.ref = gameobj

    def update(self):
        # update & position
        x, y = self.ref.rect.x, self.ref.rect.y
        text = '{}, {}'.format(x, y)
        self.image = self.font.render(text, True, self.color, self.background)
        self.rect.x, self.rect.y = x, y


class EntitySelect(pygame.sprite.Sprite):

    def __init__(self, gameobj):
        pygame.sprite.Sprite.__init__(self)

        self.ref = gameobj
        self.image = pygame.Surface(self.ref.image.get_size())
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()

    def update(self):
        if not self.rect.topleft == self.ref.rect.topleft:
            self.rect.topleft = self.ref.rect.topleft
            rect = (0, 0, self.rect.width-1, self.rect.height-1)

            pygame.draw.rect(self.image, (0, 0, 255), rect, 2)


def main():
    # load the icon to display up on the top left
    icon, icon_rect = load.image('cursor.bmp', (255, 255, 255))
    pygame.display.set_icon(icon)

    # pretty background
    background = pygame.Surface(screen.get_size())
    background.fill((225, 225, 225))
    screen.blit(background, (0, 0))

    # construct some test game objects
    test1 = Entity('button_unpressed_green-240x60.bmp')
    test2 = Entity('menu.bmp')
    test3 = Entity('button_unpressed_red-52x60.bmp')
    testgroup = pygame.sprite.RenderClear((test1, test2, test3))
    testgrouppos = pygame.sprite.RenderClear()
    testgroupselect = pygame.sprite.RenderClear()
    clock = pygame.time.Clock()

    # FPS info
    fps_font, fps_surf, fps_rect = None, None, None
    fps_font = pygame.font.Font(None, 32)
    fps_surf = fps_font.render('FPS: ???', True, (0, 0, 0))
    fps_rect = fps_surf.get_rect()

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
                    testgroupselect.empty()

                    # check which object got grabbed
                    # TO DO: fix grabbing to select the topmost object first
                    for i in xrange(sprite_count):
                        thing = testgroup.sprites()[sprite_count-i-1]

                        if thing.rect.collidepoint(pos):
                            thing.grab()
                            testgroupselect.add(EntitySelect(thing))
                            testgrouppos.add(EntityPos(thing))
                            break

            # ========== MOUSE UNCLICKED EVENTS ==========
            elif e.type == MOUSEBUTTONUP:

                # did grabbing stop?
                for thing in testgroup.sprites():
                    thing.ungrab()

                if len(testgrouppos.sprites()) == 1:
                    testgrouppos.empty()

            # ============ KEY PRESSED EVENTS ============
            elif e.type == KEYDOWN:

                # should I display all positional data?
                if e.key == K_LCTRL:
                    for thing in testgroup.sprites():
                        testgrouppos.add(EntityPos(thing))

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
        screen.blit(background, fps_rect, fps_rect)

        testgroup.update()
        testgrouppos.update()
        testgroupselect.update()
        fps_surf = fps_font.render('FPS: ' + str(int(clock.get_fps())),
                                   True, (0, 0, 0))
        fps_rect = fps_surf.get_rect()

        # redraw the shizzles
        testgroup.draw(screen)
        testgroupselect.draw(screen)
        testgrouppos.draw(screen)
        screen.blit(fps_surf, fps_rect)

        # update
        pygame.display.update()

if __name__ == "__main__":
    main()
