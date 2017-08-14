import cards

# Player : armazena informacoes sobre o jogador, usado a nivel cliente para tomar acoes
class Player:
    
    # Metodo construtor
    def __init__(self):
        self.hand = []

    # Inicializa atributos no inicio de uma rodada
    def round(self, card_strings):
        card_list = []
        for card in card_strings:
            card_list.append(card.split(" "))
        
        self.hand = [cards.Card(int(card_list[i][0]), card_list[i][1]) for i in range(3)]

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