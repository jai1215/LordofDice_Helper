import numpy as np
from Database import dbMap

class Control:
    def __init__(self):
        self.database = {}

    def set_db(self, database):
        self.database = database
        self.dbmap = dbMap()
        self.dbmap.set_size(self.database['mapSize'])
        self.dbmap.set_map_data(self.database['mapData'])
        self.master_pos = self.database["mapInfo"]["infoStartPoint"][0]


    def get_start(self):
        return self.master_pos

    def next(self):
        self.master_pos = self.dbmap.next(self.master_pos)
        return self.master_pos



