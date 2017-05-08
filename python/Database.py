import numpy as np
import re
import win32com.client

class dbMap:
    def __init__(self):
        self.xSize = 0
        self.ySize = 0
        pass

    def readExcel_header(self, sheet):
        self.direction = []
        for i in range(4):
            self.direction.append(sheet.Cells(1, i+1).Value)
        self.xSize = int(sheet.Cells(2, 2).Value)
        self.ySize = int(sheet.Cells(2, 4).Value)

    def readExcel_direction(self, sheet):
        self.map_data = np.zeros((self.xSize, self.ySize))
        for y in range(self.ySize):
            for x in range(self.xSize):
                data = sheet.Cells(4+y, 2+x).Value
                for d in range(4):
                    if data == self.direction[d]:
                        self.map_data[y][x] = d+1

    def readExcel_extraInfo(self, sheet):
        self.map_tp = []
        self.boss = []
        self.teleport = {}
        for y in range(self.ySize):
            for x in range(self.xSize):
                data = sheet.Cells(4 + y, 13 + x).Value
                if data == None:
                    continue
                if data == 'S':
                    self.start = [x, y]
                elif data == 'o':
                    self.boss.append([x, y])
                elif data == 'C':
                    self.charge = [x, y]
                elif re.search(r'T.*', data):
                    self.teleport[data] = [x, y]

    def get_direction(self, pos):
        return self.map_data[pos[1], pos[0]]

    def is_boss(self, x, y):
        for data in self.boss:
            if (data[0] == x) & (data[1] == y):
                return True
        return False

    def is_start(self, x, y):
        if (self.start[0] == x) & (self.start[1] == y):
            return True
        return False

    def is_charge(self, x, y):
        if (self.charge[0] == x) & (self.charge[1] == y):
            return True
        return False

    def is_teleport(self, x, y):
        for key in self.teleport.keys():
            if re.match(r'T.i', key):
                v = self.teleport[key]
                if(v[0] == x) & (v[1] == y):
                    return True
        return False


class dbMaster:
    def __init__(self):
        pass

    def set_position(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def get_position(self):
        return [self.pos_x, self.pos_y]


class dbDicer:
    #1: 휠윈드
    #2: 마법
    #3: 저격
    #4: 폭격
    #5: 근접
    #6: 관통
    def __init__(self):
        self.type = 0
        self.move = 0
        self.dice = 0
        self.attack = 0
        self.health = 0
        pass

    def set(self, data):
        self.type = data[0]
        self.move = data[1]
        self.dice = data[2]
        self.attack = data[3]
        self.health = data[4]
        pass

class dbMain:
    def __init__(self):
        self.db_dicers = []
        pass

    def readExcel(self, filename):
        db_map = dbMap()
        db_master = dbMaster()
        excel = win32com.client.Dispatch("Excel.Application")
        wb = excel.Workbooks.Open(filename)
        sheet = wb.Worksheets('lion')
        db_map.readExcel_header(sheet)
        print("Map Size : %dx%d" % (db_map.xSize, db_map.ySize))
        db_map.readExcel_direction(sheet)
        print(db_map.map_data)
        db_map.readExcel_extraInfo(sheet)
        print(db_map.boss)
        print(db_map.charge)
        db_master.set_position(db_map.start)
        print(db_map.teleport)
        self.db_map = db_map
        self.db_master = db_master

    def readDicer(self,filename):
        fin = open(filename)
        data = fin.read().split('\n')
        for line in data:
            line = re.split(r'\s+', line)
            dicer = dbDicer()
            dicer.set(line)
            self.db_dicers.append(dicer)

    def loadDicer(self, index):
        return self.db_dicers[index]

if __name__ == "__main__":
    dbMain = dbMain()
    dbMain.readExcel("C:/Users/choigj/Desktop/util/RoD/map.xlsx")
    dbMain.readDicer("C:/Users/choigj/Desktop/util/RoD/dicer.txt")

