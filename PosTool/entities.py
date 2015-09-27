import load
import pygame
from screen import screen
from pygame.locals import *

# global settings
# TODO: move this back into main.py
grid_size = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


class Item(pygame.sprite.Sprite):
    """A game object class for cases where objects need to be clicked,
    dragged, and move based on cursor position"""

    def __init__(self, name, colorkey=BLACK):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load.image(name, colorkey)
        self.original = self.image
        self.grabbed = False
        self.name = name
        self.selected = False

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


class Select(pygame.sprite.Sprite):
    """Draw a selection box around objects"""

    def __init__(self, border=2):
        pygame.sprite.Sprite.__init__(self)

        self.image.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.image.get_rect()
        self.border = border

    def update(self):
        half = self.border / 2

        rect = (0, 0, self.rect.width-half,
                self.rect.height-half)
        pygame.draw.rect(self.image, BLUE, rect, self.border)


class SelectItem(Select):

    def __init__(self, refobj, border=2):
        self.ref = refobj
        self.image = pygame.Surface(self.ref.image.get_size())
        super(SelectItem, self).__init__(border)

    def update(self):
        if not self.rect.topleft == self.ref.rect.topleft:
            self.rect.topleft = self.ref.rect.topleft
            super(SelectItem, self).update()


class SelectBox(Select):
    """drag and drop UI to select stuffs in an area"""

    def __init__(self, border=2):
        self.pos_origin = pygame.mouse.get_pos()
        self.image = pygame.Surface((0, 0))
        super(SelectBox, self).__init__(border)

    def update(self):
        pos = pygame.mouse.get_pos()
        x = self.pos_origin[0]
        y = self.pos_origin[1]
        width = pos[0] - self.pos_origin[0]
        height = pos[1] - self.pos_origin[1]

        if height < 0:
            height = abs(height)
            y -= height

        if width < 0:
            width = abs(width)
            x -= width

        self.image = pygame.Surface((width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        super(SelectBox, self).update()


class Text(pygame.sprite.Sprite):
    """generates text surfaces/rects/sprites"""

    def __init__(self, size, color, background):
        # initiate pygame.sprite
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.background = background
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render('...', True, color)
        self.rect = self.image.get_rect()


class TextPos(Text):
    """Displays position information relative to the given reference object
    in the form of text on the topright corner of the object."""

    def __init__(self, gameobj, size=18, color=WHITE, background=BLACK):
        super(TextPos, self).__init__(size, color, background)
        self.ref = gameobj

    def update(self):
        # update & position
        x, y = self.ref.rect.x, self.ref.rect.y
        text = '{}, {}'.format(x, y)
        self.image = self.font.render(text, True, self.color, self.background)
        self.rect.x, self.rect.y = x, y
