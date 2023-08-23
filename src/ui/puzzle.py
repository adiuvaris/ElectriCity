import os
import time
import random

import arcade
import arcade.gui

import src.const as const
from src.data.card import Card
from src.data.game import gd
from src.data.question import Question
from src.ui.attributed_text import AttributedText
from src.ui.task import Task


class Puzzle(Task):
    """
    Klasse für eine Aufgabe, die als Frage-Memory angezeigt wird
    """

    def __init__(self, aufgabe: dict):
        """
        Konstruktor
        :param aufgabe: eingelesene JSON-Struktur der Aufgabe
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__(aufgabe)

        self.karten = []
        self.fragen = []
        self.bg_bild = ""

        self.aufgabe_text = None
        self.cur_frage = None

        if "Bild" in aufgabe:
            self.bg_bild = aufgabe["Bild"]

        if "Fragen" in aufgabe:
            fragen = aufgabe["Fragen"]
            for k in fragen:
                frage = Question()
                if "Text" in k:
                    frage.text = k["Text"]
                if "Key" in k:
                    frage.key = k["Key"]
                self.fragen.append(frage)

        # Karten aus der Aufgabe in eine Liste von Card Objekten übernehmen
        if "Karten" in aufgabe:
            karten = aufgabe["Karten"]
            for k in karten:
                card = Card()
                if "Bild" in k:
                    card.bild = k["Bild"]
                if "Key" in k:
                    card.key = k["Key"]
                self.karten.append(card)

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        :param ui_manager: Arcade UIManager
        :param callback: Funktion, die zum Abschluss der Aufgabe aufgerufen werden soll
        """

        # Basisklasse aufrufen
        super().create_ui(ui_manager, callback)

        # Listen der Karten und Fragen mischen, damit das Memory immer anders aussieht.
        random.shuffle(self.karten)
        random.shuffle(self.fragen)

        # Breite und Höhe der Karten auf dem Bildschirm festlegen
        w = 266
        h = 200

        mypath = gd.get_abs_path("res/images")
        bild_path = mypath + "/"

        idx = 0
        for i in range(3):
            for j in range(3):

                # Da self.karten gemischt wurde, kann hier immer das nächste Element verwendet werden
                karte = self.karten[idx]
                karte.position = (i, j)
                idx = idx + 1

                # Position des Buttons berechnen
                x = 460 + i * w
                y = 30 + j * h

                path = bild_path + karte.bild
                te = arcade.load_texture(path, x=0, y=0, width=400, height=400)
                style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
                karte.button = arcade.gui.UITextureButton(
                    x=gd.scale(x+1), y=gd.scale(y+1),
                    width=gd.scale(w-2), height=gd.scale(h-2), texture=te, style=style)
                karte.button.on_click = self.on_puzzle_click
                self.manager.add(karte.button)

        # Die erste Frage anzeigen
        self.cur_frage = self.fragen.pop(0)

        # Aufgabentext auf der linken Seite
        aufgabe_text = self.aufgabe.copy()
        aufgabe_text.append(self.cur_frage.text)
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)
        self.manager.add(self.aufgabe_text)

    def on_puzzle_click(self, event):
        """
        Callback für den Klick auf eine Karte
        :param event: Event von Arcade
        """

        # Angeklickte Karte suchen
        for karte in self.karten:
            if karte.button == event.source:

                # Die Frage und die Karte passen zusammen, also Teil des Hintergrundbildes anzeigen
                if karte.key == self.cur_frage.key:

                    # Mit dem Ton anzeigen, dass die Antwort richtig ist
                    arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)
                    mypath = gd.get_abs_path("res/images")
                    filename = f"{mypath}/{self.bg_bild}"
                    if os.path.exists(filename):
                        self.manager.remove(karte.button)

                        # Teil des Hintergrundbildes extrahieren, der von der Karte verdeckt war
                        w = 266
                        h = 200
                        te = arcade.load_texture(
                            filename, x=karte.position[0] * w, y=(2 - karte.position[1]) * h, width=w, height=h)

                        x = 460 + karte.position[0] * w
                        y = 30 + karte.position[1] * h

                        # Antwort-Karte mit Bildteil ersetzen
                        style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
                        karte.button = arcade.gui.UITextureButton(
                            x=gd.scale(x), y=gd.scale(y),
                            width=gd.scale(w), height=gd.scale(h), texture=te, style=style)
                        self.manager.add(karte.button)

                    # Aufgabentext entfernen, damit die nächste Frage angezeigt werden kann.
                    self.manager.remove(self.aufgabe_text)

                    # Wenn alle Fragen beantwortet sind, dann kann der Spieler die View verlassen
                    if len(self.fragen) == 0:
                        self.correct = True

                        # Aufgabentext auf der linken Seite
                        aufgabe_text = self.aufgabe.copy()
                        aufgabe_text.append("Mit der Esc-Taste geht es zum Spiel zurück.")
                        self.aufgabe_text = AttributedText(
                            x=gd.scale(20), y=gd.scale(20),
                            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)
                        self.manager.add(self.aufgabe_text)

                        # self.callback()

                    else:
                        # Nächste Frage anzeigen
                        self.cur_frage = self.fragen.pop(0)

                        # Aufgabentext auf der linken Seite
                        aufgabe_text = self.aufgabe.copy()
                        aufgabe_text.append(self.cur_frage.text)
                        self.aufgabe_text = AttributedText(
                            x=gd.scale(20), y=gd.scale(20),
                            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)
                        self.manager.add(self.aufgabe_text)

                else:
                    # Mit dem Ton anzeigen, dass die Antwort falsch ist
                    arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)

                    # "Zur Strafe" muss der Spieler etwas warten
                    time.sleep(1.0)

                # Die Karte wurde gefunden, also können wir die Schleife verlassen
                self.manager.trigger_render()
                break
