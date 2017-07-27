# Imports
import pygame, sys
import cards, player, game
from pygame.locals import *

# Window Startup
pygame.init()
display = pygame.display.set_mode((1024, 768))
display.fill((0, 255, 0))
pygame.display.set_caption('Truco')

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
