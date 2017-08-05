import cards, player
import pygame, time

buttons = { "connect"   : (400, 600, 224, 100),
            "truco"     : (800, 424, 150, 70),
            "invido"    : (800, 524, 150, 70),
            "flor"      : (800, 624, 150, 70),
            "carta0"    : (100, 424, 152, 270),
            "carta1"    : (325, 424, 152, 270),
            "carta2"    : (550, 424, 152, 270),
            "playAgain" : 0}

class Game:
    def __init__(self):
        self.state = "start"

    def setState(self, newState):
        self.state = newState

    def startState(self):
        return self.state == "start"

    def waitingState(self):
        return self.state == "waiting"

    def playingState(self):
        return self.state == "playing"

    def endState(self):
        return self.state == "end"

    def gameStateToString(self):
        pass

    def stringToGameState(self):
        pass

    def updateGameState(self):
        pass
        
    #     self.players = players
    #     self.scores = [0 for _ in range(len(self.players))]
    #     self.roundScore = [0 for _ in range(len(self.players))]
    #     self.deck = cards.Deck()

    #     self.deck.shuffle()
    #     self.deck.deal(self.players)

    # def update(self, play):
    #     return True

    # def round(self):
    #     pass

    # def evaluate(self, cardA, cardB):
    #     if cardA.getScore() < cardB.getScore():
    #         return 1
    #     elif cardA.getScore() == cardB.getScore():
    #         return 0
    #     else:
    #         return -1        

def drawStartScreen(display, game):
    # Logo
    #logo = pygame.image.load('logo.png')
    #display.blit(logo, (200, 100))
    pygame.draw.rect(display, (0, 0, 0), (200, 50, 624, 300))

    # Text
    pygame.draw.rect(display, (0, 0, 0), (200, 450, 624, 50))

    # Input
    pygame.draw.rect(display, (0, 0, 0), (200, 510, 624, 50))

    # Button
    pygame.draw.rect(display, (0, 0, 0), buttons["connect"])


def drawWaitingConnectionScreen(display, game):
    # Waiting Connection Image
    pygame.draw.rect(display, (0, 0, 0), (200, 100, 624, 558))

def drawMainGameScreen(display, game, mousepos):
    # Card Hover
    if (hoverArea(mousepos, buttons["carta0"])):
        pygame.draw.rect(display, (200, 0, 0), buttons["carta0"])
    if (hoverArea(mousepos, buttons["carta1"])):
        pygame.draw.rect(display, (200, 0, 0), buttons["carta1"])
    if (hoverArea(mousepos, buttons["carta2"])):
        pygame.draw.rect(display, (200, 0, 0), buttons["carta2"])

  
    # Card
    pygame.draw.rect(display, (255, 255, 255), (110, 434, 132, 250))
    pygame.draw.rect(display, (255, 255, 255), (335, 434, 132, 250))
    pygame.draw.rect(display, (255, 255, 255), (560, 434, 132, 250))

    # Buttons
    pygame.draw.rect(display, (0, 0, 0), buttons["truco"])
    pygame.draw.rect(display, (0, 0, 0), buttons["invido"])
    pygame.draw.rect(display, (0, 0, 0), buttons["flor"])

def drawEndGameScreen(display, game):
    pass

def hoverArea(mousepos, area):
    return mousepos[0] > area[0] and mousepos[0] < area[0] + area[2] and mousepos[1] > area[1] and mousepos[1] < area[1] + area[3]

def clickInsideButton(mousepos, button):
    return mousepos[0] > button[0] and mousepos[0] < button[0] + button[2] and mousepos[1] > button[1] and mousepos[1] < button[1] + button[3]

def clickHandler(game, mousepos):
    if game.startState() and clickInsideButton(mousepos, buttons["connect"]):
        game.setState("waiting")
    
    # TEMPORARY
    elif game.waitingState():
        game.setState("playing")
    
    # TEMPORARY
    elif game.playingState():
        pass
    
    elif game.endState():
        pass