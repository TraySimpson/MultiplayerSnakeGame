class Player:
    def __init__(self, name, color, position=None, lastTurnMoved=0) -> None:
        self.name = name
        self.color = color
        self.lastTurnMoved = lastTurnMoved
        self.position = position
        pass

    def __repr__(self):
        return f"Player:{self.name} with color {self.color}. Moved on turn {self.lastTurnMoved} at {self.position}"

    def move_player(self, position, useTurn=True):
        if (useTurn):
            self.lastTurnMoved += 1
        self.position = position

    def has_moved_this_turn(self, turn) -> bool:
        return self.lastTurnMoved >= turn
    
    def encode(self):
        return f"{self.name}:{self.color}:{self.position}:{self.lastTurnMoved}"
    
    def decode(data):
        data = data.split(":")
        return Player(data[0], data[1], data[2], data[3])


test = Player("jeff",(12,23,34))
test.move_player((2,3))
print(test)
data = test.encode()
print(data)
test2 = Player.decode(data)
print(test2)
