import pygame
import load

pygame.init()

screen = pygame.display.set_mode((1600, 900))
icon, icon_rect = load.image('cursor.bmp', (255, 255, 255))
pygame.display.set_caption('PosTool')
pygame.display.set_icon(icon)
