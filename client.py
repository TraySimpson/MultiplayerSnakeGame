from graphics import *
from array import *
from gamecontroller import GameController
from clientconn import ClientConn
from player import Player
import math
import configparser

def main():
    global config 
    config = configparser.ConfigParser()
    config.read('config.ini')

    player = Player("player1", (255, 0, 0))

    gameController = GameController()
    if (bool(config["GAMEPLAY"]["ALLOW_MULTIPLAYER"])):
        sender = ClientConn()
        gameController.set_sender(sender)

    gameController.spawn_player(player)
    win = build_window()
    draw_graphics(win, gameController.get_map())
    draw_ui(win, player)
    while(not gameController.is_game_over()):
        clickPoint = get_click_point(win)
        if (gameController.player_can_move_to(clickPoint, player)):
            gameController.move_player(clickPoint, player)
            draw_graphics(win, gameController.get_map())
    print("Game over!")
    win.getMouse()

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

def draw_ui(win, player):
    uiY = int(config["GAMEPLAY"]["MAP_SIZE"]) + (float(config["GRAPHICS"]["UI_BAR_HEIGHT_SCALE"]) / 2)
    uiName = Text(Point(1, uiY), player.name)
    uiName.setFill(color_rgb(player.color[0], player.color[1], player.color[2]))
    uiName.draw(win)

def draw_graphics(win, map):
    for x, row in enumerate(map):
        for y, cell in enumerate(row):
            cellGfx = Rectangle(Point(x, y), Point(x+1, y+1))
            color = get_cell_color(cell)
            cellGfx.setFill(color)
            cellGfx.draw(win)

def get_cell_color(cell):
    if (cell is None):
        return "white"
    else:
        color = color_rgb(
            get_rgb_from_turns_left(cell.color[0], cell.turnsLeft),
            get_rgb_from_turns_left(cell.color[1], cell.turnsLeft),
            get_rgb_from_turns_left(cell.color[2], cell.turnsLeft)
        )
        return color
    
def get_rgb_from_turns_left(startValue, turnsLeft):
    modifier = (int(config["GAMEPLAY"]["CELL_LIFETIME"]) - turnsLeft) * int(config["GRAPHICS"]["COLOR_STEPS"])
    # Clamp value between 0-255
    return max(0, min(startValue + modifier, 255))

main()