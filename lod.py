
from Database import dbMap
from Database import attack_range

class Control:
    def __init__(self):
        self.database = {}

    def set_db(self, database):
        self.database = database
        self.dbmap = dbMap()
        self.dbmap.set_size(self.database['mapSize'])
        self.dbmap.set_map_data(self.database['mapData'])
        self.master_pos = self.database["mapInfo"]["infoStartPoint"][0]
        self.teleports = self.database["mapInfo"]["infoTelPoint"]
        self.dicers = self.database["dicer"]

    def get_start(self):
        return self.master_pos

    def teleports_check(self):
        length = int(len(self.teleports)/2)
        for i in range(length):
            m = self.master_pos
            t = self.teleports[i*2]
            if (m[0] == t[0])&(m[1] == t[1]):
                return self.teleports[i*2+1]
        return 0

    def select_dicers(self, ret):
        for i in range(6):
            ret.append(self.dicers[i])
        self.current_dicer = ret

    def dicer_move(self, id):
        id = int(id)
        print(self.current_dicer[id][0])
        self.check_attack_range(self.current_dicer[id][1])
        return int(self.current_dicer[int(id)][0])

    def check_attack_range(self, type):
        dir = self.dbmap.get_dir(self.master_pos)
        at_range = attack_range[type]
        def sum(a, b):
            return [a[0]+b[0], a[1]+b[1]]
        for i in range(len(at_range)):
            print(dir, ":", at_range[i])
            if dir == '1':
                at = at_range[i]
            elif dir == '2':
                at = at_range[i]
                at = [at[1], at[0]]
                print("trans", at)
            elif dir == '3':
                at = at_range[i]
                at = [-at[0], -at[1]]
            elif dir == '4':
                at = at_range[i]
                at = [-at[1], -at[0]]
            print(sum(self.master_pos, at))

    def next(self):
        self.master_pos = self.dbmap.next(self.master_pos)
        tel = self.teleports_check()
        if tel :
            self.master_pos = tel

        return self.master_pos



