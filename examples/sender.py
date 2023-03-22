import socket
from exampleutil import *

# This could also be "localhost"
TARGET_IP = "127.0.0.1"

# Can be any port not in use
# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
TARGET_PORT = 5005

# Message, in bytes
MESSAGE = b"Hello, World!"

def main():
    protocol = select_protocol()
    print_status(protocol, TARGET_IP, TARGET_PORT, MESSAGE)
    if (protocol == 'udp'):
        send_udp()
    else:
        send_tcp()

def send_udp():
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (TARGET_IP, TARGET_PORT))
    print(f"Sent UDP packet to {TARGET_IP}:{TARGET_PORT}")

def send_tcp():
    BUFFER_SIZE = 128
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
    sock.connect((TARGET_IP, TARGET_PORT))
    sock.send(MESSAGE)
    data = sock.recv(BUFFER_SIZE)
    sock.close()
    print(f"Sent TCP packet to {TARGET_IP}:{TARGET_PORT}")
    print(f"Received response: {data}")

main()
