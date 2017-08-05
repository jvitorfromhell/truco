import player
import random

cardValues = {  (1, 'spades')  : 1,
                (1, 'clubs')   : 2,
                (7, 'spades')  : 3,
                (7, 'coins')   : 4,
                (3, 'spades')  : 5,
                (3, 'clubs')   : 5,
                (3, 'coins')   : 5,
                (3, 'cups')    : 5,
                (2, 'spades')  : 6,
                (2, 'clubs')   : 6,
                (2, 'coins')   : 6,
                (2, 'cups')    : 6,
                (1, 'coins')   : 7,
                (1, 'cups')    : 7,
                (12, 'spades') : 8,
                (12, 'clubs')  : 8,
                (12, 'coins')  : 8,
                (12, 'cups')   : 8,
                (11, 'spades') : 9,
                (11, 'clubs')  : 9,
                (11, 'coins')  : 9,
                (11, 'cups')   : 9,
                (10, 'spades') : 10,
                (10, 'clubs')  : 10,
                (10, 'coins')  : 10,
                (10, 'cups')   : 10,
                (7, 'clubs')   : 11,
                (7, 'cups')    : 11,
                (6, 'spades')  : 12,
                (6, 'clubs')   : 12,
                (6, 'coins')   : 12,
                (6, 'cups')    : 12,
                (5, 'spades')  : 13,
                (5, 'clubs')   : 13,
                (5, 'coins')   : 13,
                (5, 'cups')    : 13,
                (4, 'spades')  : 14,
                (4, 'clubs')   : 14,
                (4, 'coins')   : 14,
                (4, 'cups')    : 14
                }

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.score = cardValues[(self.value, self.suit)]

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def getScore(self):
        return self.score

    def isFag(self):
        return self.value == 10 or self.value == 11 or self.value == 12

class Deck:
    def __init__(self):
        self.cards = [Card(v, s) for v in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12] for s in ['spades', 'clubs', 'coins', 'cups']]

    def deal(self, players):
        indexes = random.sample(range(0, len(self.cards) - 1), len(players) * 3)
        for i in range(len(players)):
            players[i].addCard(self.cards[indexes[i * 3]])
            players[i].addCard(self.cards[indexes[i * 3 + 1]])
            players[i].addCard(self.cards[indexes[i * 3 + 2]])
            players[i].defineFlor()
            players[i].defineInvido()

    def shuffle(self):
        random.shuffle(self.cards)