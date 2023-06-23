import os
import json

from src.base.singleton import Singleton


class GameData(object, metaclass=Singleton):

    def __init__(self):
        self.settings = {}
        self.load_setting()

    def load_setting(self):
        dateiname = f"res/data/game.data"
        if os.path.exists(dateiname):
            with open(dateiname, "r") as ifile:
                self.settings = json.load(ifile)
        else:
            # Default-Werte eintragen
            self.settings["scale"] = 100.0
            self.save_settings()

    def save_settings(self):
        dateiname = f"res/data/game.data"
        with open(dateiname, "w") as ofile:
            json.dump(self.settings, ofile)

    def get_scale(self):
        return self.settings["scale"]

    def set_scale(self, scale):
        self.settings["scale"] = scale
        self.save_settings()

    def do_scale(self, val):
        return int(val * self.get_scale() / 100.0)

