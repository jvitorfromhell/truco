import socket, select, string, sys, time
import cards, player, game


#main function
if __name__ == "__main__":
    print "Truco 1v1 em Rede!"
    
    # Criar socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Informar IP de conexao com o servidor
    print "Informe o IP do servidor: "     
    host = raw_input()

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
    localGame = game.clientGame('connected')

    while localGame.getState() != 'terminate':
        localGame.evaluateGameState(s)
    
    print "Jogo encerrado e conexao desfeita"
    s.close()
    sys.exit()
