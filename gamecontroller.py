from mapcell import MapCell
import configparser

class GameController:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.mapSize = int(config["GAMEPLAY"]["MAP_SIZE"])
        self.cellLifetime = int(config["GAMEPLAY"]["CELL_LIFETIME"])
        self._turn = 1         #default this to 1 as players will be set to 0
        self._players = []
        self._map = self.reset_map()
        self._game_over = False

    def point_is_movable(self, point, player):
        x = point[0]
        y = point[1]
        return (self.is_players_turn(player) and
                self.point_is_in_bounds(x, y) and 
                self.point_is_beside_player(x, y, player.position) and
                self.point_is_available(x, y))

    def is_players_turn(self, player) -> bool:
        return not player.has_moved_this_turn(self._turn)
    
    def point_is_in_bounds(self, x, y) -> bool:
        return x >= 0 and x < self.mapSize and y >= 0 and y < self.mapSize

    def point_is_beside_player(self, x, y, playerPosition) -> bool:
        return abs(x - playerPosition[0]) < 2 and abs(y - playerPosition[1]) < 2

    def point_is_available(self, x, y) -> bool:
        return self._map[x][y] is None
    
    def spawn_player(self, player):
        point = (0,2)
        self._map[point[0]][point[1]] = MapCell(player, self.cellLifetime)
        self._players.append(player)
        player.move_player(point, False)
        print(f"Player {player.name} joined!")

    def move_player(self, point, player):
        self._map[point[0]][point[1]] = MapCell(player, self.cellLifetime)
        player.move_player(point)
        if (self.check_game_over_for_player(player)):
            self.is_game_over()
        if (self.all_players_have_moved()):
            self.progress_turn()

    def all_players_have_moved(self) -> bool:
        for player in self._players:
            if (not player.has_moved_this_turn(self._turn)):
                return False
        return True

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
        self._turn += 1
        print(f"Turn: {self._turn}")

    def check_game_over_for_player(self, player):
        playerPosition = player.position
        for x in range(-1,2):
            for y in range(-1,2):
                if (self.point_is_movable(self._map, (playerPosition[0] + x, playerPosition[1] + y), playerPosition)):
                    return False
        print(f"Game over for {player.name}!")
        return True
    
    def check_game_over(self):
        if (len(self._players == 2)):
            print(f"Player {self._players[0].name} wins!")
    
    def is_game_over(self):
        return self._game_over