import os
from os.path import isfile, join
from platformdirs import *
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd


class DeleteView(arcade.View):
    """
    Klasse für die View beim Löschen eines Spiels
    """

    def __init__(self, menu):
        """
        Konstruktor
        """

        super().__init__()

        self.menu = menu

        self.manager = arcade.gui.UIManager()
        self.players = None
        self.setup()

    def on_draw(self):
        """
        Zeichnet die View. Es wird ein Text "Loading" ausgegeben und ein
        Fortschrittsbalken, der anzeigt, wie viel schon geladen ist.
        """
        arcade.start_render()
        self.manager.draw()

    def setup(self):
        # Verzeichnis in dem die Player-Daten liegen
        mypath = user_data_dir(const.APP_NAME, False, ensure_exists=True)

        # Alle Dateien mit der Endung player laden
        self.players = [
            f[:-7]
            for f in os.listdir(mypath)
            if isfile(join(mypath, f)) and f.endswith(".player")
        ]

        self.create_ui()

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """
        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn die View unsichtbar wird
        """

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zum Menü
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.menu)

    def create_ui(self):

        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)

        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text="Spieler löschen",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        if len(self.players) > 0:
            label = arcade.gui.UILabel(x=gd.scale(20),
                                       y=gd.scale(600),
                                       width=gd.scale(1240),
                                       height=gd.scale(30),
                                       text="Klicke auf den zu löschenden Spieler oder drücke die Taste Esc.",
                                       text_color=[0, 0, 0],
                                       bold=True,
                                       font_size=gd.scale(const.FONT_SIZE_H2),
                                       multiline=False)

            self.manager.add(label)

            x = gd.scale(20)
            y = gd.scale(550)
            i = 0
            for p in self.players:
                style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
                ib = arcade.gui.UIFlatButton(x=x, y=y, width=gd.scale(270), height=gd.scale(40), text=p, style=style)
                ib.on_click = self.on_click
                self.manager.add(ib)

                x = x + gd.scale(310)
                i = i + 1
                if i > 3:
                    i = 0
                    x = gd.scale(20)
                    y = y - gd.scale(50)

    def on_click(self, event):
        gd.delete_game_data(event.source.text)

        self.window.start_view.setup()
        self.window.show_view(self.window.start_view)

