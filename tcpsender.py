import socket

class TCPSender:
    def __init__(self) -> None:
        self.host = "localhost"
        self.port = 9999

    def send_data(self, data: dict):
        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((self.host, self.port))
            sock.sendall(bytes(str(data) + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
        # print("Sent:     {}".format(data))
        # print("Received: {}".format(received))