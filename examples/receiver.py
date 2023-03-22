import socket
from exampleutil import *

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5005

def main():
    protocol = select_protocol()
    print_status(protocol, TARGET_IP, TARGET_PORT)
    if (protocol == 'udp'):
        listen_udp()
    else:
        listen_tcp()

def listen_udp():
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.bind((TARGET_IP, TARGET_PORT))

    print("Listening...")
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print(f"Received UDP message: {data}")

def listen_tcp():
    BUFFER_SIZE = 128

    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # TCP
    sock.bind((TARGET_IP, TARGET_PORT))
    sock.listen(1)

    conn, addr = sock.accept()
    print("Listening...")
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print(f"Received UDP message: {data}")
        conn.send(data)  # echo same data back
        print(f"Sent response: {data}")
    conn.close()

main()