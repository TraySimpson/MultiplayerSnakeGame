import asyncio, socket, ast
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

    asyncio.run(run_server())

async def run_server():
    HOST, PORT = "localhost", 9000
    server = await asyncio.start_server(handle_client, HOST, PORT)
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        data = (await reader.read(255)).decode()
        data = ast.literal_eval(data)
        action = data["action"]
        print(action)
        source = data["source"]
        response = {"status": "good"}
        match(action):
            case "handshake":
                address = writer.get_extra_info('peername')
                add_client(source, address)
                response = get_handshake_config()
            case "spawn":
                player = Player.decode(data["player"])
                await gameController.spawn_player(player, source)
            case "move":
                player = Player.decode(data["player"])
                point = (0,1)
                await gameController.move_player(point, player, source)
        print(f"Sending back response: {response}")
        writer.write(str(response).encode())
        await writer.drain()
    writer.close()
    await writer.wait_closed()

def add_client(source, address):
    gameController.add_observer(Observer(source, port=get_next_client_port(), host=address))
    clients.append(source)
    print(f"Client added: {source}")

def get_next_client_port():
    global nextClientPort
    nextClientPort += 1
    return nextClientPort

def get_handshake_config():
    config = gameController.get_config()
    config["port"] = nextClientPort
    return config

if (__name__ == "__main__"):
    main()