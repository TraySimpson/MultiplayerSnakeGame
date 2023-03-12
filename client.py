from graphics import *
from gamestate import Cell
from array import *
import math

MAP_SIZE = 5
CELL_GRAPHICS_SIZE = 50
CELL_LIFETIME = 10
COLOR_STEPS = 20

playerName = "player1"
playerColor = (255, 0, 0)

def main():
    map = reset_map()
    playerPosition = (0,2)
    gameOver = False
    win = build_window()
    update_graphics(win, map)
    while(not gameOver):
        clickPoint = get_click_point(win)
        if (point_is_movable(map, clickPoint, playerPosition)):
            playerPosition = move_player(map, clickPoint)
            progress_turn(map)
            update_graphics(win, map)
            gameOver = is_game_over(map, playerPosition)
    print("Game over!")
    win.getMouse()

def get_click_point(win):
    point = win.getMouse()
    return (math.floor(point.getX()), math.floor(point.getY()))

def point_is_movable(map, point, playerPosition):
    x = point[0]
    y = point[1]
    return (point_is_in_bounds(x, y) and 
            point_is_beside_player(x, y, playerPosition) and
            point_is_available(map, x, y))

def point_is_in_bounds(x, y) -> bool:
    return x >= 0 and x < MAP_SIZE and y >= 0 and y < MAP_SIZE

def point_is_beside_player(x, y, playerPosition) -> bool:
    return abs(x - playerPosition[0]) < 2 and abs(y - playerPosition[1]) < 2

def point_is_available(map, x, y) -> bool:
    return map[x][y] is None

def move_player(map, point):
    map[point[0]][point[1]] = Cell(playerName, CELL_LIFETIME)
    return point

def reset_map():
    rows, cols = (MAP_SIZE, MAP_SIZE)
    return [[None for i in range(cols)] for j in range(rows)]

def progress_turn(map):
    for x, row in enumerate(map):
        for y, cell in enumerate(row):
            if(cell is not None):
                cell.progress_turn()
                if (cell.is_cell_finished()):
                    map[x][y] = None

def is_game_over(map, playerPosition):
    for x in range(-1,2):
        for y in range(-1,2):
            if (point_is_movable(map, (playerPosition[0] + x, playerPosition[1] + y), playerPosition)):
                return False
    return True

def build_window():
    size = CELL_GRAPHICS_SIZE * MAP_SIZE
    win = GraphWin(width = size, height = size)
    win.setCoords(0, 0, MAP_SIZE, MAP_SIZE)
    return win

def update_graphics(win, map):
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
            get_rgb_from_turns_left(playerColor[0], cell.turnsLeft),
            get_rgb_from_turns_left(playerColor[1], cell.turnsLeft),
            get_rgb_from_turns_left(playerColor[2], cell.turnsLeft)
        )
        return color
    
def get_rgb_from_turns_left(startValue, turnsLeft):
    modifier = (CELL_LIFETIME - turnsLeft) * COLOR_STEPS
    # Clamp value between 0-255
    return max(0, min(startValue + modifier, 255))

main()