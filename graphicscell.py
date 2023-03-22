from graphicswindow import Rectangle, Point

class GraphicsCell:
    def __init__(self, x, y, win, color="white", borderColor = "black") -> None:
        self.rectangle = Rectangle(Point(x, y), Point(x+1, y+1))
        self.rectangle.setFill(color)
        self.rectangle.setOutline(borderColor)
        self.draw_cell(win)

    def update_color(self, color, win):
        self.rectangle.setFill(color)
        win.update()

    def draw_cell(self, win):
        self.rectangle.draw(win)