import player
import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        #self.sprite = sprite

    def __str__(self):
        return str(self.value) + " " + self.suit

class Deck:
    def __init__(self):
        self.cards = [Card(v, s) for v in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12] for s in ['spades', 'clubs', 'coins', 'cups']]

    def deal(self, players):
        indexes = random.sample(range(0, len(self.cards) - 1), len(players) * 3)
        for i in range(len(players)):
            players[i].addCard(self.cards[indexes[i * 3]])
            players[i].addCard(self.cards[indexes[i * 3 + 1]])
            players[i].addCard(self.cards[indexes[i * 3 + 2]])

    def shuffle(self):
        random.shuffle(self.cards)