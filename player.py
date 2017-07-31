import cards

class Player:
    def __init__(self, name):
        self.name = name
        self.hiddenCards = []
        self.revealedCards = []

    def addCard(self, card):
        self.hiddenCards.append(card)