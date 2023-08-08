import os
from os import path
import json
from platformdirs import *
import src.const as const


class GameData(object):
    """
    Klasse für die Speicherung der Spieler-Daten
    """

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

    def get_volume(self):
        if "volume" not in self.game_data:
            self.game_data["volume"] = 10
        return self.game_data["volume"]

    def set_volume(self, volume):
        self.game_data["volume"] = volume
        self.save_game_data()

    def init_player(self, player_name):
        self.player_name = player_name
        self.load_game_data()

    def load_game_data(self):
        mypath = user_data_dir(const.APP_NAME, False, ensure_exists=True)
        dateiname = f"{mypath}/{self.player_name}.player"
        if os.path.exists(dateiname):
            with open(dateiname, "r") as ifile:
                self.game_data = json.load(ifile)
        else:
            self.game_data["books"] = {}
            self.game_data["room_keys"] = {}
            self.save_game_data()

    def save_game_data(self):
        mypath = user_data_dir(const.APP_NAME, False, ensure_exists=True)
        dateiname = f"{mypath}/{self.player_name}.player"
        with open(dateiname, "w") as ofile:
            json.dump(self.game_data, ofile, indent=2)

    @staticmethod
    def delete_game_data(player_name):
        mypath = user_data_dir(const.APP_NAME, False, ensure_exists=True)
        dateiname = f"{mypath}/{player_name}.player"
        if os.path.exists(dateiname):
            os.remove(dateiname)

    def get_books(self):
        if "books" not in self.game_data:
            self.game_data["books"] = {}
        return self.game_data["books"]

    def init_book(self, room_nr, book_nr, anz_tasks: int = 0):
        books = self.get_books()
        if room_nr not in books:
            books[room_nr] = {}
        if book_nr not in books[room_nr]:
            books[room_nr][book_nr] = []
        while len(books[room_nr][book_nr]) < anz_tasks:
            books[room_nr][book_nr].append(False)
        self.save_game_data()

    def set_task(self, room_nr: str, book_nr: str, task_nr: int):
        self.init_book(room_nr, book_nr, task_nr)
        books = self.get_books()
        books[room_nr][book_nr][task_nr] = True
        self.save_game_data()

    def get_task(self, room_nr: str, book_nr: str, task_nr: int):
        self.init_book(room_nr, book_nr, task_nr)
        books = self.get_books()
        return books[room_nr][book_nr][task_nr]

    def has_all_tasks(self, room_nr: str):
        rooms = self.get_books()
        if room_nr in rooms:
            books = rooms[room_nr]
            for book_nr in books:
                anz_tasks = gd.get_anz_tasks(room_nr, book_nr)
                self.init_book(room_nr, book_nr, anz_tasks)
                for task_nr in range(anz_tasks):
                    if not self.get_task(room_nr, book_nr, task_nr):
                        return False
        else:
            return False

        return True

    def get_avatar(self):
        if "avatar" not in self.game_data:
            self.game_data["avatar"] = "dog.png"
        avatar = self.game_data["avatar"]
        if avatar.find("res/avatars/") != -1:
            avatar = avatar.replace("res/avatars/", "")
        return avatar

    def set_avatar(self, avatar):
        self.game_data["avatar"] = avatar
        self.save_game_data()

    def get_room_keys(self):
        if "room_keys" not in self.game_data:
            self.game_data["room_keys"] = {}
        return self.game_data["room_keys"]

    def has_room_key(self, room_key):
        keys = self.get_room_keys()
        if room_key not in keys:
            return False
        return True

    def set_room_key(self, room_nr):
        keys = self.get_room_keys()
        keys[room_nr] = True
        self.save_game_data()

    @staticmethod
    def get_anz_tasks(room_nr: str, book_nr: str):
        mypath = gd.get_abs_path("res/data")
        dateiname = f"{mypath}/book_{room_nr}_{book_nr}.json"
        if os.path.exists(dateiname):
            with open(dateiname, "r", encoding="'utf-8") as ifile:
                data = json.load(ifile)
                if "Aufgaben" in data:
                    aufgaben = data["Aufgaben"]
                    return len(aufgaben)
        return 0

    @staticmethod
    def get_abs_path(rel_path):
        abs_path = path.abspath(path.join(path.dirname(__file__), "../.."))
        abs_path = path.abspath(path.join(abs_path, rel_path))
        return abs_path


# Einzige Instanz von GameData
gd = GameData()
