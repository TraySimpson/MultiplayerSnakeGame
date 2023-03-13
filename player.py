class Player:
    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color
        self.lastTurnMoved = 0
        self.position = None
        pass

    def move_player(self, position):
        self.position = position

    def has_moved_this_turn(self, turn) -> bool:
        return self.lastTurnMoved >= turn