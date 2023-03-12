from graphics import *
from array import *
import math

MAP_SIZE = 5
CELL_GRAPHICS_SIZE = 50

gameOver = False

def main():
    map = reset_map()
    win = build_window()
    update_graphics(win, map)
    while(not gameOver):
        clickPoint = get_click_point(win)
        if (click_is_possible(clickPoint)):
            move_player(map, clickPoint)
            update_graphics(win, map)

def get_click_point(win):
    point = win.getMouse()
    return (math.floor(point.getX()), math.floor(point.getY()))

def click_is_possible(point):
    return True

def move_player(map, point):
    map[point[0]][point[1]] = 1

def reset_map():
    rows, cols = (MAP_SIZE, MAP_SIZE)
    return [[0 for i in range(cols)] for j in range(rows)]

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
    match cell:
        case 0:
            return "white"
        case 1:
            return color_rgb(255, 0, 0)

main()