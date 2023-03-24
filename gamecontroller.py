import configparser, random, os, psutil, uuid, util

class GameController:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.mapSize = int(config["GAMEPLAY"]["MAP_SIZE"])
        self.cellLifetime = int(config["GAMEPLAY"]["CELL_LIFETIME"])
        self._turn = 1         #default this to 1 as players will be set to 0
        self._players = []
        self._map = self.reset_map()
        self._obstacles = []
        self.add_obstacles()
        self._game_over = False

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
    
    def get_random_move(self, player):
        moves = self.get_possible_moves(player)
        index = random.randint(0, len(moves)-1)
        return moves[index]
    
    async def spawn_player(self, player, source=None, point=None):
        if (point is None):
            point = self.get_open_spawn_point()
        self._map[point[0]][point[1]] = MapCell(player, self.cellLifetime)
        self._players.append(player)
        player.move_player(point, False)
        return point

    def get_open_spawn_point(self):
        while True:
            (x, y) = self.get_random_point()
            if self.point_is_available(x, y):
                return (x, y)

    async def move_player(self, point, player, source=None):
        if (self._game_over):
            return
        player.position = self.get_player_from_list(player.name).position
        self._map[point[0]][point[1]] = MapCell(player, self.cellLifetime)
        player.move_player(point)
        if (self.check_game_over_for_players()):
            self.is_game_over()
        if (self.all_players_have_moved()):
            self.progress_turn()

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
            (x, y) = self.get_random_point()
            self._obstacles.append((x, y))
            self._map[x][y] = ObstacleCell()

    def get_random_point(self):
        x = random.randint(0, self.mapSize-1)
        y = random.randint(0, self.mapSize-1)
        return (x, y)
    
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

    def get_possible_moves(self, player):
        playerPosition = player.position
        moves = []
        for x in range(-1,2):
            for y in range(-1,2):
                point = (playerPosition[0] + x, playerPosition[1] + y)
                if (self.point_is_movable(point, player)):
                    moves.append(point)
        return moves
    
    def has_player_lost(self, player):
        return player not in self._players
    
    def check_game_over_for_players(self):
        playerLost = False
        for player in self._players:
            if(self.check_game_over_for_player(player)):
                playerLost = True
        return playerLost

    def check_game_over_for_player(self, player):
        if (len(self.get_possible_moves(player)) > 0):
            return False
        print(f"Game over for {player.name}!")
        self._players.remove(player)
        return True
    
    def check_game_over(self):
        if (len(self._players) == 1):
            print(f"Player {self._players[0].name} wins!")
            self._game_over = True
    
    def is_game_over(self):
        return self._game_over
    

class ObserverGameController(GameController):
    def __init__(self) -> None:
        super().__init__()
        self._observers = []

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

    async def spawn_player(self, player, source=None, point=None):
        point = super().spawn_player(player, source, point)
        state = self.get_state_data("spawn", player)
        await self.notify_observers(state, source)
        return point
    
    async def move_player(self, point, player, source=None):
        super().move_player(point, player, source)
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


class MapCell:
    def __init__(self, player, startTurns, permanent=False) -> None:
        self.playerId = player.id
        self.turnsLeft = startTurns

    def __repr__(self):
        return f"Cell of {self.player} with {self.turnsLeft} turns left"

    def progress_turn(self):
        self.turnsLeft -= 1

    def is_cell_finished(self):
        return self.turnsLeft <= 0
    
    def is_permanent(self):
        return False
    

class ObstacleCell:
    def __init__(self) -> None:
        pass

    def __repr__(self):
        return f"Obstacle"

    def progress_turn(self):
        pass

    def is_cell_finished(self):
        return False
    
    def is_permanent(self):
        return True


class Player:
    def __init__(self, name, position=None, lastTurnMoved=0, id=None) -> None:
        if (id == None):
            id = str(uuid.uuid1())
        self.id = id
        self.name = name
        self.lastTurnMoved = lastTurnMoved
        self.position = position
        pass

    def __repr__(self):
        return f"Player:{self.name}. Moved on turn {self.lastTurnMoved} at {self.position}"

    def move_player(self, position, useTurn=True):
        if (useTurn):
            self.lastTurnMoved += 1
        self.position = position

    def has_moved_this_turn(self, turn) -> bool:
        return self.lastTurnMoved >= turn
    
    def encode(self):
        return f"{self.name}:{self.position}:{self.lastTurnMoved}:{self.id}"
    
    def decode(data):
        data = data.split(":")
        return Player(
            data[0], 
            util.get_tuple_from_string(data[1]), 
            int(data[2]),
            data[3])