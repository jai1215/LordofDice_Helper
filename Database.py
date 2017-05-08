import numpy as np
import re

attack_range = {
    "폭격" : [
        [0, -1],
        [0, -2],
        [1, -2],
        [-1, -2],
        [0, -3],
        [1, -3],
        [-1, -3]
    ],
    "관통": [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
    ],
    "마법": [
        [-1, 1],
        [0, 1],
        [1, 1],
        [-1, 2],
        [0, 2],
        [1, 2],
    ],
    "휠윈드": [
        [0, 1],
        [1, 1],
        [1, 0],
        [1, -1],
        [0, -1],
        [-1, -1],
        [-1, 0],
        [0, 0]
    ],
    "근접": [],
    "저격": []
}

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

    def get_dir(self, point):
        dir = self.map_data[point[1], point[0]]
        return dir


