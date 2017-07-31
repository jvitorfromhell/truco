import cards, player

class Play:
    def __init__(self, player):
        self.player = player

class CallPlay(Play):
    pass

class CardPlay(Play):
    pass

class Game:
    def __init__(self, players):
        self.players = players
        self.scores = [0 for _ in range(len(self.players))]
        self.deck = cards.Deck()
        self.deck.shuffle()
        self.deck.deal(self.players)

    def update(self, play):
        return True
