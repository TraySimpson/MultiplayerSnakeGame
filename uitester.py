import configparser
from gamecontroller import GameController
from graphicswindow import GraphicsWindow
from player import Player
import asyncio

async def main():
    global config 
    config = configparser.ConfigParser()
    config.read('config.ini')
    tickTime = .5

    gameController = GameController()
    graphics = GraphicsWindow()
    players = []

    for i in range(4):
        player = Player(f"player{i}")
        spawnPoint = gameController.get_open_spawn_point()
        await gameController.spawn_player(player, point=spawnPoint)
        graphics.add_player(player)
        players.append(player)

    graphics.draw_graphics(gameController.get_map())
    while(not gameController.is_game_over()):
        print(f"Turn {gameController._turn}")
        for player in players:
            await asyncio.sleep(tickTime)
            point = gameController.get_random_move(player)
            await gameController.move_player(point, player)
            graphics.update_graphics(gameController.get_map())
    print("Game over!")
    # Stall
    graphics.get_click_point()

asyncio.run(main())