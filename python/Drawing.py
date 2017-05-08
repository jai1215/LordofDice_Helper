from Database import dbMap
import turtle

class drawingMap:
    def __init__(self):
        self.mTurtle = turtle.Turtle()
        self.mTurtle.penup()
        self.mTurtle.hideturtle()
        turtle.tracer(0, 0)
        pass

    def px(self, x):
        return x*30-200

    def py(self, y):
        return -y*30+200

    def draw_arrow(self, pos_x, pos_y, direction):
        aTurtle = turtle.Turtle()
        aTurtle.shapesize(0.8, 0.8)
        aTurtle.up()
        aTurtle.goto(self.px(pos_x) + 12.5, self.py(pos_y) + 12.5)
        if direction == 4:
            aTurtle.right(90)
        elif direction == 3:
            aTurtle.right(270)
        elif direction == 2:
            aTurtle.right(180)
        aTurtle.forward(14)

    def draw_squre(self, pos_x, pos_y):
        self.mTurtle.goto(self.px(pos_x), self.py(pos_y))
        self.mTurtle.pendown()
        self.mTurtle.fillcolor("#ffffff")
        if self.dbmap.is_boss(pos_x, pos_y):
            self.mTurtle.fillcolor("#00ff00")
        elif self.dbmap.is_start(pos_x, pos_y):
            self.mTurtle.fillcolor("#ff0000")
        elif self.dbmap.is_charge(pos_x, pos_y):
            self.mTurtle.fillcolor("#0000ff")
        elif self.dbmap.is_teleport(pos_x, pos_y):
            self.mTurtle.fillcolor("#00ffff")
        self.mTurtle.begin_fill()
        for i in range(4):
            self.mTurtle.forward(25)
            self.mTurtle.left(90)
        pass
        self.mTurtle.end_fill()
        self.mTurtle.penup()

    def drawMap(self, dbmap):
        self.dbmap = dbmap
        xSize = dbmap.xSize
        ySize = dbmap.ySize

        for y in range(ySize):
            for x in range(xSize):
                direction = dbmap.map_data[y, x]
                if direction != 0:
                    self.draw_squre(x, y)
                    self.draw_arrow(x, y, direction)
                elif dbmap.is_boss(x, y):
                    self.draw_squre(x, y)
                elif dbmap.is_teleport(x, y):
                    self.draw_squre(x, y)
        turtle.update()
        turtle.exitonclick()

if __name__ == "__main__":
    dbmap = dbMap()
    dbmap.readExcel("C:/Users/choigj/Desktop/util/RoD/map.xlsx")
    drawing = drawingMap()
    drawing.drawMap(dbmap)
    turtle.exitonclick()