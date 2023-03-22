from graphicswindow import Text, Point

class GraphicsPlayer:
    def __init__(self, player, color, win, y) -> None:
        self.playerId = player.id
        self.text = Text(Point(1,y), player.name)
        self.text.setFill(color)
        self.text.draw(win)

    def move(self, x):
        self.text.move(x, 0)

    def undraw(self):
        self.text.undraw()