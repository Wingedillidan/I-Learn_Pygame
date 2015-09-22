import pygame
import load
import sys
from screen import screen
from pygame.locals import *


class Entity(pygame.sprite.Sprite):

    def __init__(self, name, colorkey=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load.image(name, colorkey)
        self.grabbed = False
        self.name = name

    def update(self):
        if self.grabbed:
            pos = pygame.mouse.get_pos()
            self.rect.center = pos
        else:
            return False

icon, icon_rect = load.image('cursor.bmp', (255, 255, 255))
pygame.display.set_icon(icon)

background = pygame.Surface(screen.get_size())
background.fill((225, 225, 225))
screen.blit(background, (0, 0))

test1 = Entity('button_unpressed_green-240x60.bmp')
test2 = Entity('menu.bmp')
test3 = Entity('button_unpressed_red-52x60.bmp')
testgroup = pygame.sprite.RenderClear((test1, test2, test3))
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == KEYUP and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == QUIT:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()

            for thing in testgroup.sprites():
                if thing.rect.collidepoint(pos):
                    thing.grabbed = True
                    break
        elif e.type == MOUSEBUTTONUP:
            for thing in testgroup.sprites():
                thing.grabbed = False

    testgroup.clear(screen, background)
    testgroup.update()
    testgroup.draw(screen)

    pygame.display.update()
