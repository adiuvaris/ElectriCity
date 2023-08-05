import random
import os
import string
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.base.term import Term
from src.data.task import Task
from src.ui.attributed_text import AttributedText
from src.ui.message_box import MessageBox


class Karte:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.bild = ""
        self.key = ""
        self.button = None


class Frage:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.text = ""
        self.key = ""


class Puzzle(Task):
    def __init__(self, aufgabe: dict):
        super().__init__(aufgabe)

        self.karten = []
        self.fragen = []
        self.bild = ""

        self.buttons = {}
        self.grid = []
        self.grid_fragen = []

        self.aufgabe_text = None
        self.cur_frage = None

        self.dauer = 0.0

        if "Bild" in aufgabe:
            self.bild = aufgabe["Bild"]

        if "Fragen" in aufgabe:
            self.fragen = aufgabe["Fragen"]

        if "Karten" in aufgabe:
            self.karten = aufgabe["Karten"]

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):

        super().create_ui(ui_manager, callback)

        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=self.aufgabe)

        self.manager.add(self.aufgabe_text)

        style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}

        for k in self.fragen:
            frage = Frage()
            if "Text" in k:
                frage.text = k["Text"]
            if "Key" in k:
                frage.key = k["Key"]

            self.grid_fragen.append(frage)

        random.shuffle(self.grid_fragen)

        for k in self.karten:
            karte = Karte()
            if "Bild" in k:
                karte.bild = k["Bild"]
            if "Key" in k:
                karte.key = k["Key"]

            self.grid.append(karte)

        random.shuffle(self.grid)

        w = 200
        h = 200

        mypath = gd.get_abs_path("res/images")
        avatar_path = mypath + "/"

        for i in range(4):
            for j in range(3):

                karte = self.grid.pop(0)

                x = 460 + i * w
                y = 30 + j * h

                path = avatar_path + karte.bild
                te = arcade.load_texture(path, x=0, y=0, width=400, height=400)
                ib = arcade.gui.UITextureButton(x=gd.scale(x), y=gd.scale(y),
                                                width=gd.scale(w), height=gd.scale(h), texture=te, style=style)

                ib.on_click = self.on_puzzle_click
                karte.button = ib
                self.manager.add(ib)
                self.buttons[(i, j)] = karte

        self.cur_frage = self.grid_fragen.pop(0)

        aufgabe_text = self.aufgabe.copy()
        aufgabe_text.append(self.cur_frage.text)
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

        self.manager.add(self.aufgabe_text)

    def on_puzzle_click(self, event):

        for k in self.buttons:
            karte = self.buttons[k]
            b = karte.button
            if b == event.source:
                i = k[0]
                j = k[1]

                if karte.key == self.cur_frage.key:
                    arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)
                    mypath = gd.get_abs_path("res/images")
                    filename = f"{mypath}/{self.bild}"
                    if os.path.exists(filename):
                        te = arcade.load_texture(filename, x=i*200, y=(2-j)*200, width=200, height=200)
                        b.texture = te

                    self.manager.remove(self.aufgabe_text)

                    if len(self.grid_fragen) == 0:
                        self.correct = True

                        aufgabe_text = self.aufgabe.copy()
                        aufgabe_text.append("Mit der Esc-Taste geht es zum Spiel zurück.")
                        self.aufgabe_text = AttributedText(
                            x=gd.scale(20), y=gd.scale(20),
                            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                        self.manager.add(self.aufgabe_text)

                        self.buttons.pop(k)
                        self.manager.trigger_render()

                    else:
                        self.cur_frage = self.grid_fragen.pop(0)

                        aufgabe_text = self.aufgabe.copy()
                        aufgabe_text.append(self.cur_frage.text)
                        self.aufgabe_text = AttributedText(
                            x=gd.scale(20), y=gd.scale(20),
                            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                        self.manager.add(self.aufgabe_text)

                        self.buttons.pop(k)
                        self.manager.trigger_render()
                else:
                    arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)

                break

