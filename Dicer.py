attack_range = {
    "폭격" : [
        [0, 1],
        [0, 2],
        [1, 2],
        [-1, 2],
        [0, 3],
        [1, 3],
        [-1, 3]
    ],
    "관통": [
        [0, -1],
        [0, -2],
        [0, -3],
        [0, -4],
    ],
    "마법": [
        [-1, -1],
        [0, -1],
        [1, -1],
        [-1, -2],
        [0, -2],
        [1, -2],
    ],
    "휠윈드": [
        [0, -1],
        [1, -1],
        [1, 0],
        [1, 1],
        [0, 1],
        [-1, 1],
        [-1, 0],
        [-1, -1],
    ],
    "근접": [],
    "저격": []
}

class Dicer:
    def __init__(self, data):
        self.data = data
        self.use_point = 0
        pass

    def initialize(self):
        self.use_point = self.data["use_point"]

    def get_name(self):
        return self.data["name"]

    def cal_move(self, pos, map):
        ret = {}
        ret["new_pos"] = self.dicer_move_new_pos(pos, map)
        ret["attack_pos"] = self.dicer_attack_pos(pos, map)
        ret["attack"] = self.data["attack"]
        return ret

    def dicer_move_new_pos(self, pos, map):
        new_pos = pos
        for i in range(self.data["move"]):
            new_pos = map.next(new_pos)
            if map.teleports_check(new_pos):
                new_pos = map.teleports_check(new_pos)
        return new_pos

    def dicer_attack_pos(self, pos, map):
        dir = map.get_dir(pos)
        at_range = attack_range[self.data["type"]]
        ret = []
        def sum(a, b):
            return [a[0]+b[0], a[1]+b[1]]
        for i in range(len(at_range)):
            at = at_range[i]
            if dir == '1':
                pass
            elif dir == '2':
                at = [-at[1], at[0]]
            elif dir == '3':
                at = [-at[0], -at[1]]
            elif dir == '4':
                at = [at[1], -at[0]]
            ret.append(sum(pos, at))
        return ret

    def use(self):
        self.use_point -= 1

    def available(self):
        if self.use_point > 0:
            return True
        return False