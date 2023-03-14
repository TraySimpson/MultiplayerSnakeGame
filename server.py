import socketserver
from gamecontroller import GameController
from player import Player

class Server(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print(self.data)
        data = self.data.decode("utf-8").split("$")
        action = data[0]
        player = Player.decode(data[1])
        print(f"Player: {player}")
        if (action == "spawn"):
            gameController.spawn_player(player)
        elif (action == "move"):
            gameController.move_player(player.position, player)
        self.request.sendall(self.data.upper())

if (__name__ == "__main__"):
    global gameController
    gameController = GameController()

    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), Server)
    server.serve_forever()