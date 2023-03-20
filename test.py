from tcpsender import TCPSender
import asyncio

async def main():
    sender = TCPSender(port=9000)
    message = {
        "action": "handshake",
        "source": "jeff"
        }
    response = await sender.send_data(message)
    listenPort = int(response["port"])
    await run_server(listenPort)

async def run_server(port):
    HOST = "localhost"
    server = await asyncio.start_server(handle_client, HOST, port)
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):
    data = (await reader.read(255)).decode()
    print(f"Got data: {data}")

asyncio.run(main())