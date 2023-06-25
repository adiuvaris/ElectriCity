import os
import json


class GameData(object):

    def __init__(self):
        self.player_name = ""
        self.game_data = {}

    def get_scale(self):
        if "scale" not in self.game_data:
            self.game_data["scale"] = 100
        return self.game_data["scale"]

    def set_scale(self, scale):
        self.game_data["scale"] = scale
        self.save_game_data()

    def scale(self, val):
        return int(val * self.get_scale() / 100.0)

    def init_player(self, player_name):
        self.player_name = player_name
        self.load_game_data()

    def load_game_data(self):
        dateiname = f"res/data/{self.player_name}.player"
        if os.path.exists(dateiname):
            with open(dateiname, "r") as ifile:
                self.game_data = json.load(ifile)
        else:
            self.game_data["books"] = []
            self.save_game_data()

    def save_game_data(self):
        dateiname = f"res/data/{self.player_name}.player"
        with open(dateiname, "w") as ofile:
            json.dump(self.game_data, ofile)

    def get_books(self):
        if "books" not in self.game_data:
            self.game_data["books"] = []
        return self.game_data["books"]

    def set_book(self, books):
        self.game_data["books"] = books
        self.save_game_data()


# Einzige Instanz von GameData
gd = GameData()
