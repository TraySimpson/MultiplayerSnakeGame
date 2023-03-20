import socket
import ast
import asyncio

class TCPSender:
    def __init__(self, port=9000, host="localhost") -> None:
        self.host = host
        self.port = port

    def set_port(self, port):
        self.port = port

    async def send_data(self, data: dict):
        reader, writer = await asyncio.open_connection(
            self.host, self.port)

        print("Sending data!")
        writer.write(str(data).encode())
        await writer.drain()

        received = await reader.read(255)
        received = received.decode()
        print(f'Received: {received}')

        print('Close the connection')
        writer.close()
        await writer.wait_closed()
        if (received is not None and received != ''):
            return ast.literal_eval(received)