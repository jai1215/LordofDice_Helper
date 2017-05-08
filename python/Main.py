from Database import dbMain
from Drawing import drawingMap

class Main(drawingMap):
    def __init__(self):
        super().__init__()
        self.db = dbMain()
        self.db.readExcel("C:/Users/choigj/Desktop/util/RoD/map.xlsx")
        self.db.readDicer("C:/Users/choigj/Desktop/util/RoD/dicer.txt")
        self.dicers = []

    def run(self):
        self.dicers.append(self.db.loadDicer(0))
        self.dicers.append(self.db.loadDicer(1))
        self.dicers.append(self.db.loadDicer(2))
        self.dicers.append(self.db.loadDicer(3))
        self.dicers.append(self.db.loadDicer(4))
        self.dicers.append(self.db.loadDicer(5))
        self.moveDicer(0)
        self.moveDicer(0)
        self.moveDicer(1)
        self.drawMap(self.db.db_map)

    def moveDicer(self, index):
        dicer = self.dicers[index]
        move = dicer.move
        self.moveMaster(move)

    def add(self, a, b):
        return [a[0]+b[0], a[1]+b[1]]

    def moveMaster(self, move):
        for i in range(int(move)):
            cur_pos = self.db.db_master.get_position()
            direction = self.db.db_map.get_direction(cur_pos)
            if(direction == 1):
                cur_pos = self.add(cur_pos, [1, 0])
            elif(direction == 2):
                cur_pos = self.add(cur_pos, [-1, 0])
            elif(direction == 3):
                cur_pos = self.add(cur_pos, [0, -1])
            elif(direction == 4):
                cur_pos = self.add(cur_pos, [0, 1])
            else:
                print("Error while reading direction")
                exit(1)
            print(cur_pos)
            self.db.db_master.set_position(cur_pos)


main = Main()
main.run()