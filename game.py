import cards, player
import pygame, time, random

# Estados onde o servidor envia a mesma mensagem para todos
broadcast_states = ['connected', 'gameSetup', 'roundContinue']

# Placar para final de jogo
final_score = 3

# clientGame : versao do jogo que lida com as acoes no lado cliente
class clientGame:
    # Metodo construtor
    def __init__(self, s):
        self.state = s
        self.player = None

    # Retorna estado atual
    def getState(self):
        return self.state

    # Atualiza Estado de Jogo
    def evaluateGameState(self, s):
        # Estado conectado, aguardando inicializacao
        if self.state == 'connected':
            message = s.recv(4096)
            print "Oponente conectado, servidor inicializando o jogo"
            self.state = 'gameSetup'

        # Estado inicializado, aguardando rodada
        elif self.state == 'gameSetup':
            message = s.recv(4096)
            print "Jogo inicializado"
            self.start()
            self.state = 'roundBegin'

        # Inicio de rodada
        elif self.state == 'roundBegin':
            message = s.recv(4096)
            self.roundBegin(message)
            self.state = 'getPlayStatus'

        # Aguardando pra saber se eh o jogador ativo ou inativo
        elif self.state == 'getPlayStatus':
            self.state = s.recv(4096)

        # Jogador ativo
        elif self.state == 'active':
            print "Voce eh o jogador ativo. Qual carta deseja jogar?"
            play = int(raw_input())
            while (play < 0 or play > self.player.numCards()):
                print "INVALIDO"
                play = int(raw_input())
            self.player.play(play, s)
            print "Jogada enviada, aguardando resposta do seu oponente."
            self.state = 'waitingOppPlay'

        # Esperando responsta do oponente
        elif self.state == 'waitingOppPlay':
            play = s.recv(4096)
            print "Seu oponente jogou: " + play
            self.state = 'waitingPlayResult'

        # Jogador inativo
        elif self.state == 'inactive':
            print "Voce eh o jogador inativo, esperando jogada do oponente"
            self.state = 'waitingPlay'

        # Aguardando jogada
        elif self.state == 'waitingPlay':
            play = s.recv(4096)
            print "Seu oponente jogou: " + play
            self.state = 'respond'

        # Respondendo jogada
        elif self.state == 'respond':
            print "Qual carta deseja jogar?"
            play = int(raw_input())
            while (play < 0 or play > self.player.numCards()):
                print "INVALIDO"
                play = int(raw_input())
            self.player.play(play, s)
            print "Jogada enviada, aguardando servidor processar resultado"
            self.state = 'waitingPlayResult'

        # Aguardando resultado da jogada
        elif self.state == 'waitingPlayResult':
            result = s.recv(4096)
            if 'winner' in result:
                print "Voce venceu!"
            elif 'loser' in result:
                print "Voce perdeu ):"
            else:
                print "Empardou!"
            self.state = 'waitRoundUpdate'

        # Aguarda status do round
        elif self.state == 'waitRoundUpdate':
            update = s.recv(4096)
            if 'roundContinue' in update:
                print "A rodada continua!\n"
                self.state = 'roundContinue'
            else:
                if 'winner' in update:
                    print "Voce venceu a rodada!"
                else:
                    print "Voce perdeu a rodada"
                self.state = 'roundEnd'

        # Segue round
        elif self.state == 'roundContinue':
            self.player.printCards()
            self.state = 'getPlayStatus'

        # Termina round
        elif self.state == 'roundEnd':
            self.state = 'getGameResults'

        # Verifica estado do jogo
        elif self.state == 'getGameResults':
            results = s.recv(4096)
            if 'winner' in results:
                print "Voce venceu o jogo!"
                self.state = 'terminate'
            elif 'loser' in results:
                print "Voce perdeu o jogo!"
                self.state = 'terminate'
            else:
                print "O jogo continua! O placar eh " + results
                self.state = 'roundBegin'

    # Inicializa jogo, a nivel local
    def start(self):
        self.player = player.Player()

    # Inicializa rodada, a nivel local
    def roundBegin(self, message):
        print "\nInicio de rodada.\n"
        message = message.split('\n')
        self.player.round(message)
        self.player.printCards()


# serverGame : versao do jogo que lida com as acoes no lado servidor
class serverGame:
    
    # Metodo construtor
    def __init__(self, s):
        # Atributos relacionados ao jogo inteiro
        self.state = s
        self.deck = cards.Deck()
        self.scores = [0, 0]
        self.firstPlayer = None

        # Atributos relacionados a uma rodada
        self.roundScore = [0, 0]
        self.roundValue = 1
        self.roundPlays = 0
        self.winners = [None, None, None]

        # Atributos relacionados a uma jogada
        self.activePlayer = None
        self.inactivePlayer = None
        self.playedCard = None
        self.winner = None

    # Retorna estado de jogo
    def getState(self):
        return self.state

    # Avalia estado de jogo
    def evaluateGameState(self, sockets):

        # Estado conectado
        if self.state == 'connected':
            self.sendMessages(sockets)
            self.state = 'gameSetup'

        # Estado de inicializacao
        elif self.state == 'gameSetup':
            self.sendMessages(sockets)
            self.startGame()
            self.state = 'roundBegin'

        # Estado de inicio de rodada
        elif self.state == 'roundBegin':
            self.sendMessages(sockets)
            self.roundBegin()
            self.state = 'sendPlayStatus'

        # Envia mensagem de status de jogador a ambos jogadores
        elif self.state == 'sendPlayStatus':
            self.sendMessages(sockets)
            self.state = 'waitingPlay1'

        # Verifica se o round terminou
        elif self.state == 'updateRoundResults':
            # Condicao de vitoria 1 : score == 2
            if max(self.roundScore) == 2:
                self.winner = 0 if self.roundScore[0] == 2 else 1
                self.state = 'roundEnd'
            
            # Ocorreu empate
            elif (self.roundPlays > 1) and (None in self.winners[:self.roundPlays]):
                # Descobre primeiro vencedor
                firstWinner = None
                
                for winner in self.winners[:self.roundPlays]:
                    if winner != None:
                        firstWinner = winner
                        break

                # Se ha primeiro vencedor, ele vence a rodada
                if firstWinner != None:
                    self.winner = firstWinner
                    self.state = 'roundEnd'
                    
                # Se nao ha primeiro vencedor, mas as 3 jogadas ja aconteceram, vence o mao (quem comecou)
                elif self.roundPlays == 3:
                    self.winner = self.firstPlayer
                    self.state = 'roundEnd'
                
                # Segue round
                else:
                    self.state = 'roundConinue'

            # Segue round    
            else:
                self.state = 'roundContinue'

        # Segue o round
        elif self.state == 'roundContinue':
            self.sendMessages(sockets)
            self.state = 'sendPlayStatus'
            if self.winner != None:
                self.activePlayer = self.winner
                self.inactivePlayer = (self.winner + 1) % 2

        # Finaliza o round
        elif self.state == 'roundEnd':
            self.sendMessages(sockets)
            self.scores[self.winner] = self.scores[self.winner] + self.roundValue
            if max(self.scores) == final_score:
                self.state = 'endGame'
                self.winner = 0 if self.scores[0] == final_score else 1
            else:
                self.state = 'sendScores'

        # Envia scores e comeca novo round
        elif self.state == 'sendScores':
            self.sendMessages(sockets)
            self.firstPlayer = (self.firstPlayer + 1) % 2
            self.state = 'roundBegin'

        # Finaliza o jogo
        elif self.state == 'endGame':
            self.sendMessages(sockets)
            self.state = 'terminate'

    # Avalia mensagem recebida
    def evaluateMessage(self, message):
        
        # Recebeu mensagem do jogador ativo
        if self.state == 'waitingPlay1':
            self.playedCard = message

        elif self.state == 'waitingPlay2':
            self.evaluatePlay(message.split(" "))
            self.playedCard = message
            self.state = 'sendPlayResult'

    # Envia mensagens para os jogadores
    def sendMessages(self, sockets):
        if self.state in broadcast_states:
            for s in sockets:
                s.send(self.state)
                time.sleep(0.1)

        elif self.state == 'roundBegin':
            hands = self.deck.deal()
            
            for i in range(2):
                message = str(hands[i][0]) + "\n" + str(hands[i][1]) + "\n" + str(hands[i][2])
                sockets[i].send(message)

        elif self.state == 'sendPlayStatus':
            sockets[self.activePlayer].send('active')
            sockets[self.inactivePlayer].send('inactive')

        elif self.state == 'waitingPlay1':
            sockets[self.inactivePlayer].send(self.playedCard)
            self.playedCard = self.playedCard.split(" ")
            self.state = 'waitingPlay2'

        elif self.state == 'sendPlayResult':
            sockets[self.activePlayer].send(self.playedCard)
            time.sleep(0.05)
            if self.winner != None:
                sockets[self.winner].send('winner')
                sockets[(self.winner + 1) % 2].send('loser')
            else:
                for s in sockets:
                    s.send('draw')
                    time.sleep(0.1)
            self.roundPlays = self.roundPlays + 1
            self.state = 'updateRoundResults'

        elif self.state == 'roundEnd':
            sockets[self.winner].send('winner')
            sockets[(self.winner + 1) % 2].send('loser')

        elif self.state == 'sendScores':
            for i in range(2):
                sockets[i].send(str(self.scores[i]) + "x" + str(self.scores[(i + 1) % 2]))
                time.sleep(0.1)
        
        elif self.state == 'endGame':
            sockets[self.winner].send('winner')
            sockets[(self.winner + 1) % 2].send('loser')

    # Inicializa jogo a nivel servidor
    def startGame(self):
        self.firstPlayer = random.randint(0, 1)
        self.scores = [0, 0]

    # Inicializa rodada a nivel servidor
    def roundBegin(self):
        self.activePlayer = self.firstPlayer
        self.inactivePlayer = (self.activePlayer + 1) % 2
        self.roundScore = [0, 0]
        self.roundValue = 1
        self.roundPlays = 0
        self.winners = [None, None, None]
        self.deck.shuffle()

    # Avalia a jogada de duas cartas
    def evaluatePlay(self, answerCard):
        cardA = cards.Card(int(self.playedCard[0]), self.playedCard[1])
        cardB = cards.Card(int(answerCard[0]), answerCard[1])

        if cardA.getScore() < cardB.getScore():
            self.winner = self.activePlayer
            self.roundScore[self.winner] = self.roundScore[self.winner] + 1
        elif cardA.getScore() > cardB.getScore():
            self.winner = self.inactivePlayer
            self.roundScore[self.winner] = self.roundScore[self.winner] + 1
        else:
            self.winner = None

        self.winners[self.roundPlays] = self.winner