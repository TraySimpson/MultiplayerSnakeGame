import socketserver
import ast
from gamecontroller import GameController
from observer import Observer

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
    gameController.add_observer(Observer(source, get_next_port(), address))
    clients.append(source)

def get_next_port():
    global nextClientPort
    nextClientPort += 1
    return nextClientPort

class Server(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        data = self.data.decode("utf-8")
        print(data)
        data = ast.literal_eval(data)
        print(data)
        action = data["action"]
        print(action)
        match(action):
            case "handshake":
                add_client(data["source"], self.client_address)
                self.request.sendall(bytes(f"{nextClientPort}", 'utf-8'))
            case "spawn":
                pass
            case "move":
                pass
        # self.request.sendall(b"Good")

if (__name__ == "__main__"):
    main()