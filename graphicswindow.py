from graphics import *
from graphicscell import GraphicsCell
from graphicsplayer import GraphicsPlayer
import configparser
import math

class GraphicsWindow():
    def __init__(self) -> None:
        self._load_config()
        self._win = self.build_window()
        self._backgroundColor = "#DEE3E8"
        self._obstacleColor = "#2A2B2D"
        self._borderColor = "#494B4D"
        self._graphicsMap = self._build_graphics_map()
        self._playerColors = {}
        self._playerTexts = []
        self._nextColorIndex = 0

    def _load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self._mapSize = int(config["GAMEPLAY"]["MAP_SIZE"])
        self._uiBarHeight = float(config["GRAPHICS"]["UI_BAR_HEIGHT"])
        self._cellSize = int(config["GRAPHICS"]["CELL_GRAPHICS_SIZE"])
        self._cellLifetime = int(config["GAMEPLAY"]["CELL_LIFETIME"])
        self._colorSteps = int(config["GRAPHICS"]["COLOR_STEPS"])
        self._uiNameSpacing = float(config["GRAPHICS"]["UI_NAME_SPACING"])

    def _get_color_options(self):
        return [
            "#0AC5EB",      # Deep Sky Blue
            "#1FD163",      # Malachite (Green)
            "#F2C618",      # Moon Yellow
            "#FA2929"       # Fancy Red (Idk you try naming colors)
        ]
    
    def _get_next_color(self):
        colors = self._get_color_options()
        color = colors[self._nextColorIndex]
        self._nextColorIndex = (self._nextColorIndex + 1) % len(colors)
        return color

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
        return [[GraphicsCell(x, y, self._win, self._backgroundColor, self._borderColor) for y in range(self._mapSize)] for x in range(self._mapSize)]

    def _draw_obstacles(self, map):
        for x, row in enumerate(map):
            for y, cell in enumerate(row):
                if (cell is not None and cell.is_permanent()):
                    self._graphicsMap[x][y] = GraphicsCell(x, y, self._win, self._obstacleColor)

    def add_player(self, player):
        y = self._mapSize + (self._uiBarHeight / 2)
        playerColor = self._get_next_color()
        self._playerColors[player.id] = playerColor
        playerText = GraphicsPlayer(player, playerColor, self._win, y)
        self._playerTexts.append(playerText)
        playerText.move(self._uiNameSpacing * (len(self._playerTexts) - 1))

    def remove_player(self, player):
        index = None
        for i, playerText in enumerate(self._playerTexts):
            if (player.id == playerText.playerId):
                index = i
                break
        playerText = self._playerTexts.pop(index)
        playerText.undraw()
        while index < (len(self._playerTexts) - 1):
            self._playerTexts[index].move(-self._uiNameSpacing)

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
            baseColor = self._get_player_color(cell.playerId)
            return self._get_color_from_turns_left(baseColor, cell.turnsLeft)
        
    def _get_player_color(self, playerId):
        return self._playerColors[playerId]
    
    def _get_color_from_turns_left(self, baseColor, turnsLeft):
        r = baseColor[1:3]
        g = baseColor[3:5]
        b = baseColor[5:7]
        backgroundR = self._backgroundColor[1:3]
        backgroundG = self._backgroundColor[3:5]
        backgroundB = self._backgroundColor[5:7]
        return f"#{self._hex(r, turnsLeft, backgroundR)}{self._hex(g, turnsLeft, backgroundG)}{self._hex(b, turnsLeft, backgroundB)}"
        
    # Gradually approach white (255) as the turnsLeft approaches 0
    def _hex(self, startValue, turnsLeft, targetColor):
        diff = int(startValue, 16) - int(targetColor, 16)
        # ex 16
        progression = float((self._cellLifetime - turnsLeft) / self._cellLifetime)
        value = int(startValue, 16)
        value -= int(progression * diff)
        hx = hex(value)
        if (len(hx) == 3):
            return f"0{hx[2:3]}"
        else:
            return hx[2:4]
