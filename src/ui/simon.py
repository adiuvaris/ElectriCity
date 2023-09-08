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
        self.raster = 2
        self.count = 0
        self.number = 0
        self.running = False
        self.show_number = False
        self.hide_number = False
        self.dauer = 0.0
        self.spiel = []

        # Aus dem Raster eine Liste von Karten erzeugen
        for i in range(self.raster):
            for j in range(self.raster):
                card = Card()
                card.key = str(j * self.raster + i + 1).zfill(2)
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
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=self.aufgabe)
        self.manager.add(self.aufgabe_text)

        # Buttons für alle Karten erzeugen
        i = 0
        for karte in self.karten:

            # Breite und Höhe der Karten auf dem Bildschirm festlegen
            # Position des Buttons für die Karte berechnen
            w = gd.scale(int(620 / self.raster))
            h = w
            x = gd.scale(550) + karte.position[0] * w
            y = gd.scale(20) + karte.position[1] * h

            style = {"font_size": 3 * gd.scale(const.FONT_SIZE_H1), "bg_color": (100, 0, 0)}
            if i == 1:
                style = {"font_size": 3 * gd.scale(const.FONT_SIZE_H1), "bg_color": (0, 100, 0)}
            elif i == 2:
                style = {"font_size": 3 * gd.scale(const.FONT_SIZE_H1), "bg_color": (0, 0, 100)}
            elif i == 3:
                style = {"font_size": 3 * gd.scale(const.FONT_SIZE_H1), "bg_color": (0, 100, 100)}

            i = i + 1

            karte.button = arcade.gui.UIFlatButton(
                x=x + gd.scale(2), y=y + gd.scale(2), width=w - gd.scale(4), height=h - gd.scale(4),
                text="", style=style)
            karte.button.on_click = self.on_simon_click
            self.manager.add(karte.button)

    def on_update(self, delta_time: float):

        self.dauer = self.dauer + delta_time
        if self.dauer > 1.0:
            self.dauer = 0.0

            if self.show_number:
                karte = self.karten[self.spiel[self.number]]
                karte.button.text = str(self.number + 1)
                self.show_number = False
                self.hide_number = True

            elif self.hide_number:
                karte = self.karten[self.spiel[self.number]]
                karte.button.text = ""

                self.number = self.number + 1
                self.show_number = True
                self.hide_number = False

                if self.number == self.count:
                    self.number = 0
                    self.show_number = False
                    self.hide_number = False
                    self.running = True

                    self.manager.remove(self.aufgabe_text)
                    text = ["Wiederhole die Sequenz durch Klicks auf die farbigen Flächen"]
                    self.aufgabe_text = AttributedText(
                        x=gd.scale(20), y=gd.scale(20),
                        width=gd.scale(400), height=gd.scale(300), text=text)
                    self.manager.add(self.aufgabe_text)
                    self.manager.trigger_render()

    def on_simon_click(self, event):
        """
        Callback für den Klick auf eine Karte
        :param event: Event von Arcade
        """
        if not self.running:
            return

        # Angeklickte Karte suchen
        for karte in self.karten:
            if karte.button == event.source:

                self.manager.remove(self.aufgabe_text)
                text = self.aufgabe

                ref_karte = self.karten[self.spiel[self.number]]
                if karte == ref_karte:
                    self.number = self.number + 1
                    if self.number == self.count:
                        arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)
                        self.running = False
                        self.number = 0
                    else:
                        text = ["Wiederhole die Sequenz durch Klicks auf die farbigen Flächen"]

                else:
                    arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)
                    self.running = False

                self.aufgabe_text = AttributedText(
                    x=gd.scale(20), y=gd.scale(20),
                    width=gd.scale(400), height=gd.scale(300), text=text)
                self.manager.add(self.aufgabe_text)

    def on_key_press(self, key, modifiers):
        """
        Callback, wenn eine Taste gedrückt wurde
        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Taste auch an Basisklasse melden
        super().on_key_press(key, modifiers)

        # Leertaste gedrückt?
        if key == arcade.key.SPACE or key == arcade.key.NUM_SPACE:

            self.manager.remove(self.aufgabe_text)
            text = ["Merke dir die Sequenz"]
            self.aufgabe_text = AttributedText(
                x=gd.scale(20), y=gd.scale(20),
                width=gd.scale(400), height=gd.scale(300), text=text)
            self.manager.add(self.aufgabe_text)
            self.manager.trigger_render()

            self.count = 4
            self.spiel.clear()
            for i in range(self.count):
                r = random.randint(0, 3)
                self.spiel.append(r)

            self.number = 0
            self.running = False
            self.show_number = True
            self.hide_number = True

