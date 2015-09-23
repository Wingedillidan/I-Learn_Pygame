import pygame
import load
import sys
import pdb
from screen import screen
from pygame.locals import *


class Entity(pygame.sprite.Sprite):

    def __init__(self, name, colorkey=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load.image(name, colorkey)
        self.original = self.image
        self.grabbed = False
        self.name = name
        self.dx = 0
        self.dy = 0

        # font information
        self.font = pygame.font.Font(None, 18)
        self.font_surface = None
        self.font_rect = None

    def position(self):
        """Displays the object's position information in the top left corner
        of the object"""
        if self.font_surface:
            self.image.blit(self.original, self.font_rect, self.font_rect)

        text = '{}, {}'.format(str(self.rect.x), str(self.rect.y))
        self.font_surface = self.font.render(text, True, (255, 255, 255))
        self.font_rect = self.font_surface.get_rect()
        self.image.blit(self.font_surface, self.font_rect)

    def update(self):
        if self.grabbed:
            pos = pygame.mouse.get_pos()
            offset = (pos[0]-self.dx, pos[1]-self.dy)

            self.rect.topleft = offset
            self.position()

    def grab(self):
        self.grabbed = True

        pos = pygame.mouse.get_pos()
        self.dx = pos[0] - self.rect.x
        self.dy = pos[1] - self.rect.y

    def ungrab(self):
        self.grabbed = False


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
clock = pygame.time.Clock()

# FPS info
fps_font, fps_surf, fps_rect = None, None, None

if pygame.font:
    fps_font = pygame.font.Font(None, 32)
    fps_surf = fps_font.render('FPS: ???', True, (0, 0, 0))
    fps_rect = fps_surf.get_rect()

while True:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()

            for thing in testgroup.sprites():
                if thing.rect.collidepoint(pos):
                    thing.grab()
                    break
        elif e.type == MOUSEBUTTONDOWN and e.button == 3:
            testgroup.remove(testgroup.sprites()[0])
        elif e.type == MOUSEBUTTONUP:
            for thing in testgroup.sprites():
                thing.ungrab()
        elif e.type == KEYUP and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == QUIT:
            sys.exit()

    # clear necessary wizzles
    testgroup.clear(screen, background)
    screen.blit(background, fps_rect, fps_rect)

    # update the shizzle wizzles
    testgroup.update()
    fps_surf = fps_font.render('FPS: ' + str(int(clock.get_fps())),
                               True, (0, 0, 0))
    fps_rect = fps_surf.get_rect()

    # redraw the shizzles
    testgroup.draw(screen)
    screen.blit(fps_surf, fps_rect)

    pygame.display.update()
