import socketserver
import ast
from gamecontroller import GameController
from observer import Observer
from player import Player

def main():
    global gameController
    gameController = GameController()

    global clients
    clients = []

    global nextClientPort
    nextClientPort = 9000

    HOST, PORT = "localhost", 9000
    server = socketserver.TCPServer((HOST, PORT), Server)
    server.serve_forever()

def add_client(source, address):
    gameController.add_observer(Observer(source, port=get_next_port(), host=address))
    clients.append(source)
    print(f"Client added: {source}")

def get_next_port():
    global nextClientPort
    nextClientPort += 1
    return nextClientPort

def get_config_message():
    return {
        "port": nextClientPort,
        "mapSize": gameController.mapSize,
        "cellLifetime": gameController.cellLifetime,
        "obstacles": gameController.get_obstacles()
    }

class Server(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        data = self.data.decode("utf-8")
        data = ast.literal_eval(data)
        # print(data)
        action = data["action"]
        print(action)
        source = data["source"]
        match(action):
            case "handshake":
                add_client(source, str(self.client_address))
                self.request.sendall(bytes(f"{get_config_message()}", 'utf-8'))
            case "spawn":
                player = Player.decode(data["player"])
                gameController.spawn_player(player, source)
            case "move":
                player = Player.decode(data["player"])
                point = (0,1)
                gameController.move_player(point, player, source)
        # self.request.sendall(b"Good")

if (__name__ == "__main__"):
    main()