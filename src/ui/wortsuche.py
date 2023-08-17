import random
import string

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.wort import Wort
from src.data.card import Card
from src.ui.attributed_text import AttributedText
from src.ui.task import Task


class Wortsuche(Task):
    """
    Klasse für eine Wortsuche-Aufgabe
    """

    def __init__(self, aufgabe: dict):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__(aufgabe)

        # Member definieren
        self.words = []
        self.karten = []
        self.raster = 20

        self.such_worte = {}
        self.cur_such_wort = None
        self.first_karte = None
        self.aufgabe_text = None

        if "Raster" in aufgabe:
            self.raster = aufgabe["Raster"]

        if "Worte" in aufgabe:
            self.words = aufgabe["Worte"]

            # Das Raster muss 1 grösser als das längste Wort sein
            # sonst können die Wörter nichts zufällig im Grid platziert werden
            for word in self.words:
                if self.raster <= len(word):
                    self.raster = len(word) + 1

            # Zufälliges Raster von Buchstaben erstellen
            grid = [[random.choice(string.ascii_uppercase) for i in range(0, self.raster)] for j in range(0, self.raster)]
            already_taken = []

            # Suchwörter in das Raster eintragen
            for word in self.words:
                stop = 0
                ok = self.put_word(word, grid, already_taken)
                while not ok and stop < 100:
                    ok = self.put_word(word, grid, already_taken)
                    stop += 1
                else:
                    pass

            # Aus dem Raster eine Liste von Karten erzeugen
            for i in range(self.raster):
                for j in range(self.raster):
                    card = Card()
                    card.key = grid[i][j]
                    card.position = (i, j)
                    self.karten.append(card)

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        :param ui_manager: Arcade UIManager
        :param callback: Funktion, die zum Abschluss der Aufgabe aufgerufen werden soll
        """

        # Basisklasse aufrufen
        super().create_ui(ui_manager, callback)

        # Aufgabentext auf der linken Seite
        aufgabe_text = self.aufgabe.copy()
        aufgabe_text.extend(self.words)
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)
        self.manager.add(self.aufgabe_text)

        # Buttons für alle Karten (Buchstaben) erzeugen
        for karte in self.karten:

            # Position des Buttons für die Karte berechnen
            w = gd.scale(int(620 / self.raster))
            h = w
            x = gd.scale(550) + karte.position[0] * w
            y = gd.scale(20) + karte.position[1] * h
            style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
            karte.button = arcade.gui.UIFlatButton(
                x=x, y=y, width=w, height=h,
                text=karte.key, style=style)
            karte.button.on_click = self.on_wortsuche_click
            self.manager.add(karte.button)

    def on_wortsuche_click(self, event):
        """
        Callback für den Klick auf eine Karte
        :param event: Event von Arcade
        """

        # Angeklickte Karte suchen
        for karte in self.karten:
            if karte.button == event.source and karte.button.text != "":

                # Ist es die erste Karte, dann nur die Karte merken und den Buchstaben entfernen
                if self.first_karte is None:
                    self.first_karte = karte
                    self.first_karte.button.text = ""
                    self.cur_such_wort = None

                    # Prüfen, ob der angeklickte Buchstabe der erste oder der letzte
                    # eines Suchwortes ist - potenzielles Suchwort merken
                    for wk in self.such_worte:
                        such_wort = self.such_worte[wk]
                        if such_wort.start_pos == karte.position:
                            such_wort.start_found = True
                            self.cur_such_wort = such_wort

                        elif such_wort.end_pos == karte.position:
                            such_wort.end_found = True
                            self.cur_such_wort = such_wort

                else:

                    # Wenn das der zweite Klick ist und kein potenzielles Suchwort aktiv ist,
                    # dann einen Ton für den Misserfolg ausgeben.
                    if self.cur_such_wort is None:
                        arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)
                        self.first_karte.button.text = self.first_karte.key
                        self.first_karte = None
                    else:

                        # Prüfen, ob hier das andere Ende des potenziellen Suchworts gefunden wurde
                        such_wort = self.cur_such_wort
                        if such_wort.start_pos == karte.position:
                            such_wort.start_found = True
                        elif such_wort.end_pos == karte.position:
                            such_wort.end_found = True

                        # Start und Ende gefunden?
                        if such_wort.start_found and such_wort.end_found:

                            # Ton für den erfolg ausgeben und
                            arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)

                            # Alle Buchstaben des Worts entfernen
                            for position in such_wort.positionen:
                                idx = position[0] * self.raster + position[1]
                                self.karten[idx].button.text = ""

                            # Gefundenes Wort aus der Liste der zu Suchenden entfernen
                            self.words.remove(such_wort.wort)

                            # Werte für die Suche zurücksetzen.
                            self.first_karte = None
                            self.cur_such_wort = None

                            # Wenn alle Wörter gefunden wurden, dann kann der Spieler die View verlassen
                            self.manager.remove(self.aufgabe_text)
                            if len(self.words) == 0:
                                self.correct = True
                                self.callback()

                            else:

                                # Aufgabentext anpassen
                                aufgabe_text = self.aufgabe.copy()
                                aufgabe_text.extend(self.words)
                                self.aufgabe_text = AttributedText(
                                    x=gd.scale(20), y=gd.scale(20),
                                    width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                            self.manager.add(self.aufgabe_text)
                        else:
                            # Einen Ton für den Misserfolg ausgeben.
                            arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)
                            self.first_karte.button.text = self.first_karte.key

                            # Werte für die Suche zurücksetzen.
                            self.first_karte = None
                            self.cur_such_wort = None

                break

        self.manager.trigger_render()

    def put_word(self, word, grid, already_taken):
        """
        Wort ins Grid eintragen
        :param word: Wort
        :param grid: Buchstaben-Bitter
        :param already_taken: bereits verwendete Einträge im Grid
        """

        # Wort zufällig umdrehen oder eben nicht
        rand_word = random.choice([word, word[::-1]])

        # Zufällig eine Richtung wählen links-rechts, rechts-links oder diagonal
        d = random.choice([[1, 0], [0, 1], [1, 1]])

        # Notwendige Grössen abhängig von Richtung berechnen
        x_size = self.raster if d[0] == 0 else self.raster - len(rand_word)
        y_size = self.raster if d[1] == 0 else self.raster - len(rand_word)

        # Zufällige Startposition
        x = random.randrange(0, x_size)
        y = random.randrange(0, y_size)

        # Zwischenspeicher für Positionen des Wortes
        wort_positionen = []
        start_pos = (x, y)
        end_pos = (x, y)

        # Versuchen Wort zu platzieren
        for i in range(0, len(rand_word)):
            x_pos = x + d[0] * i
            y_pos = y + d[1] * i
            check = (x_pos, y_pos)

            # Wenn die Position schon von einem anderen Wort verwendet wird,
            # dann kann das Wort so nicht platziert werden
            if check in already_taken:

                # Die Positionen des Wortes zurückgeben, da sie nicht benötigt werden.
                for pos in wort_positionen:
                    already_taken.remove(pos)

                # Dem Aufrufer mitteilen, dass er es nochmals versuchen soll
                return False

            else:
                # Die Position als verwendet markieren
                already_taken.append(check)

                # Informationen für das Suchwort zwischenspeichern
                end_pos = check
                wort_positionen.append(check)

        # Die Buchstaben des Worts im Grid eintragen
        for i in range(0, len(rand_word)):
            x_pos = x + d[0] * i
            y_pos = y + d[1] * i
            grid[x_pos][y_pos] = rand_word[i]

        # Suchwort Struktur erzeugen
        such_wort = Wort(word)
        such_wort.positionen = wort_positionen
        such_wort.start_pos = start_pos
        such_wort.end_pos = end_pos
        self.such_worte[word] = such_wort

        return True
