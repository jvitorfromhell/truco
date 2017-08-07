import player
import random

cardValues = {  (1, 'espadas')  : 1,
                (1, 'paus')   : 2,
                (7, 'espadas')  : 3,
                (7, 'ouro')   : 4,
                (3, 'espadas')  : 5,
                (3, 'paus')   : 5,
                (3, 'ouro')   : 5,
                (3, 'copas')    : 5,
                (2, 'espadas')  : 6,
                (2, 'paus')   : 6,
                (2, 'ouro')   : 6,
                (2, 'copas')    : 6,
                (1, 'ouro')   : 7,
                (1, 'copas')    : 7,
                (12, 'espadas') : 8,
                (12, 'paus')  : 8,
                (12, 'ouro')  : 8,
                (12, 'copas')   : 8,
                (11, 'espadas') : 9,
                (11, 'paus')  : 9,
                (11, 'ouro')  : 9,
                (11, 'copas')   : 9,
                (10, 'espadas') : 10,
                (10, 'paus')  : 10,
                (10, 'ouro')  : 10,
                (10, 'copas')   : 10,
                (7, 'paus')   : 11,
                (7, 'copas')    : 11,
                (6, 'espadas')  : 12,
                (6, 'paus')   : 12,
                (6, 'ouro')   : 12,
                (6, 'copas')    : 12,
                (5, 'espadas')  : 13,
                (5, 'paus')   : 13,
                (5, 'ouro')   : 13,
                (5, 'copas')    : 13,
                (4, 'espadas')  : 14,
                (4, 'paus')   : 14,
                (4, 'ouro')   : 14,
                (4, 'copas')    : 14
                }

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.score = cardValues[(self.value, self.suit)]

    def __str__(self):
        return str(self.value) + " " + self.suit

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def getScore(self):
        return self.score

    def isFag(self):
        return self.value == 10 or self.value == 11 or self.value == 12

    def clone(self):
        return Card(self.value, self.suit)

class Deck:
    def __init__(self):
        self.cards = [Card(v, s) for v in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12] for s in ['espadas', 'paus', 'ouro', 'copas']]

    def deal(self, hands):
        indexes = random.sample(range(0, len(self.cards) - 1), len(hands) * 3)
        for i in range(len(hands)):
            hands[i].append(self.cards[indexes[i * 3]].clone())
            hands[i].append(self.cards[indexes[i * 3 + 1]].clone())
            hands[i].append(self.cards[indexes[i * 3 + 2]].clone())
            #hands[i].defineFlor()
            #hands[i].defineInvido()

    def shuffle(self):
        random.shuffle(self.cards)