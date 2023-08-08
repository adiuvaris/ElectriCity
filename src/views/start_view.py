import os
from os.path import isfile, join
from platformdirs import *
import arcade
import arcade.gui

import src.const as const

from src.data.game import gd

from src.maps import load_maps
from src.views.game_view import GameView
from src.views.help_view import HelpView
from src.views.delete_view import DeleteView


class StartView(arcade.View):
    """
    Klasse für die View beim Laden der Daten (Maps und Views)
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()

        # Attribute definieren
        self.started = False
        self.done = False
        self.progress = 0
        self.map_list = None

        self.manager = arcade.gui.UIManager()
        self.input_text = None
        self.players = None
        self.setup()

    def on_draw(self):
        """
        Zeichnet die View. Es wird ein Text "Loading" ausgegeben und ein
        Fortschrittsbalken, der anzeigt, wie viel schon geladen ist.
        """
        arcade.start_render()
        if not self.done:
            self.draw_bar()

        self.started = True
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
        self.create_ui()

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

        # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
        if self.input_text is not None:
            event = arcade.gui.UIMousePressEvent(
                x=self.input_text.x + 1, y=self.input_text.y + 1, button=0, modifiers=0, source=self)
            self.input_text.on_event(event)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn die View unsichtbar wird
        """

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_update(self, delta_time: float):
        """
        Diese Funktion wird von arcade immer wieder aufgerufen. Sie ruft
        die Funktion load_maps solange auf, bis diese angibt, dass alles
        geladen ist. Danach wird zur GameView gewechselt.

        :param delta_time: vergangene Zeit seit letztem Aufruf
        """
        if self.started:
            if not self.done:
                self.done, self.progress, self.map_list = load_maps()
            if self.done:
                self.window.game_view = GameView(self.map_list)

    def draw_bar(self):
        """
        Zeichnet den Fortschrittsbalken. Es wird ein schwarzer Balken gezeichnet, der den Progress-Wert
        im Verhältnis zur Fensterbreite darstellt.
        """
        # Hintergrund zeichnen
        if self.progress < 100:
            arcade.draw_rectangle_filled(center_x=self.window.width / 2, center_y=20,
                                         width=self.window.width, height=20, color=arcade.color.BLACK)

        # Aktuelle Breite berechnen
        bar_width = self.window.width * (self.progress / 100.0)

        # Gefüllten Teil zeichnen
        arcade.draw_rectangle_filled(center_x=self.window.width / 2 - 0.5 * (self.window.width - bar_width),
                                     center_y=20, width=bar_width, height=20, color=arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        if key == arcade.key.F1 or key == arcade.key.NUM_F1:
            hint = HelpView("anleitung.json", self)
            self.window.show_view(hint)

        if key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:

            if self.done:
                player_name = self.input_text.text.strip()
                player_name.replace('\n', '')
                if len(player_name) > 0:
                    self.start_game(player_name)

    def create_ui(self):

        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)

        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text="Starte ElectriCity",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        label = arcade.gui.UILabel(x=gd.scale(20),
                                   y=gd.scale(600),
                                   width=gd.scale(290),
                                   height=gd.scale(30),
                                   text="Gib deinen Namen ein:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)

        self.manager.add(label)

        self.input_text = arcade.gui.UIInputText(x=gd.scale(340), y=gd.scale(600),
                                                 width=gd.scale(290), height=gd.scale(30),
                                                 font_size=gd.scale(const.FONT_SIZE_H2), text="")
        self.manager.add(self.input_text.with_border())

        if len(self.players) > 0:
            label = arcade.gui.UILabel(x=gd.scale(20),
                                       y=gd.scale(550),
                                       width=gd.scale(1240),
                                       height=gd.scale(30),
                                       text="Oder klicke auf einen vorhandenen Spieler, um das Spiel zu starten.",
                                       text_color=[0, 0, 0],
                                       bold=True,
                                       font_size=gd.scale(const.FONT_SIZE_H2),
                                       multiline=False)

            self.manager.add(label)

            style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
            x = gd.scale(20)
            y = gd.scale(500)
            i = 0
            for p in self.players:
                ib = arcade.gui.UIFlatButton(x=x, y=y, width=gd.scale(200), height=gd.scale(40), text=p, style=style)
                ib.on_click = self.on_click
                self.manager.add(ib)

                x = x + gd.scale(210)
                i = i + 1
                if i > 5:
                    i = 0
                    x = gd.scale(20)
                    y = y - gd.scale(50)

            del_button = arcade.gui.UIFlatButton(x=gd.scale(500),
                                                 y=gd.scale(200),
                                                 width=gd.scale(280),
                                                 height=gd.scale(40),
                                                 text="Einen Spieler löschen...",
                                                 style=style)

            del_button.on_click = self.on_click_del_game
            self.manager.add(del_button)

        hint = arcade.gui.UILabel(x=gd.scale(20),
                                  y=gd.scale(100),
                                  width=gd.scale(1280),
                                  height=gd.scale(30),
                                  text="Drücke die Taste 'F1' für eine kurze Anleitung.",
                                  text_color=[0, 0, 0],
                                  bold=True,
                                  font_size=gd.scale(const.FONT_SIZE_H2),
                                  align="center",
                                  multiline=False)

        self.manager.add(hint)

    def on_click_del_game(self, event):
        delete_view = DeleteView()
        self.window.show_view(delete_view)

    def on_click(self, event):
        if self.done:
            self.start_game(event.source.text)

    def start_game(self, player_name):
        gd.init_player(player_name)

        self.window.game_view.setup()

        # Fenstergrösse für die gewünschte Skalierung anpassen
        w = gd.scale(const.SCREEN_WIDTH)
        h = gd.scale(const.SCREEN_HEIGHT)
        self.window.set_size(w, h)
        self.window.center_window()

        # Game über die Anpassung informieren und anzeigen
        self.window.game_view.on_resize(w, h)
        self.window.show_view(self.window.game_view)
