import socket, select, random, time, sys
import cards, player, game

if __name__ == "__main__":
    # Variaveis auxiliares
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000

    # Inicializar socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Adiciona socket local a lista de sockets que a aplicacao escuta
    CONNECTION_LIST.append(server_socket)

    print "Servidor de jogo inicializado na porta " + str(PORT)

    # Escuta socket ate que dois jogadores estejam conectados
    while len(CONNECTION_LIST) < 3:
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])
        sockfd, addr = server_socket.accept()

        CONNECTION_LIST.append(sockfd)
        print "Jogador (%s, %s) conectado" % addr	   
        sockfd.send('accepted')

    print "Dois jogadores conectados, inicializando o jogo e enviando mensagem de inicializacao para ambos"

    centralGame = game.serverGame('connected')

    print "Game Loop"

    while centralGame.getState() != 'terminate':
        centralGame.evaluateGameState(CONNECTION_LIST[1:3])

        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[], 0.5)

        if read_sockets:
            for sock in read_sockets:
                # Tentativa de conexao com servidor lotado, negar
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    sockfd.send('denied')
                    sockfd.close()

                # Mensagem chegou de algum jogador, atualizar jogo
                else:
                    centralGame.evaluateMessage(sock.recv(4096))
                    centralGame.sendMessages(CONNECTION_LIST[1:3])

    # Fechando sockets e terminando conexao
    print "Jogo encerrado e conexoes desfeitas"
    for socket in CONNECTION_LIST:
        socket.close()
    sys.exit()
 