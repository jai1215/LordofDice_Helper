from Database import dbMap, dbDicer
import random

class Control:
    def __init__(self):
        self.database = {}
        self.dbmap = 0

    def set_db(self, database):
        self.dbmap = dbMap(database['mapSize'], database['mapData'])
        self.dbmap.set_boss(database["mapInfo"]["infoBoss"])
        self.dbmap.set_wall(database["mapInfo"]["infoWall"])
        self.dbmap.set_teleports(database["mapInfo"]["infoTelPoint"])
        self.dicers = dbDicer(database["dicer"])
        self.master_pos = database["mapInfo"]["infoStartPoint"][0]

    def get_start(self):
        return self.master_pos

    def select_dicers(self):
        #selection = random(set(range(self.dicers.length())), 6)
        #print(selection)
        #return self.dicers.set_selection(selection)
        dicer = {
            "name" : "아리오크",
            "type" : "폭격",
            "attack" : 3280,
            "move" : 4,
        }
        self.dicers.add_dicer(dicer)
        dicer = {
            "name": "로키",
            "type": "마법",
            "attack": 2757,
            "move": 4,
        }
        self.dicers.add_dicer(dicer)
        dicer = {
            "name": "비홀더",
            "type": "휠윈드",
            "attack": 2444,
            "move": 2,
            "charge" : 0.35,
        }
        self.dicers.add_dicer(dicer)
        dicer = {
            "name": "바루나",
            "type": "휠윈드",
            "attack": 2218,
            "move": 5,
            "charge" : 0.35,
        }
        self.dicers.add_dicer(dicer)
        dicer = {
            "name": "그라이프",
            "type": "관통",
            "attack": 2108,
            "move": 3,
            "charge" : 0.35,
        }
        self.dicers.add_dicer(dicer)
        dicer = {
            "name": "에드워드",
            "type": "폭격",
            "attack": 1807,
            "move": 1,
            "charge" : 0.30,
        }
        self.dicers.add_dicer(dicer)
        return self.dicers.get_dicers()

    def dicer_move(self, dicer):
        ret = self.dicers.cal_dicer_move(dicer, self.master_pos, self.dbmap)
        self.master_pos = ret["new_pos"]
        return ret

    def dicer_move_etc(self, move):
        ret = {}
        ret["position"] = self.dicer_move_position(move)
        attack_list = self.get_attack_range(type, self.master_pos)
        ret["attack_list"] = []
        for attack in attack_list:
            if self.is_boss(attack):
                ret["attack_list"].append(attack)
                print("Hit ", attack)
        return ret

    def dicer_move_punch(self, move):
        ret = {}
        ret["attack_list"] = []
        prev_pos = self.master_pos
        for i in range(move):
            new_pos = self.dbmap.next(prev_pos)
            if self.dbmap.is_boss(new_pos):
                ret["position"] = prev_pos
                ret["attack_list"].append(new_pos)
                return ret
            prev_pos = new_pos
        ret["position"] = new_pos
        return ret

    def dicer_move_shoot(self, move):
        ret = {}
        ret["position"] = self.dicer_move_position(move)
        ret["attack_list"] = []
        prev_pos_4 = self.master_pos
        for i in range(4):
            prev_pos_4 = self.dbmap.prev(prev_pos_4)
        prev_pos_5 = self.dbmap.prev(prev_pos_4)

        next_pos_4 = self.master_pos
        for i in range(4):
            next_pos_4 = self.dbmap.next(next_pos_4)
        next_pos_5 = self.dbmap.next(next_pos_4)

        if prev_pos_5:
            ret["attack_list"].append(prev_pos_5)
        elif prev_pos_4:
            ret["attack_list"].append(prev_pos_4)
        elif next_pos_4:
            ret["attack_list"].append(next_pos_4)
        elif next_pos_5:
            ret["attack_list"].append(next_pos_5)
        return ret


