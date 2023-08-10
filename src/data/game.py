import os
from os import path
import json
from platformdirs import *
import src.const as const


class GameData(object):
    """
    Klasse für die Speicherung der Spieler- und Einstellungsdaten
    Es darf nur eine Instanz geben und die wird in diesem Modul erstellt.
    Der Zugriff auf die Funktionen muss immer über die Instanz "gd" passieren
    Z.B.

        from src.data.game import gd
        gd.scale(200)

    """

    def __init__(self):
        """
        Konstruktor
        """

        # Member definieren
        self.player_name = ""
        self.game_data = {}

    def get_scale(self):
        """
        Liefert die eingestellte Skalierung - Default 100 %.
        :return Skalierung
        """

        if "scale" not in self.game_data:
            self.game_data["scale"] = 100
        return self.game_data["scale"]

    def set_scale(self, scale):
        """
        Speichert die Skalierung.
        :param scale: Skalierung in %
        """

        self.game_data["scale"] = scale
        self.save_game_data()

    def scale(self, val):
        """
        Skalierung auf einen Wert anwenden
        :param val: Wert der umgerechnet werden soll
        :return umgerechneter Wert
        """
        return int(val * self.get_scale() / 100.0)

    def get_volume(self):
        """
        Liefert die eingestellte Lautstärke - Default 10 %.
        :return Lautstärke
        """

        if "volume" not in self.game_data:
            self.game_data["volume"] = 10
        return self.game_data["volume"]

    def set_volume(self, volume):
        """
        Speichert die Lautstärke.
        :param volume: Lautstärke in %
        """

        self.game_data["volume"] = volume
        self.save_game_data()

    def get_avatar(self):
        """
        Liefert den definierten Avatar - Default ist der Hund
        :return Dateiname des avatars
        """

        if "avatar" not in self.game_data:
            self.game_data["avatar"] = "dog.png"
        avatar = self.game_data["avatar"]

        # Pfad vom Dateinamen entfernen
        if avatar.find("res/avatars/") != -1:
            avatar = avatar.replace("res/avatars/", "")
        return avatar

    def set_avatar(self, avatar):
        """
        Avatar für aktuellen Spieler festlegen
        :avatar Dateiname des avatars
        """

        self.game_data["avatar"] = avatar

        # Aktuelle Struktur speichern
        self.save_game_data()

    def init_player(self, player_name):
        """
        Initialisiert die Spiel-Daten eines Spielers.
        :param player_name: Name des Spielers
        """

        # Spiel-Daten einlesen aus Datei player_name.player
        self.player_name = player_name
        self.load_game_data()

    def load_game_data(self):
        """
        Spieler-Daten einlesen
        """

        # Spiel-Daten einlesen aus Datei "player_name".player
        mypath = user_data_dir(const.APP_NAME, False, ensure_exists=True)
        dateiname = f"{mypath}/{self.player_name}.player"
        if os.path.exists(dateiname):
            with open(dateiname, "r") as ifile:
                self.game_data = json.load(ifile)
        else:
            # Falls es den Spieler noch nicht gibt, dann die Daten initialisieren und speichern
            self.game_data["books"] = {}
            self.game_data["room_keys"] = {}
            self.save_game_data()

        # Spieler-Daten gemäss allen book_xx_yy.json Files anpassen
        self.adjust_game_data()

    def save_game_data(self):
        """
        Spieler-Daten speichern
        """

        # Spiel-Daten speichern in Datei "player_name".player als JSON-Struktur
        mypath = user_data_dir(const.APP_NAME, False, ensure_exists=True)
        dateiname = f"{mypath}/{self.player_name}.player"
        with open(dateiname, "w") as ofile:
            json.dump(self.game_data, ofile, indent=2)

    def adjust_game_data(self):
        """
        Spieler-Daten aktualisieren
        """

        # Gelöschte Räume, Bücher und Aufgaben aus den game-daten entfernen
        book_to_del = []
        mypath = gd.get_abs_path("res/data")
        books = self.get_books()
        for room_nr in books:
            for book_nr in books[room_nr]:
                dateiname = f"{mypath}/book_{room_nr}_{book_nr}.json"
                if os.path.exists(dateiname):
                    with open(dateiname, "r", encoding="'utf-8") as ifile:
                        data = json.load(ifile)
                        anz_aufgaben = 0
                        if "Aufgaben" in data:
                            aufgaben = data["Aufgaben"]
                            anz_aufgaben = len(aufgaben)
                    while len(books[room_nr][book_nr]) > anz_aufgaben:
                        books[room_nr][book_nr].pop()

                else:
                    book_to_del.append((room_nr, book_nr))

        for room_nr, book_nr in book_to_del:
            books[room_nr].pop(book_nr)
        self.save_game_data()

        # Hinzugefügte Räume, Bücher und Aufgaben in die game-daten einfügen
        for r in range(9):
            for b in range(9):
                room_nr = str(r + 1).zfill(2)
                book_nr = str(b + 1).zfill(2)

                dateiname = f"{mypath}/book_{room_nr}_{book_nr}.json"
                if os.path.exists(dateiname):
                    with open(dateiname, "r", encoding="'utf-8") as ifile:
                        data = json.load(ifile)
                        if "Aufgaben" in data:
                            aufgaben = data["Aufgaben"]
                            self.init_book(room_nr, book_nr, len(aufgaben))

    def get_books(self):
        """
        Liefert die Bücher in den Spieler-Daten
        :return dict mit allen Büchern - kann leer sein
        """

        if "books" not in self.game_data:
            self.game_data["books"] = {}
        return self.game_data["books"]

    def init_book(self, room_nr, book_nr, anz_tasks: int = 0):
        """
        Buch init
        :param room_nr: Raum z.B. "02"
        :param book_nr: Buch z.B. "03"
        :param anz_tasks: Anzahl Aufgaben im Buch
        """

        # Dict mit den Büchern holen und falls etwas fehlt (Raum, Buch, Aufgabe) einfügen
        books = self.get_books()
        if room_nr not in books:
            books[room_nr] = {}
        if book_nr not in books[room_nr]:
            books[room_nr][book_nr] = []
        while len(books[room_nr][book_nr]) < anz_tasks:
            books[room_nr][book_nr].append(False)

        # Aktuelle Struktur speichern
        self.save_game_data()

    def set_task(self, room_nr: str, book_nr: str, task_nr: int):
        """
        Aufgabe als erledigt eintragen
        :param room_nr: Raum z.B. "02"
        :param book_nr: Buch z.B. "03"
        :param task_nr: Gelöste Aufgabe
        """

        # Sicherstellen, dass die Aufgabe in der Struktur vorhanden ist
        self.init_book(room_nr, book_nr, task_nr)

        # Und dann als erledigt kennzeichnen
        books = self.get_books()
        books[room_nr][book_nr][task_nr] = True

        # Aktuelle Struktur speichern
        self.save_game_data()

    def get_task(self, room_nr: str, book_nr: str, task_nr: int):
        """
        Liefert zurück, ob eine Aufgabe gelöst wurde
        :param room_nr: Raum z.B. "02"
        :param book_nr: Buch z.B. "03"
        :param task_nr: fragliche Aufgabe
        :return True, wenn gelöst, sonst False
        """

        # Sicherstellen, dass die Aufgabe in der Struktur vorhanden ist
        self.init_book(room_nr, book_nr, task_nr)

        # Und dann den bool Wert der Aufgabe zurückgeben
        books = self.get_books()
        return books[room_nr][book_nr][task_nr]

    def has_all_tasks(self, room_nr: str):
        """
        Prüfen, ob alle Aufgaben eines Raumes/Hauses gelöst sind
        :param room_nr: Raum z.B. "02"
        :return True, wenn alles gelöst, sonst False
        """
        books = self.get_books()
        if room_nr in books:
            for book_nr in books[room_nr]:
                for task in books[room_nr][book_nr]:
                    if not task:
                        return False
        else:
            return False

        return True

    def get_room_keys(self):
        """
        Liefert ein dict mit allen Schlüsseln der Häuser.
        :return dict room_keys
        """

        if "room_keys" not in self.game_data:
            self.game_data["room_keys"] = {}
        return self.game_data["room_keys"]

    def has_room_key(self, room_nr):
        """
        Prüft, ob ein Haus betreten werden darf oder nicht
        :param room_nr: Raum z.B. "02"
        :return True, wenn der Schlüssel für das Haus vorhanden ist, False sonst
        """
        keys = self.get_room_keys()
        if room_nr not in keys:
            return False
        return True

    def set_room_key(self, room_nr):
        """
        Setzt den Schlüssel für das Haus
        :param room_nr: Raum z.B. "02"
        """

        keys = self.get_room_keys()
        keys[room_nr] = True

        # Aktuelle Struktur speichern
        self.save_game_data()

    @staticmethod
    def delete_game_data(player_name):
        """
        Spieler-Daten löschen
        :param player_name: Name des Spielers
        """

        # Spiel-Daten Datei "player_name".player löschen
        mypath = user_data_dir(const.APP_NAME, False, ensure_exists=True)
        dateiname = f"{mypath}/{player_name}.player"
        if os.path.exists(dateiname):
            os.remove(dateiname)

    @staticmethod
    def get_abs_path(rel_path):
        """
        Liefert einen absoluten Pfad zu einer Datei
        :param rel_path: relativer Pfad
        :return kompletten absoluten Pfad
        """
        abs_path = path.abspath(path.join(path.dirname(__file__), "../.."))
        abs_path = path.abspath(path.join(abs_path, rel_path))
        return abs_path


# Einzige Instanz von GameData
gd = GameData()
