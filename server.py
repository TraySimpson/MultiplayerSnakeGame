from tcpreciever import TCPReceiver 
from gamecontroller import GameController
import socketserver

def main():
    clients = []
    gameController = GameController()
    
    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), TCPReceiver)
    server.serve_forever()


if (__name__ == "__main__"):
    main()