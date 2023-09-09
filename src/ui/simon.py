import random
import time

import arcade
import arcade.gui

import src.const as const
from src.data.card import Card
from src.data.game import gd
from src.ui.attributed_text import AttributedText
from src.ui.task import Task


class Simon(Task):
    """
    Klasse für eine Aufgabe, die als Simon says angezeigt wird
    """

    def __init__(self, aufgabe: dict):
        """
        Konstruktor
        :param aufgabe: eingelesene JSON-Struktur der Aufgabe
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__(aufgabe)

        # Member definieren
        self.karten = []
        self.aufgabe_text = None
        self.state = "start"
        self.level = 4
        self.cur_card = 0
        self.dauer = 0.0
        self.timer = 0
        self.spiel = []
        self.player = None

        # Die vier Karten für das Spiel erzeugen
        for i in range(2):
            for j in range(2):
                card = Card()
                card.position = (i, j)
                card.sound = arcade.load_sound(f":sounds:simon_{i}{j}.wav")
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
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=self.aufgabe)
        self.manager.add(self.aufgabe_text)

        # Buttons für alle Karten erzeugen
        i = 0
        for karte in self.karten:

            # Breite und Höhe der Karten auf dem Bildschirm festlegen
            # Position des Buttons für die Karte berechnen
            w = gd.scale(int(620 / 2))
            h = w
            x = gd.scale(550) + karte.position[0] * w
            y = gd.scale(20) + karte.position[1] * h

            style = {"font_size": 4 * gd.scale(const.FONT_SIZE_H1), "bg_color": (100, 0, 0), "bg_color_pressed": (200, 0, 0)}
            if i == 1:
                style = {"font_size": 4 * gd.scale(const.FONT_SIZE_H1), "bg_color": (0, 100, 0), "bg_color_pressed": (0, 200, 0)}
            elif i == 2:
                style = {"font_size": 4 * gd.scale(const.FONT_SIZE_H1), "bg_color": (0, 0, 100), "bg_color_pressed": (0, 0, 200)}
            elif i == 3:
                style = {"font_size": 4 * gd.scale(const.FONT_SIZE_H1), "bg_color": (0, 100, 100), "bg_color_pressed": (0, 200, 200)}

            i = i + 1

            karte.button = arcade.gui.UIFlatButton(
                x=x + gd.scale(2), y=y + gd.scale(2), width=w - gd.scale(4), height=h - gd.scale(4),
                text="", style=style)
            karte.button.on_click = self.on_simon_click
            self.manager.add(karte.button)

    def on_update(self, delta_time: float):

        self.dauer = self.dauer + delta_time

        if self.state == "start":
            return

        elif self.state == "game":
            self.dauer = 0.0
            self.show_aufgaben_text()
            while len(self.spiel) < self.level:
                r = random.randint(0, 3)
                self.spiel.append(r)

            self.cur_card = 0
            self.timer = 2 * self.level
            self.state = "show"
            self.show_aufgaben_text()

        elif self.state == "error":
            if self.dauer > 1.0:
                self.dauer = 0.0
                arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)
                self.state = "start"
                self.show_aufgaben_text()

        elif self.state == "nextlevel":
            if self.dauer > 1.0:
                self.dauer = 0.0
                arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)
                if self.level > gd.get_max_level():
                    gd.set_max_level(self.level)
                self.level = self.level + 1
                self.state = "game"

        elif self.state == "show":
            if self.dauer > 1.0:
                self.dauer = 0.0
                if self.cur_card > 0:
                    karte = self.karten[self.spiel[self.cur_card - 1]]
                    karte.button.text = ""

                if self.cur_card == len(self.spiel):
                    self.cur_card = 0
                    self.state = "play"
                    self.show_aufgaben_text()
                else:
                    karte = self.karten[self.spiel[self.cur_card]]
                    karte.button.text = str(self.cur_card + 1)
                    arcade.play_sound(karte.sound, volume=gd.get_volume() / 100.0)
                    self.cur_card = self.cur_card + 1

        elif self.state == "play":
            if self.dauer > 1.0:
                self.dauer = 0.0
                self.timer = self.timer - 1
                self.show_aufgaben_text()
                if self.timer == 0:
                    arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)
                    self.state = "start"
                    self.show_aufgaben_text()

    def on_simon_click(self, event):
        """
        Callback für den Klick auf eine Karte
        :param event: Event von Arcade
        """

        # Nur auf Klicks reagieren, wenn der Spieler dran ist
        if self.state != "play":
            return

        if self.player is not None:
            self.player.pause()

        # Angeklickte Karte suchen
        for karte in self.karten:
            if karte.button == event.source:
                self.player = arcade.play_sound(karte.sound, volume=gd.get_volume() / 100.0)
                ref_karte = self.karten[self.spiel[self.cur_card]]
                if karte == ref_karte:
                    self.cur_card = self.cur_card + 1
                    if self.cur_card == len(self.spiel):
                        self.dauer = 0.0
                        self.state = "nextlevel"
                else:
                    self.dauer = 0.0
                    self.state = "error"

                break

    def on_key_press(self, key, modifiers):
        """
        Callback, wenn eine Taste gedrückt wurde
        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Taste auch an Basisklasse melden
        super().on_key_press(key, modifiers)

        # Nur im Zustand start auf Tasten reagieren
        if self.state == "start":

            # Leertaste gedrückt?
            if key == arcade.key.SPACE or key == arcade.key.NUM_SPACE:

                # Neues Spiel init
                self.spiel.clear()
                self.level = 4
                self.cur_card = 0
                self.state = "game"

    def show_aufgaben_text(self):

        max_level = gd.get_max_level()
        text_liste = []
        if self.state == "start":
            text_liste.append("Starte ein neues Spiel mit der Leertaste.")
        elif self.state == "game":
            text_liste.append(f"Merke dir die Sequenz von {self.level} Karten.")
        elif self.state == "show":
            text_liste.append(f"Merke dir die Sequenz von {self.level} Karten.")
        elif self.state == "play":
            text_liste.append(f"Wiederhole die Sequenz von {self.level} Karten.")
            text_liste.append(f"Du hast noch {self.timer} Sekunden zeit.")

        text_liste.append("")
        text_liste.append(f"Maximale Anzahl wiederholter Karten <b>{max_level}</b>")

        self.manager.remove(self.aufgabe_text)
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=text_liste)
        self.manager.add(self.aufgabe_text)
        self.manager.trigger_render()
