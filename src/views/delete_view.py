import os
from os.path import isfile, join

import arcade
import arcade.gui
from platformdirs import *

import src.const as const
from src.data.game import gd


class DeleteView(arcade.View):
    """
    Klasse für die View beim Löschen eines Spielers
    """

    def __init__(self):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Member definieren
        self.manager = arcade.gui.UIManager()
        self.players = None
        self.setup()

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

        arcade.start_render()
        self.manager.draw()

    def setup(self):
        """
        View initialisieren.
        Es wird die Theorie für den Raum und das Buch angezeigt.
        """

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
            self.window.start_view.setup()
            self.window.show_view(self.window.start_view)

    def on_click(self, event):
        """
        Callback für den Klick auf einen Player
        :param event: Event von Arcade
        """

        # Spieler löschen
        gd.delete_game_data(event.source.text)

        # Zurück zur Start View
        self.window.start_view.setup()
        self.window.show_view(self.window.start_view)

    def create_ui(self):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        """

        # Zuerst mal Elemente löschen
        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)
        self.manager.clear()

        # Titeltext oben in der Mitte
        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text="Einen Spieler löschen",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        # Falls es schon gespeicherte Player-Files hat, dann diese als Buttons anzeigen
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
                ib = arcade.gui.UIFlatButton(x=x, y=y, width=gd.scale(200), height=gd.scale(40), text=p, style=style)
                ib.on_click = self.on_click
                self.manager.add(ib)

                x = x + gd.scale(210)
                i = i + 1
                if i > 5:
                    i = 0
                    x = gd.scale(20)
                    y = y - gd.scale(50)
