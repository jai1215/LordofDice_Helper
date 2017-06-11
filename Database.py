import numpy as np
import re
from Dicer import Dicer

class dbMap:
    def __init__(self, size, data):
        self.xSize = size[0]
        self.ySize = size[1]
        self.map_data = np.array(data)
        pass

    def set_boss(self, data):
        self.boss = data

    def set_wall(self, data):
        self.wall = data

    def set_teleports(self, data):
        self.teleports = data

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

    def prev(self, point):
        if point == False:
            return False

        if point[0] != 0:
            dir = self.map_data[point[1], point[0]-1] #left
            if dir == '2':
                return (point[0] - 1, point[1])

        if point[0] < (self.xSize-1):
            dir = self.map_data[point[1], point[0] + 1]  # right
            if dir == '4':
                return (point[0] + 1, point[1])

        if point[1] != 0:
            dir = self.map_data[point[1] - 1, point[0]]  # Up
            if dir == '3':
                return (point[0], point[1] - 1)

        if point[1] < (self.ySize - 1):
            dir = self.map_data[point[1] + 1, point[0]]  # Down
            if dir == '1':
                return (point[0], point[1] + 1)
        return False

    def get_dir(self, point):
        dir = self.map_data[point[1], point[0]]
        return dir

    def teleports_check(self, pos):
        length = int(len(self.teleports)/2)
        for i in range(length):
            m = pos
            t = self.teleports[i*2]
            if self.eq_pos(m, t):
                return self.teleports[i*2+1]
        return False

    def eq_pos(self, a, b):
        return (a[0] == b[0]) & (a[1] == b[1])

    def is_boss(self, pos):
        for boss_pos in self.boss:
            if self.eq_pos(boss_pos, pos):
                return True
        return False

class dbDicer:
    def __init__(self, dicers):
        self.dicers = []
        pass

    def initialize(self):
        for d in self.dicers:
            d.initialize()

    def length(self):
        return len(self.dicers)

    def set_selection(self, sel):
        self.selection = sel
        ret = []
        for i in sel:
            ret.append(self.dicers[i])
        return ret

    def get_type(self, dicer_id):
        sel = self.selection(dicer_id)
        dicer = self.dicers[sel]
        return dicer[1]

    def get_move(self, dicer_id):
        sel = self.selection(dicer_id)
        dicer = self.dicers[sel]
        return dicer[0]

    def get_attack(self, dicer_id):
        sel = self.selection(dicer_id)
        dicer = self.dicers[sel]
        return dicer[2]

    def add_dicer(self, dicer):
        new_dicer = Dicer(dicer)
        self.dicers.append(new_dicer)

    def get_dicers(self):
        ret = []
        for d in self.dicers:
            ret.append(d.get_name())
        return ret

    def get_dicer(self, name):
        for d in self.dicers:
            if d.get_name() == name:
                return d
        print("Cannot find dicer")
        return 0

    def get_dicerID(self, id):
        return self.dicers[id]

    def cal_dicer_move(self, dicer_name, pos, map):
        dicer = self.get_dicer(dicer_name)
        dicer.use()
        return dicer.cal_move(pos, map)

    def cal_dicerID_move(self, id, pos, map):
        dicer = self.get_dicerID(id)
        dicer.use()
        return dicer.cal_move(pos, map)






