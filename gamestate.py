class Cell:
    player = ""
    turnsLeft = 0
    isPermanent = False

    def __init__(self, name, startTurns, permanent=False) -> None:
        self.player = name
        self.turnsLeft = startTurns
        self.isPermanent = permanent

    def __repr__(self):
        return f"Cell of {self.player} with {self.turnsLeft} turns left"

    # def __str__(self):
    #     return f"Cell of {self.player} with {self.turnsLeft} turns left"

    def progress_turn(self):
        if (self.isPermanent):
            return
        self.turnsLeft -= 1

    def is_cell_finished(self):
        return self.turnsLeft <= 0
