# Imports
import sys
import cards, player, game
from pygame.locals import *
from game import *

# Window Startup
pygame.init()
display = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Truco')

# Game Startup
truco = Game()

# Game Loop
while True:
    display.fill((39, 119, 20))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickHandler(truco, pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            print "UP"
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if truco.startState():
        drawStartScreen(display, truco)
    if truco.waitingState():
        drawWaitingConnectionScreen(display, truco)
    if truco.playingState():
        drawMainGameScreen(display, truco, pygame.mouse.get_pos())
    if truco.endState():
        drawEndGameScreen(display, truco)
    
    pygame.display.update()