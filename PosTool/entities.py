import load
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


class ItemPlain(pygame.sprite.DirtySprite):
    """A game object that is nothing but a solid color rect"""

    def __init__(self, grid, colorkey, name=None, size_x=100, size_y=100):
        pygame.sprite.DirtySprite.__init__(self)
        if name:
            self.image, self.rect = load.image(name, colorkey)
        else:
            self.image = pygame.Surface((size_x, size_y))
            self.rect = self.image.get_rect()
        self.grid = grid


class ItemMenuBlock(ItemPlain):
    """The base for the right-click menu"""

    def __init__(self, grid, size_x):
        super(ItemMenuBlock, self).__init__(grid, None, None, size_x)


class Item(ItemPlain):
    """A game object class for cases where objects need to be clicked,
    dragged, and move based on cursor position"""

    def __init__(self, name, grid, colorkey=BLACK):
        super(Item, self).__init__(grid, colorkey, name)
        self.original = self.image
        self.grabbed = False
        self.selected = False
        self.nudge = None
        self.dirty = 1

        # where the cursor is in relation to the object's top left pixel
        self.dx = 0
        self.dy = 0

    def nudger(self):
        self.dirty = 1
        x, y = 0, 0

        for direction in self.nudge:
            if direction is 'left':
                x -= self.grid
            elif direction is 'right':
                x += self.grid
            elif direction is 'up':
                y -= self.grid
            elif direction is 'down':
                y += self.grid

        self.rect = self.rect.move(x, y)

    def update(self):
        if self.grabbed:
            self.dirty = 1
            pos = pygame.mouse.get_pos()
            gridx = pos[0]-self.dx
            gridy = pos[1]-self.dy

            if self.grid > 1:
                gridx = gridx - (gridx % self.grid)
                gridy = gridy - (gridy % self.grid)

            if not self.rect.topleft == (gridx, gridy):
                self.rect.topleft = gridx, gridy
        elif self.nudge:
            self.nudger()
            self.nudge = None

    def grab(self):
        self.grabbed = True

        # dx, dy enable the object to be moved smoothly and without it
        # jumping to a preset movement point (uhhh, do I need this comment?)
        pos = pygame.mouse.get_pos()
        self.dx = pos[0] - self.rect.x
        self.dy = pos[1] - self.rect.y

    def ungrab(self):
        self.grabbed = False


class Select(pygame.sprite.DirtySprite):
    """Draw a selection box around objects"""

    def __init__(self, border=2):
        pygame.sprite.DirtySprite.__init__(self)

        self.image.set_colorkey(BLACK, RLEACCEL)
        self.rect = self.image.get_rect()
        self.border = border
        self.dirty = 1

    def update(self):
        self.dirty = 1
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


class Text(pygame.sprite.DirtySprite):
    """generates text surfaces/rects/sprites"""

    def __init__(self, text, size, color, font=None):
        # initiate pygame.sprite
        pygame.sprite.DirtySprite.__init__(self)

        self.color = color
        self.text = text
        self.dirty = 1
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect()


class TextMenu(Text):
    """the textisms located within the menus"""

    color_hovered = (225, 225, 255)
    color_unhovered = (175, 175, 175)

    def __init__(self, text, size, width, color=BLACK, font=None):
        super(TextMenu, self).__init__(text, size, color, font)
        self.raw_image = pygame.Surface((width, size))
        self.raw_image.fill(self.color_unhovered)
        self.image = self.font.render(self.text, True, color)
        temprect = self.image.get_rect()

        self.raw_image.blit(self.image, temprect)
        self.image = self.raw_image
        self.rect = self.image.get_rect()
        self.hovered = False
        self.disabled = False

    def hover(self):
        if not self.hovered:
            self.raw_image.fill(self.color_hovered)
            self.raw_image.blit(self.text, self.rect)
            self.image = self.raw_image

            self.dirty = 1

    def unhover(self):
        if self.hovered:
            self.raw_image.fill(self.color_unhovered)
            self.raw_image.blit(self.text, self.rect)
            self.image = self.raw_image

            self.dirty = 1


class TextFPS(Text):
    """updates the fps information"""

    def __init__(self, clock, size, color, font=None, text='...'):
        super(TextFPS, self).__init__(text, size, color, font)
        self.ref = clock

    def update(self):
        self.dirty = 1
        self.text = "FPS: " + str(int(self.ref.get_fps()))
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()


class TextPos(Text):
    """Displays position information relative to the given reference object
    in the form of text on the topright corner of the object."""

    def __init__(self, gameobj, size, color,
                 background, font=None, text='...'):
        super(TextPos, self).__init__(text, size, color, font)
        self.ref = gameobj
        self.background = background

    def update(self):
        self.dirty = 1

        # update & position
        x, y = self.ref.rect.x, self.ref.rect.y
        self.text = '{}, {}'.format(x, y)
        self.image = self.font.render(self.text, True, self.color,
                                      self.background)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
