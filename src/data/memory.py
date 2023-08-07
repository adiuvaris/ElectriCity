import random
import time
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.task import Task
from src.ui.attributed_text import AttributedText


class Karte:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.bild = ""
        self.key = ""
        self.button = None


class Memory(Task):
    def __init__(self, aufgabe: dict):
        super().__init__(aufgabe)
        self.karten = []
        self.first_karte = None
        self.second_karte = None

        self.buttons = {}
        self.grid = []
        self.grid_fragen = []

        self.aufgabe_text = None

        if "Karten" in aufgabe:
            self.karten = aufgabe["Karten"]

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):

        super().create_ui(ui_manager, callback)

        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=self.aufgabe)

        self.manager.add(self.aufgabe_text)

        for k in self.karten:
            karte = Karte()
            if "Bild" in k:
                karte.bild = k["Bild"]
            if "Key" in k:
                karte.key = k["Key"]

            self.grid.append(karte)

        random.shuffle(self.grid)

        w = 200
        h = 150

        mypath = gd.get_abs_path("res/images")
        avatar_path = mypath + "/back.png"
        te = arcade.load_texture(avatar_path, x=0, y=0, width=200, height=200)

        # self.grid = [[0 for i in range(0, 4)] for j in range(0, 3)]
        style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}

        for i in range(4):
            for j in range(4):
                karte = self.grid.pop(0)

                x = 460 + i * w
                y = 30 + j * h
                ib = arcade.gui.UITextureButton(x=gd.scale(x + 5), y=gd.scale(y + 5),
                                                width=gd.scale(w - 10), height=gd.scale(h - 10), texture=te,
                                                style=style)

                ib.on_click = self.on_memory_click
                karte.button = ib
                self.manager.add(ib)
                self.buttons[(i, j)] = karte

    def on_memory_click(self, event):

        if self.first_karte is not None and self.second_karte is not None:
            return

        for k in self.buttons:
            karte = self.buttons[k]
            b = karte.button
            if b == event.source:
                i = k[0]
                j = k[1]

                mypath = gd.get_abs_path("res/images")
                avatar_path = mypath + "/" + karte.bild
                te = arcade.load_texture(avatar_path, x=0, y=0, width=400, height=400)
                b.texture = te

                self.manager.trigger_render()

                if self.first_karte is None:
                    self.first_karte = karte
                else:
                    if karte == self.first_karte:
                        return

                    self.second_karte = karte

                    self.manager.remove(self.aufgabe_text)

                    aufgabe_text = self.aufgabe.copy()
                    aufgabe_text.append("Weiter mit der Leer-Taste.")
                    self.aufgabe_text = AttributedText(
                        x=gd.scale(20), y=gd.scale(20),
                        width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                    self.manager.add(self.aufgabe_text)
                    self.manager.trigger_render()

                    if self.first_karte.key == self.second_karte.key:
                        arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)
                    else:
                        arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)

                break

    def on_key_press(self, key, modifiers):
        if self.msg_active:
            return

        super().on_key_press(key, modifiers)

        if key == arcade.key.SPACE or key == arcade.key.NUM_SPACE:
            if self.first_karte is not None and self.second_karte is not None:

                self.manager.remove(self.aufgabe_text)

                aufgabe_text = self.aufgabe.copy()
                self.aufgabe_text = AttributedText(
                    x=gd.scale(20), y=gd.scale(20),
                    width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                self.manager.add(self.aufgabe_text)

                if self.first_karte.key == self.second_karte.key:

                    for k in self.buttons:
                        karte = self.buttons[k]
                        if karte == self.first_karte:
                            self.buttons.pop(k)
                            break

                    for k in self.buttons:
                        karte = self.buttons[k]
                        if karte == self.second_karte:
                            self.buttons.pop(k)
                            break

                    self.manager.remove(self.first_karte.button)
                    self.manager.remove(self.second_karte.button)
                    self.first_karte = None
                    self.second_karte = None

                    if len(self.buttons) == 0:
                        self.correct = True

                        self.manager.remove(self.aufgabe_text)

                        aufgabe_text = self.aufgabe.copy()
                        aufgabe_text.append("Mit der Esc-Taste geht es zum Spiel zurück.")
                        self.aufgabe_text = AttributedText(
                            x=gd.scale(20), y=gd.scale(20),
                            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                        self.manager.add(self.aufgabe_text)

                else:
                    time.sleep(2.0)

                    mypath = gd.get_abs_path("res/images")
                    avatar_path = mypath + "/back.png"
                    te = arcade.load_texture(avatar_path, x=0, y=0, width=200, height=200)
                    self.first_karte.button.texture = te
                    self.second_karte.button.texture = te
                    self.first_karte = None
                    self.second_karte = None

