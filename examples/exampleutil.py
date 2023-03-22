def select_protocol():
    protocol = input("Type 'udp' or 'tcp':")
    while(protocol != 'udp' and protocol != 'tcp'):
        print(f"Invalid response: {protocol}")
        protocol = input("Type 'udp' or 'tcp':")
    return protocol

def print_status(protocol, ip, port, message=None):
    print(f"Protocol: {protocol}")
    print(f"Target IP: {ip}")
    print(f"Target port: {port}")
    if (message != None):
        print(f"Message: {message}")