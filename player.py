import uuid
from util import *

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
            get_tuple_from_string(data[1]), 
            int(data[2]),
            data[3])
