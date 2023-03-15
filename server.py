import socketserver
import ast
from gamecontroller import GameController

def main():
    global gameController
    gameController = GameController()

    global clients
    clients = []

    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), Server)
    server.serve_forever()

def add_client(client):
    clients.append(client)

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
                pass
            case "spawn":
                pass
            case "move":
                pass
        self.request.sendall("Good")

if (__name__ == "__main__"):
    main()