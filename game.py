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

class clientGame:
    def __init__(self):
        self.state = "waitingServer"
        self.cards = []

    def start(self, message):
        self.state = message
        print "Oponente conectado, inicializando jogo\n"

    def round(self, message):
        message = message.split("\n")
        self.state = message[1]
        print "Inicio de rodada"
        print "Sua mao tem: " + message[2] + ", " + message[3] + " e " + message[4]

    def getOppPlay(self, message):
        print "Seu oponente jogou: " + message
        self.state = "active"

    def getPlayResult(self, message):
        print message
        self.state = 'terminate'

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def evaluateMessage(self, message):
        if 'terminate' in message:
            self.state = 'terminate'
        else:
            self.state = message


class serverGame:
    def __init__(self):
        self.state = None
        self.firstPlayer = None
        self.activePlayer = None
        self.inactivePlayer = None
        self.playedCard = None
        self.winner = None

        self.deck = cards.Deck()
        self.hands = [[], []]

    def startGame(self, sockets):
        self.state = 'gameSetup'
        self.firstPlayer = random.randint(0, 1)
        self.sendMessages(sockets)

    def round(self):
        if self.state != 'gameSetup':
            self.firstPlayer = self.swapFirst()
        self.state = 'roundBegin'
        self.activePlayer = self.firstPlayer
        self.inactivePlayer = (self.activePlayer + 1) % 2
        self.deck.shuffle()
        self.deck.deal(self.hands)

    def getState(self):
        return self.state

    def getActivePlayer(self):
        return self.activePlayer

    def getInactivePlayer(self):
        return self.inactivePlayer

    def swapFirst(self):
        self.firstPlayer = (self.firstPlayer + 1) % 2

    def swapActive(self):
        self.activePlayer = (self.activePlayer + 1) % 2
        self.inactivePlayer = (self.inactivePlayer + 1) % 2

    def handMessage(self, playerID):
        msg = str(self.hands[playerID][0]) + "\n" 
        msg = msg + str(self.hands[playerID][1]) + "\n" 
        msg = msg + str(self.hands[playerID][2]) + "\n"
        return msg

    def evaluateMessage(self, message):
        if 'terminate' in message:
            self.state = 'terminate'
        
        elif self.state == 'roundBegin':
            self.state = 'getRes'
            self.playedCard = self.hands[self.activePlayer][int(message)]

        elif self.state == 'getRes':
            self.state = 'sendRes'        
            self.winner = self.winsPlay(self.playedCard, self.hands[self.inactivePlayer][int(message)])
            
    def sendMessages(self, sockets):
        if self.state == 'gameSetup':
            for s in sockets:
                s.send(self.state)
                time.sleep(2)
        
        elif self.state == 'roundBegin':
            sockets[self.activePlayer].send(self.state + '\nactive\n' + 
                                            self.handMessage(self.activePlayer))
            sockets[self.inactivePlayer].send(self.state + '\ninactive\n' + 
                                              self.handMessage(self.inactivePlayer))
        elif self.state == 'getRes':
            sockets[self.inactivePlayer].send(str(self.playedCard))

        elif self.state == 'sendRes':
            if self.winner != None:
                sockets[self.winner].send("Voce venceu!")
                sockets[(self.winner + 1) % 2].send("Voce perdeu!")
            else:
                for s in sockets:
                    s.send("Empardou!")
                time.sleep(2)

    def winsPlay(self, cardA, cardB):
        if cardA.getScore() < cardB.getScore():
            return self.activePlayer
        elif cardA.getScore() > cardB.getScore():
            return self.inactivePlayer
        else:
            return None

# class Game:
#     def __init__(self):
#         self.playerA = None
#         self.playerB = None
#         self.activePlayer = None
#         self.trucoLevel = 0
#         self.invidoOn = False
#         self.florOn = False
#         self.scores = []
#         self.roundScores = []
#         self.deck = None
#         self.state = "start"
#         self.playState = None
#         self.winner = None

#     def startGame(self, pA, pB):
#         self.playerA = pA
#         self.playerB = pB
#         self.deck = cards.Deck()
#         self.scores = [0, 0]
#         self.startRound()
#         self.deck.shuffle()
#         self.deck.deal([self.playerA, self.playerB])
#         self.activePlayer = random.randint(0, 1)

#     def setState(self, newState):
#         self.state = newState

#     def startState(self):
#         return self.state == "start"

#     def waitingState(self):
#         return self.state == "waiting"

#     def playingState(self):
#         return self.state == "playing"

#     def endState(self):
#         return self.state == "end"

#     def terminateState(self):
#         return self.state == "terminate"

#     def winsPlay(self, cardA, cardB):
#         if cardA.getScore() < cardB.getScore():
#             return 1
#         elif cardA.getScore() > cardB.getScore():
#             return -1
#         else:
#             return 0

#     def swapActive(self):
#         self.activePlayer = (self.activePlayer + 1) % 2

#     def clickHandler(self, mousepos, IP):
#         if self.startState() and clickInsideButton(mousepos, buttons["connect"]):
#             self.setState("waiting")
    
#         # TEMPORARY
#         elif self.waitingState():
#             self.setState("playing")
        
#         # TEMPORARY
#         elif self.playingState() and self.activePlayer.isThisMe(IP):
#             if clickInsideButton(mousepos, buttons["truco"]):
#                 pass
#             elif clickInsideButton(mousepos, buttons["invido"]):
#                 pass
#             elif clickInsideButton(mousepos, buttons["carta0"]):
#                 pass
#             elif clickInsideButton(mousepos, buttons["carta1"]):
#                 pass
#             elif clickInsideButton(mousepos, buttons["carta2"]):
#                 pass

        
#         elif game.endState() and clickInsideButton(mousepos, buttons["playAgain"]):
#             self.setState("waiting")
            
#         elif game.endState() and clickInsideButton(mousepos, buttons["quit"]):
#             self.setState("terminate")

#     def gameStateToString(self):
#         pass

#     def stringToGameState(self, string):
#         pass

#     def updateGameState(self):
#         pass

# def drawStartScreen(display, game):
#     # Logo
#     #logo = pygame.image.load('logo.png')
#     #display.blit(logo, (200, 100))
#     pygame.draw.rect(display, (0, 0, 0), (200, 50, 624, 300))

#     # Text
#     pygame.draw.rect(display, (0, 0, 0), (200, 450, 624, 50))

#     # Input
#     pygame.draw.rect(display, (0, 0, 0), (200, 510, 624, 50))

#     # Button
#     pygame.draw.rect(display, (0, 0, 0), buttons["connect"])


# def drawWaitingConnectionScreen(display, game):
#     # Waiting Connection Image
#     pygame.draw.rect(display, (0, 0, 0), (200, 100, 624, 558))

# def drawMainGameScreen(display, game, mousepos):
#     # Card Hover
#     if (hoverArea(mousepos, buttons["carta0"])):
#         pygame.draw.rect(display, (200, 0, 0), buttons["carta0"])
#     if (hoverArea(mousepos, buttons["carta1"])):
#         pygame.draw.rect(display, (200, 0, 0), buttons["carta1"])
#     if (hoverArea(mousepos, buttons["carta2"])):
#         pygame.draw.rect(display, (200, 0, 0), buttons["carta2"])

  
#     # Card
#     pygame.draw.rect(display, (255, 255, 255), (110, 434, 132, 250))
#     pygame.draw.rect(display, (255, 255, 255), (335, 434, 132, 250))
#     pygame.draw.rect(display, (255, 255, 255), (560, 434, 132, 250))

#     # Buttons
#     pygame.draw.rect(display, (0, 0, 0), buttons["truco"])
#     pygame.draw.rect(display, (0, 0, 0), buttons["invido"])
#     pygame.draw.rect(display, (0, 0, 0), buttons["flor"])

# def drawEndGameScreen(display, game):
#     pass

# def drawTerminateGameScreen(display, game):
#     sleep(3)
#     pygame.quit()
#     sys.exit()

# def hoverArea(mousepos, area):
#     return mousepos[0] > area[0] and mousepos[0] < area[0] + area[2] and mousepos[1] > area[1] and mousepos[1] < area[1] + area[3]

# def clickInsideButton(mousepos, button):
#     return mousepos[0] > button[0] and mousepos[0] < button[0] + button[2] and mousepos[1] > button[1] and mousepos[1] < button[1] + button[3]