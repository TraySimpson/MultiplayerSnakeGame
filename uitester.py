import configparser
from gamecontroller import GameController
from graphicswindow import GraphicsWindow
from player import Player
import asyncio

async def main():
    global config 
    config = configparser.ConfigParser()
    config.read('config.ini')
    tickTime = .2

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
        for player in players:
            if (gameController.has_player_lost(player)):
                graphics.remove_player(player)
                players.remove(player)
                break
            await asyncio.sleep(tickTime)
            point = gameController.get_random_move(player)
            await gameController.move_player(point, player)
            if (gameController.has_player_lost(player)):
                players.remove(player)
                graphics.remove_player(player)
                break
            graphics.update_graphics(gameController.get_map())
    print("Game over!")
    graphics.get_click_point()

asyncio.run(main())