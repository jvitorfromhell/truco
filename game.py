import cards, player
import pygame, time, random

buttons = { "connect"   : (400, 600, 224, 100),
            "truco"     : (800, 424, 150, 70),
            "invido"    : (800, 524, 150, 70),
            "flor"      : (800, 624, 150, 70),
            "carta0"    : (100, 424, 152, 270),
            "carta1"    : (325, 424, 152, 270),
            "carta2"    : (550, 424, 152, 270),
            "playAgain" : 0,
            "quit"      : 0}

class Game:
    def __init__(self):
        self.playerA = None
        self.playerB = None
        self.activePlayer = None
        self.trucoOn = False
        self.retrucoOn = False
        self.vale4On = False
        self.invidoOn = False
        self.florOn = False
        self.scores = []
        self.roundScores = []
        self.deck = None
        self.state = "start"
        self.playState = None
        self.winner = None

    def startGame(self, pA, pB):
        self.playerA = pA
        self.playerB = pB
        self.deck = cards.Deck()
        self.scores = [0, 0]
        self.startRound()
        self.deck.shuffle()
        self.deck.deal([self.playerA, self.playerB])
        self.activePlayer = random.randint(0, 1)

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

    def terminateState(self):
        return self.state == "terminate"

    def winsPlay(self, cardA, cardB):
        if cardA.getScore() < cardB.getScore():
            return 1
        elif cardA.getScore() > cardB.getScore():
            return -1
        else:
            return 0

    def swapActive(self):
        self.activePlayer = (self.activePlayer + 1) % 2

    def clickHandler(self, mousepos, IP):
        if self.startState() and clickInsideButton(mousepos, buttons["connect"]):
            self.setState("waiting")
    
        # TEMPORARY
        elif self.waitingState():
            self.setState("playing")
        
        # TEMPORARY
        elif self.playingState() and self.activePlayer.isThisMe(IP):
            if clickInsideButton(mousepos, buttons["truco"]):
                pass
            elif clickInsideButton(mousepos, buttons["invido"]):
                pass
            elif clickInsideButton(mousepos, buttons["carta0"]):
                pass
            elif clickInsideButton(mousepos, buttons["carta1"]):
                pass
            elif clickInsideButton(mousepos, buttons["carta2"]):
                pass

        
        elif game.endState() and clickInsideButton(mousepos, buttons["playAgain"]):
            self.setState("waiting")
            
        elif game.endState() and clickInsideButton(mousepos, buttons["quit"]):
            self.setState("terminate")

    def gameStateToString(self):
        pass

    def stringToGameState(self, string):
        pass

    def updateGameState(self):
        pass

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

def drawTerminateGameScreen(display, game):
    sleep(3)
    pygame.quit()
    sys.exit()

def hoverArea(mousepos, area):
    return mousepos[0] > area[0] and mousepos[0] < area[0] + area[2] and mousepos[1] > area[1] and mousepos[1] < area[1] + area[3]

def clickInsideButton(mousepos, button):
    return mousepos[0] > button[0] and mousepos[0] < button[0] + button[2] and mousepos[1] > button[1] and mousepos[1] < button[1] + button[3]