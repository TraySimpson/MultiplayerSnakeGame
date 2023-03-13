class Player:
    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color
        self.lastTurnMoved = 0
        self.position = None
        pass

    def move_player(self, position, useTurn=True):
        if (useTurn):
            self.lastTurnMoved += 1
        self.position = position

    def has_moved_this_turn(self, turn) -> bool:
        return self.lastTurnMoved >= turn