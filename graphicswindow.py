from graphics import *
from graphicscell import GraphicsCell
import configparser
import math

class GraphicsWindow():
    def __init__(self) -> None:
        self._load_config()
        self._win = self.build_window()
        self._backgroundColor = "white"
        self._obstacleColor = "black"
        self._graphicsMap = self._build_graphics_map()

    def _load_config(self, config):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self._mapSize = int(config["GAMEPLAY"]["MAP_SIZE"])
        self._uiBarHeight = float(self._config["GRAPHICS"]["UI_BAR_HEIGHT"])
        self._cellSize = int(self._config["GRAPHICS"]["CELL_GRAPHICS_SIZE"])
        self._cellLifetime = int(config["GAMEPLAY"]["CELL_LIFETIME"])
        self._colorSteps = int(config["GRAPHICS"]["COLOR_STEPS"])

    def get_click_point(self):
        point = self._win.getMouse()
        return (math.floor(point.getX()), math.floor(point.getY()))

    def build_window(self):
        width = self._mapSize
        height = self._mapSize + self._uiBarHeight
        win = GraphWin(width = width * self._cellSize, height = height * self._cellSize)
        win.setCoords(0, 0, width, height)
        return win

    def _build_graphics_map(self):
        return [[GraphicsCell(x, y, self._win, self._backgroundColor) for y in range(self._mapSize)] for x in range(self._mapSize)]

    def _draw_obstacles(self, map):
        for x, row in enumerate(map):
            for y, cell in enumerate(row):
                if (cell is not None and cell.is_permanent()):
                    self._graphicsMap[x][y] = GraphicsCell(x, y, self._win, self._obstacleColor)

    def draw_ui(self, player):
        uiY = self._mapSize + (self._uiBarHeight / 2)
        uiName = Text(Point(1, uiY), player.name)
        uiName.setFill(self.color_rgb(player.color[0], player.color[1], player.color[2]))
        uiName.draw(self._win)

    def draw_graphics(self, map):
        self._draw_obstacles(map)
        self.update_graphics(map)

    def update_graphics(self, map):
        for x, row in enumerate(map):
            for y, cell in enumerate(row):
                self._graphicsMap[x][y].update_color(self._get_cell_color(cell), self._win)

    def _get_cell_color(self, cell):
        if (cell is None):
            return self._backgroundColor
        elif (cell.is_permanent()):
            return self._obstacleColor
        else:
            color = color_rgb(
                self._get_rgb_from_turns_left(cell.color[0], cell.turnsLeft),
                self._get_rgb_from_turns_left(cell.color[1], cell.turnsLeft),
                self._get_rgb_from_turns_left(cell.color[2], cell.turnsLeft)
            )
            return color
        
    # Gradually approach white (255) as the turnsLeft approaches 0
    def _get_rgb_from_turns_left(self, startValue, turnsLeft):
        modifier = (self.cellLifetime - turnsLeft) * self._colorSteps
        # Clamp value between 0-255
        return max(0, min(startValue + modifier, 255))