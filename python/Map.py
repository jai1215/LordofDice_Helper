from openpyxl import load_workbook
import Main

wb = load_workbook(filename='test.py')
sheet_ex1 = wb['ex1']

print(sheet_ex1['A2'].value)

class Map:
    def __init__(self):
        self.x_size = 0
        self.y_size = 0
        self.map = []
        self.teleport = dict()

    def draw(self):
        pass

    def load_map(self, filename):
        fin = open(filename)
        line = fin.readline()
        map_info = line.split(' ')
        self.x_size = int(map_info[0])
        self.y_size = int(map_info[1])
        info = int(map_info[2])
        for i in range(info):
            line = fin.readline().split(' ')
            self.teleport[line[0]] = [int(line[1]), int(line[2])]

        for y in range(self.y_size):
            line = fin.readline().rstrip()
            x_line = []
            for x in range(self.x_size):
                if x>=len(line):
                    x_line.append(Tile(' '))
                else:
                    x_line.append(Tile(line[x]))
            self.map.append(x_line)
        fin.close()

    def print_map(self):
        print("Print Map %dx%d" % (self.x_size, self.y_size))
        for y in range(self.y_size):
            for x in range(self.x_size):
                print("%c " % self.map[y][x].type, end='')
            print()

    def find_tel(self, target):
        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.map[y][x] == target:
                    return [x, y]
        print("cannot find target : ", target)
        exit(100)

    def next(self, pos):
        direction = self.get_type(pos)
        if direction == '1':
            return self.a_sum(pos, [1, 0])
        elif direction == '2':
            return self.a_sum(pos, [0, 1])
        elif direction == '3':
            return self.a_sum(pos, [-1, 0])
        elif direction == '4':
            return self.a_sum(pos, [0, -1])
        elif direction == ' ':
            print("Cannot Find path :", direction)
            exit(99)
        self.teleport[direction]
        exit(100)


    def get_type(self, pos):
        return self.map[pos[1]][pos[0]].typedh

    def a_sum(self, a, b):
        return [a[0]+b[0], a[1]+b[1]]

if __name__ == "__main__":

    load_map("map.xlsx")
    pass