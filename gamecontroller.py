from mapcell import MapCell, ObstacleCell
import configparser, random
import os, psutil, ast

class GameController:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.mapSize = int(config["GAMEPLAY"]["MAP_SIZE"])
        self.cellLifetime = int(config["GAMEPLAY"]["CELL_LIFETIME"])
        self._observers = []
        self._turn = 1         #default this to 1 as players will be set to 0
        self._players = []
        self._map = self.reset_map()
        self._obstacles = []
        self.add_obstacles()
        self._game_over = False

    def add_observer(self, observer):
        self._observers.append(observer)

    def get_config(self):
        return {
            "mapSize": self.mapSize,
            "cellLifetime": self.cellLifetime,
            "obstacles": self.get_obstacles()
        }
    
    def load_config_from_data(self, data):
        self.mapSize = int(data["mapSize"])
        self.cellLifetime = int(data["cellLifetime"])
        self._map = self.reset_map()
        self.load_obstacles(data["obstacles"])

    def load_obstacles(self, obstacles):
        self._obstacles = []
        for obstacle in obstacles:
            self._obstacles.append(obstacle)
            self._map[obstacle[0]][obstacle[1]] = ObstacleCell()

    def get_obstacles(self):
        return self._obstacles

    def player_can_move_to(self, point, player):
        return self.is_players_turn(player) and self.point_is_movable(point, player)

    def point_is_movable(self, point, player):
        x = point[0]
        y = point[1]
        return (self.point_is_in_bounds(x, y) and 
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
    
    async def spawn_player(self, player, source=None):
        point = (0,2)
        self._map[point[0]][point[1]] = MapCell(player, self.cellLifetime)
        self._players.append(player)
        player.move_player(point, False)
        state = self.get_state_data("spawn", player)
        await self.notify_observers(state, source)

    async def move_player(self, point, player, source=None):
        player.position = self.get_player_from_list(player.name).position
        self._map[point[0]][point[1]] = MapCell(player, self.cellLifetime)
        player.move_player(point)
        if (self.check_game_over_for_player(player)):
            self.is_game_over()
        if (self.all_players_have_moved()):
            self.progress_turn()
        state = self.get_state_data("move", player, point)
        await self.notify_observers(state, source)

    def get_state_data(self, action, player, point=None):
        data = {
            "action": action,
            "player": player.encode()
        }
        if (point is not None):
            data["point"] = point
        return data

    async def notify_observers(self, state, source):
        for observer in self._observers:
            await observer.update(state, source)

    def get_player_from_list(self, playerName):
        for player in self._players:
            if player.name == playerName:
                return player
        else:
            return None
        
    def all_players_have_moved(self) -> bool:
        for player in self._players:
            if (not player.has_moved_this_turn(self._turn)):
                return False
        return True

    def reset_map(self):
        return [[None for i in range(self.mapSize)] for j in range(self.mapSize)]
    
    def add_obstacles(self):
        for i in range(10):
            x = random.randint(0, self.mapSize-1)
            y = random.randint(0, self.mapSize-1)
            self._obstacles.append((x, y))
            self._map[x][y] = ObstacleCell()
    
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
        process = psutil.Process(os.getpid())
        print(f"Turn: {self._turn} \t{process.memory_info().rss}")

    def check_game_over_for_player(self, player):
        playerPosition = player.position
        for x in range(-1,2):
            for y in range(-1,2):
                if (self.point_is_movable((playerPosition[0] + x, playerPosition[1] + y), player)):
                    return False
        print(f"Game over for {player.name}!")
        return True
    
    def check_game_over(self):
        if (len(self._players == 2)):
            print(f"Player {self._players[0].name} wins!")
    
    def is_game_over(self):
        return self._game_over