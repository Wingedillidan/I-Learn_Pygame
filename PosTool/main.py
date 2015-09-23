import pygame
import load
import sys
from screen import screen
from pygame.locals import *

# global settings
grid_size = 10


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

            self.rect.topleft = gridx, gridy

    def grab(self):
        self.grabbed = True

        # dx, dy enable the object to be moved smoothly and without it
        # jumping to a preset movement point (uhhh, do I need this comment?)
        pos = pygame.mouse.get_pos()
        self.dx = pos[0] - self.rect.x
        self.dy = pos[1] - self.rect.y

    def ungrab(self):
        self.grabbed = False


class EntityPos(pygame.sprite.Sprite):
    """Displays position information relative to the given reference object
    in the form of text on the topright corner of the object."""

    def __init__(self, gameobj):
        pygame.sprite.Sprite.__init__(self)

        self.ref = gameobj
        self.font = pygame.font.Font(None, 18)
        self.image = self.font.render('???', True, (0, 0, 0))
        self.rect = self.image.get_rect()

    def update(self):
        # set coloring
        background = (0, 0, 0)
        color = (255, 255, 255)

        # update & position
        x, y = self.ref.rect.x, self.ref.rect.y
        text = '{}, {}'.format(x, y)
        self.image = self.font.render(text, True, color, background)
        self.rect.x, self.rect.y = x, y


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
clock = pygame.time.Clock()

# FPS info
fps_font, fps_surf, fps_rect = None, None, None

if pygame.font:
    fps_font = pygame.font.Font(None, 32)
    fps_surf = fps_font.render('FPS: ???', True, (0, 0, 0))
    fps_rect = fps_surf.get_rect()

# main loop
while True:
    clock.tick(60)

    for e in pygame.event.get():
        # did a thing get grabbed?
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()
            sprite_count = len(testgroup.sprites())

            # check which object got grabbed
            # TO DO: fix grabbing to select the topmost object first
            for i in xrange(0, sprite_count):
                thing = testgroup.sprites()[sprite_count-i-1]

                if thing.rect.collidepoint(pos):
                    thing.grab()
                    testgrouppos.add(EntityPos(thing))
                    break

        # keydown case group
        elif e.type == KEYDOWN:

            # should I display all positional data?
            if e.key == K_LCTRL:
                for thing in testgroup.sprites():
                    testgrouppos.add(EntityPos(thing))

        # keyup case group
        elif e.type == KEYUP:
            if e.key == K_LCTRL:
                testgrouppos.empty()
            elif e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        # test case for removing stuff
        # will break if clicked 4 times
        elif e.type == MOUSEBUTTONDOWN and e.button == 3:
            testgroup.remove(testgroup.sprites()[0])

        # did grabbing stop?
        elif e.type == MOUSEBUTTONUP:
            for thing in testgroup.sprites():
                thing.ungrab()

            if len(testgrouppos.sprites()) == 1:
                testgrouppos.empty()

        elif e.type == QUIT:
            pygame.quit()
            sys.exit()

    # clear necessary wizzles
    testgroup.clear(screen, background)
    testgrouppos.clear(screen, background)
    screen.blit(background, fps_rect, fps_rect)

    # update the shizzle wizzles
    testgroup.update()
    testgrouppos.update()
    fps_surf = fps_font.render('FPS: ' + str(int(clock.get_fps())),
                               True, (0, 0, 0))
    fps_rect = fps_surf.get_rect()

    # redraw the shizzles
    testgroup.draw(screen)
    testgrouppos.draw(screen)
    screen.blit(fps_surf, fps_rect)

    # update
    pygame.display.update()
