class MapCell:
    def __init__(self, player, startTurns, permanent=False) -> None:
        self.player = player.name
        self.color = player.color
        self.turnsLeft = startTurns
        self.isPermanent = permanent

    def __repr__(self):
        return f"Cell of {self.player} with {self.turnsLeft} turns left"

    def progress_turn(self):
        if (self.isPermanent):
            return
        self.turnsLeft -= 1

    def is_cell_finished(self):
        return self.turnsLeft <= 0
