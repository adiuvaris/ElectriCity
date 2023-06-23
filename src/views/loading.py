
import arcade
import arcade.gui

import src.const as const

from src.data.player_data import PlayerData
from src.data.game_data import GameData

from src.maps import load_maps
from src.views.game import Game
from src.views.menu import Menu
from src.views.settings import Settings


class Loading(arcade.View):
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
        self.titel = None
        self.create_ui()

        arcade.set_background_color(arcade.color.ALMOND)

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
        pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """
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

                self.window.views["game"] = Game(self.map_list)
                self.window.views["game"].setup()

                self.window.views["menu"] = Menu()
                self.window.views["menu"].setup()

                self.window.views["settings"] = Settings()
                self.window.views["settings"].setup()

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

        if key == arcade.key.ENTER:

            if self.done:
                player_name = self.input_text.text.strip()
                if len(player_name) > 0:

                    player_data = PlayerData()
                    player_data.init_player(player_name)

                    self.window.show_view(self.window.views["game"])

    def create_ui(self):
        game_data = GameData()
        scale = game_data.get_scale()

        self.manager.clear()

        self.titel = arcade.gui.UILabel(x=0, y=game_data.do_scale(660),
                                   width=self.window.width, height=game_data.do_scale(30),
                                   text="Starte ElectriCity",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=game_data.do_scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(self.titel.with_border())

        label = arcade.gui.UILabel(x=game_data.do_scale(20),
                                   y=game_data.do_scale(600),
                                   width=game_data.do_scale(290),
                                   height=game_data.do_scale(30),
                                   text="Gib deinen Namen ein:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=game_data.do_scale(const.FONT_SIZE_H2),
                                   multiline=False)

        self.manager.add(label)

        self.input_text = arcade.gui.UIInputText(x=game_data.do_scale(340), y=game_data.do_scale(600),
                                                 width=game_data.do_scale(290), height=game_data.do_scale(30),
                                                 font_size=game_data.do_scale(const.FONT_SIZE_H2), text="")
        self.manager.add(self.input_text)

#        arcade.draw_text("Loading", self.window.width / 2, self.window.height / 2, arcade.color.GUPPIE_GREEN, 64,
#                         anchor_x="center", anchor_y="center", align="center", width=self.window.width)

        self.manager.trigger_render()