import socketserver

class TCPReceiver(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        data = self.data.decode("utf-8")
        print(data)
        # action = data[0]
        # player = Player.decode(data[1])
        # print(f"Player: {player}")
        # if (action == "spawn"):
        #     gameController.spawn_player(player)
        # elif (action == "move"):
        #     gameController.move_player(player.position, player)
        # self.request.sendall(self.data.upper())