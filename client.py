from graphics import *
from array import *
from util import *
from gamecontroller import GameController
from observer import Observer
from player import Player
from graphicscell import GraphicsCell
from tcpsender import TCPSender
import math
import configparser
import asyncio

async def main():
    global config 
    config = configparser.ConfigParser()
    config.read('config.ini')

    global backgroundColor
    backgroundColor= "white"

    global obstacleColor
    obstacleColor = "black"

    player = get_player_from_input()

    gameController = GameController()
    spawnPoint = gameController.get_open_spawn_point()
    
    if ((config["GAMEPLAY"]["ALLOW_MULTIPLAYER"]) == "yes"):
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
    win = build_window()
    init_graphics_map(gameController.mapSize, win)
    draw_obstacles(win, gameController.get_map())
    update_graphics(win, gameController.get_map())
    draw_ui(win, player)
    # await check_click(win, gameController, player)
    # asyncio.create_task(check_msg(listenPort))
    while(not gameController.is_game_over()):
        print("update?")
        await wait_for_update(win, gameController, player, listenPort)
        print(f"Triggered an update cycle!")
        update_graphics(win, gameController.get_map())
    print("Game over!")
    win.getMouse()

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
    clickPoint = get_click_point(win)
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
    return Player("player1", (255, 0, 0))
    print("Enter player name:")
    playerName = input()
    print("Choose color:")
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255)
    }
    colorChoice = input()
    color = colors[colorChoice]
    return Player(playerName, color)

def get_click_point(win):
    point = win.getMouse()
    return (math.floor(point.getX()), math.floor(point.getY()))

def build_window():
    width = int(config["GAMEPLAY"]["MAP_SIZE"])
    height = int(config["GAMEPLAY"]["MAP_SIZE"]) + int(config["GRAPHICS"]["UI_BAR_HEIGHT_SCALE"])
    cellSize = int(config["GRAPHICS"]["CELL_GRAPHICS_SIZE"])
    win = GraphWin(width = width * cellSize, height = height * cellSize)
    win.setCoords(0, 0, width, height)
    return win

def init_graphics_map(mapSize, win):
    global graphicsMap
    graphicsMap = [[GraphicsCell(x, y, win, backgroundColor) for y in range(mapSize)] for x in range(mapSize)]

def draw_obstacles(win, map):
    for x, row in enumerate(map):
        for y, cell in enumerate(row):
            if (cell is not None and cell.is_permanent()):
                graphicsMap[x][y] = GraphicsCell(x, y, win, obstacleColor)

def draw_ui(win, player):
    uiY = int(config["GAMEPLAY"]["MAP_SIZE"]) + (float(config["GRAPHICS"]["UI_BAR_HEIGHT_SCALE"]) / 2)
    uiName = Text(Point(1, uiY), player.name)
    uiName.setFill(color_rgb(player.color[0], player.color[1], player.color[2]))
    uiName.draw(win)

def update_graphics(win, map):
    for x, row in enumerate(map):
        for y, cell in enumerate(row):
            graphicsMap[x][y].update_color(get_cell_color(cell), win)

def get_cell_color(cell):
    if (cell is None):
        return backgroundColor
    elif (cell.is_permanent()):
        return obstacleColor
    else:
        color = color_rgb(
            get_rgb_from_turns_left(cell.color[0], cell.turnsLeft),
            get_rgb_from_turns_left(cell.color[1], cell.turnsLeft),
            get_rgb_from_turns_left(cell.color[2], cell.turnsLeft)
        )
        return color
    
# Gradually approach white (255) as the turnsLeft approaches 0
def get_rgb_from_turns_left(startValue, turnsLeft):
    modifier = (int(config["GAMEPLAY"]["CELL_LIFETIME"]) - turnsLeft) * int(config["GRAPHICS"]["COLOR_STEPS"])
    # Clamp value between 0-255
    return max(0, min(startValue + modifier, 255))

asyncio.run(main())