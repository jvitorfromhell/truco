import socket, select, string, sys
import cards, player, game


#main function
if __name__ == "__main__":
    print "Truco 1v1 em Rede!"
    
    # Criar socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Informar IP de conexao com o servidor
    #print "Informe o IP do servidor: "     
    host = "192.168.1.103" #raw_input()

    # Tentar conexao
    try:
        s.connect((host, 5000))
    except:
        print 'Conexao nao estabelecida'
        sys.exit()

    # Verificar se ainda existe slot para jogador
    data = s.recv(4096)
    if 'denied' in data:
        print 'Partida em andamento, nao ha espaco para novos jogadores'
        s.close()
        sys.exit()

    print "Conectado, aguardando servidor estabelecer conexao com outro jogador e inicializar estado de jogo"

    s.settimeout(None)
    localGame = game.clientGame()
    localGame.start(s.recv(4096))

    while localGame.getState() != 'terminate':
        if localGame.getState() == 'gameSetup':
            localGame.round(s.recv(4096))
        
        elif localGame.getState() == 'active':
            print "Qual carta voce quer jogar? (0, 1, 2)"
            action = int(raw_input())
            while (action < 0 or action > 2):
                print "INVALIDO"
                action = int(raw_input())
            s.send(str(action))
            print "Aguardando jogada do seu oponente"
            localGame.setState('waitingPlayResult')

        elif localGame.getState() == 'inactive':
            print "Voce eh o jogador inativo, esperando jogada do oponente"
            localGame.getOppPlay(s.recv(4096))

        else:
            localGame.getPlayResult(s.recv(4096))
            s.send('terminate')
    
    print "Jogo encerrado e conexao desfeita"
    s.close()
    sys.exit()