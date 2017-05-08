import numpy as np
import re

class dbMap:
    def __init__(self):
        self.xSize = 0
        self.ySize = 0
        pass

    def set_size(self, point):
        self.xSize = point[0]
        self.ySize = point[1]

    def set_map_data(self, data):
        self.map_data = np.array(data)

    def next(self, point):
        dir = self.map_data[point[1], point[0]]
        if dir == '1':
            return (point[0], point[1] - 1)
        elif dir == '2':
            return (point[0] + 1, point[1])
        elif dir == '3':
            return (point[0], point[1] + 1)
        elif dir == '4':
            return (point[0] - 1, point[1])
        else:
            print("direction find error "+dir)


