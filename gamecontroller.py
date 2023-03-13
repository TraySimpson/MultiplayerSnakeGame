from mapcell import MapCell
import configparser

class GameController:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.mapSize = int(config["GAMEPLAY"]["MAP_SIZE"])
        self.cellLifetime = int(config["GAMEPLAY"]["CELL_LIFETIME"])
        self._map = self.reset_map()
        self._game_over = False

    def point_is_movable(self, point, playerPosition):
        x = point[0]
        y = point[1]
        return (self.point_is_in_bounds(x, y) and 
                self.point_is_beside_player(x, y, playerPosition) and
                self.point_is_available(x, y))

    def point_is_in_bounds(self, x, y) -> bool:
        return x >= 0 and x < self.mapSize and y >= 0 and y < self.mapSize

    def point_is_beside_player(self, x, y, playerPosition) -> bool:
        return abs(x - playerPosition[0]) < 2 and abs(y - playerPosition[1]) < 2

    def point_is_available(self, x, y) -> bool:
        return self._map[x][y] is None

    def move_player(self, point, player):
        self._map[point[0]][point[1]] = MapCell(player, self.cellLifetime)
        player.move_player(point)
        return point

    def reset_map(self):
        return [[None for i in range(self.mapSize)] for j in range(self.mapSize)]
    
    def get_map(self):
        return self._map

    def progress_turn(self):
        for x, row in enumerate(self._map):
            for y, cell in enumerate(row):
                if(cell is not None):
                    cell.progress_turn()
                    if (cell.is_cell_finished()):
                        self._map[x][y] = None

    def check_game_over_for_player(self, playerPosition):
        for x in range(-1,2):
            for y in range(-1,2):
                if (self.point_is_movable(self._map, (playerPosition[0] + x, playerPosition[1] + y), playerPosition)):
                    return False
        return True
    
    def is_game_over(self):
        return self._game_over