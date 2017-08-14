import cards

# Player : armazena informacoes sobre o jogador, usado a nivel cliente para tomar acoes
class Player:
    
    # Metodo construtor
    def __init__(self):
        self.hand = []
        self.canRaise = True
        self.invido = False
        self.flor = False
        self.invidoValue = 0
        self.florValue = 0

    # Inicializa atributos no inicio de uma rodada
    def round(self, card_strings):
        card_list = []
        for card in card_strings:
            card_list.append(card.split(" "))
        
        self.hand = [cards.Card(int(card_list[i][0]), card_list[i][1]) for i in range(3)]

        self.defineFlor()

        if not self.flor:
            self.defineInvido()
        

    # Define se usuario tem Flor (tres cartas do mesmo naipe) e calcula o valor
    def defineFlor(self):
        if self.hand[0].getSuit() == self.hand[1].getSuit() and self.hand[0].getSuit() == self.hand[2].getSuit():
            self.flor = True
            self.florValue = 20 + sum([self.hand[i].getValue() if not self.hand[i].isFag() else 0 for i in range(3)])

    # Define se o usuario tem Invido (duas cartas do mesmo naipe) e calcula valor
    def defineInvido(self):
        if self.hasPair():
            pair = self.getPair()
            self.invido = True
            self.invidoValue = 20 + sum([pair[i].getValue() if not pair[i].isFag() else 0 for i in range(len(pair))])

    # Verifica se o usuario tem um par de cartas do mesmo naipe
    def hasPair(self):
        return self.hand[0].getSuit() == self.hand[1].getSuit() or self.hand[0].getSuit() == self.hand[2].getSuit() or self.hand[2].getSuit() == self.hand[1].getSuit()

    # Encontra par nas cartas
    def getPair(self):
        if self.hand[0].getSuit() == self.hand[1].getSuit():
            return [self.hand[0], self.hand[1]] 
        elif self.hand[0].getSuit() == self.hand[2].getSuit():
            return [self.hand[0], self.hand[2]] 
        else:   
            return [self.hand[1], self.hand[2]] 

    # Getters pra Invido e Flor
    def hasInvido(self):
        return self.invido

    def getInvidoValue(self):
        return self.invidoValue

    def hasFlor(self):
        return self.flor

    def getFlorValue(self):
        return self.florValue

    # Printa acoes possives na tela
    def printActions(self):
        print "1) Jogar carta"

        if self.hasFlor:
            print "2) Chamar Flor"
        else:
            print "2) Chamar Invido"

    # Printa as cartas na tela
    def printCards(self):
        i = 0
        print "Sua mao tem:"
        for card in self.hand:
            print str(i) + ") " + str(card)
            i = i + 1

    # Joga carta : remove carta da mao e envia mensagem ao servidor
    def play(self, index, socket):
        message = str(self.hand[index])
        del self.hand[index]
        socket.send(message)

    # Retorna o numero de cartas na mao
    def numCards(self):
        return len(self.hand)