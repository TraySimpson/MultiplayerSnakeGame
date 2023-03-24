from array import *
from util import *
from gamecontroller import GameController, ObserverGameController
from observer import Observer
from player import Player
from tcpsender import TCPSender
from graphicscontroller import GraphicsController
import configparser
import asyncio

async def main():
    global config 
    config = configparser.ConfigParser()
    config.read('config.ini')

    allowMultiplayer = config["GAMEPLAY"]["ALLOW_MULTIPLAYER"] == "yes"

    player = get_player_from_input()

    gameController = ObserverGameController() if allowMultiplayer else GameController()
    spawnPoint = gameController.get_open_spawn_point()
    
    listenPort = 0
    if (allowMultiplayer):
        message = { "action": "handshake"}
        sender = TCPSender()
        observer = Observer()
        message = observer.prepare_data(message)
        response = await sender.send_data(message)
        listenPort = int(response["port"])
        load_config_from_data(response)
        gameController.load_config_from_data(response)

        message = observer.prepare_data({
            "action": "spawn",
            "player": player.encode(),
        })
        response = await sender.send_data(message)
        print(f"Spawn player response: {response}")
        spawnPoint = response["point"]

        observer.set_sender(sender)
        gameController.add_observer(observer)

    await gameController.spawn_player(player, point=spawnPoint)
    graphics = GraphicsController()
    graphics.add_player(player)
    graphics.draw_graphics(gameController.get_map())
    # await check_click(win, gameController, player)
    # asyncio.create_task(check_msg(listenPort))
    while(not gameController.is_game_over()):
        print("update?")
        await wait_for_update(graphics, gameController, player, listenPort)
        print(f"Triggered an update cycle!")
        graphics.update_graphics(gameController.get_map())
    print("Game over!")
    graphics.get_click_point()

async def check_msg(port):
    print(f"Listening for  on port: {port}")
    server = await asyncio.start_server(handle_client, "localhost", port)
    print("Listener set")
    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):
    print("Handling data!")
    data = (await reader.read(255)).decode()
    writer.write(str(data).encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def check_click(win, gameController, player):
    print("Listening for clicks")
    clickPoint = win.get_click_point()
    if (gameController.player_can_move_to(clickPoint, player)):
        await gameController.move_player(clickPoint, player)

async def wait_for_update(win, gameController, player, port):
    tasks = [
        # asyncio.create_task(check_msg(port)),
        asyncio.create_task(check_click(win, gameController, player))
    ]

    # with asyncio.FIRST_COMPLETED, this triggers as soon as one of the events is fired
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    task = done.pop().result()

    # cancel the other check
    for future in pending:
        future.cancel()

    print(f"Task finished, returned: {task}")

def load_config_from_data(data):
    config["GAMEPLAY"]["CELL_LIFETIME"]
    config["GAMEPLAY"]["MAP_SIZE"]

def get_player_from_input():
    return Player("player1")
    playerName = input("Enter player name:")
    return Player(playerName)

asyncio.run(main(), debug=True)