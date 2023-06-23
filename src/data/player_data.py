import os
import json

from src.base.singleton import Singleton


class PlayerData(object, metaclass=Singleton):

    def __init__(self):
        self.player_name = ""
        self.player_data = {}

    def init_player(self, player_name):
        self.player_name = player_name
        self.load_player_data()

    def load_player_data(self):
        dateiname = f"res/data/{self.player_name}.player"
        if os.path.exists(dateiname):
            with open(dateiname, "r") as ifile:
                self.player_data = json.load(ifile)
        else:
            self.player_data["books"] = []
            self.save_player_data()

    def save_player_data(self):
        dateiname = f"res/data/{self.player_name}.player"
        with open(dateiname, "w") as ofile:
            json.dump(self.player_data, ofile)

    def get_books(self):
        return self.player_data["books"]

    def set_book(self, books):
        self.player_data["books"] = books
        self.save_player_data()
