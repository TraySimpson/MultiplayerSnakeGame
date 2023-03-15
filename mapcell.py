class MapCell:
    def __init__(self, player, startTurns, permanent=False) -> None:
        self.player = player.name
        self.color = player.color
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