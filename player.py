import cards

class Player:
    def __init__(self):
        self.cards = []
        self.invido = False
        self.invidoValue = None
        self.flor = False
        self.florValue = None

    def getCards(self):
        return self.cards

    def toString(self):
        pass

    def addCard(self, card):
        self.cards.append(card)

    def hasPair(self):
        return self.cards[0].getSuit() == self.cards[1].getSuit() or self.cards[0].getSuit() == self.cards[2].getSuit() or self.cards[1].getSuit() == self.cards[2].getSuit()

    def getPair(self):
        if self.cards[0].getSuit() == self.cards[1].getSuit():
            return [self.cards[0], self.cards[1]] 
        elif self.cards[0].getSuit() == self.cards[2].getSuit():
            return [self.cards[0], self.cards[2]] 
        else:   
            return [self.cards[1], self.cards[2]] 

    def hasInvido(self):
        return self.invido

    def getInvidoValue(self):
        return self.invidoValue

    def defineInvido(self):
        if not self.flor:
            if self.hasPair():
                pair = self.getPair()
                self.invido = True
                self.invidoValue = 20 + sum([pair[i].getValue() if not pair[i].isFag() else 0 for i in range(len(pair))])
            else:
                self.invido = False
                self.invidoValue = 0   

    def hasFlor(self):
        return self.flor

    def getFlorValue(self):
        return self.florValue

    def defineFlor(self):
        if self.cards[0].getSuit() == self.cards[1].getSuit() and self.cards[0].getSuit() == self.cards[2].getSuit():
            self.flor = True
            self.florValue = 20 + sum([self.cards[i].getValue() if not self.cards[i].isFag() else 0 for i in range(len(self.cards))])
        else:
            self.flor = False
            self.florValue = 0

    def isThisMe(self, IP):
        return self.IP == IP