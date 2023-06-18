
import arcade
import arcade.gui
import json
from src.sprites.player import Player
from src.maps import load_maps
from src.views.game import Game
from src.views.menu import Menu
from src.views.settings import Settings
import os


class Loading(arcade.View):
    """
    Klasse für die View beim Laden der Daten (Maps und Views)
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()
        self.started = False
        self.done = False
        self.progress = 0
        self.map_list = None
        arcade.set_background_color(arcade.color.ALMOND)
        self.manager = arcade.gui.UIManager()
        label = arcade.gui.UILabel(x=0,
                                   align="center",
                                   y=600,
                                   height=50,
                                   width=self.window.width,
                                   text="Gib deinen Namen ein",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=24,
                                   multiline=False)

        self.manager.add(label)

        self.input_text = arcade.gui.UIInputText(x=400, y=500, width=200, height=50, font_size=24, text="")
        self.manager.add(self.input_text)

    def on_draw(self):
        """
        Zeichnet die View. Es wird ein Text "Loading" ausgegeben und ein
        Fortschrittsbalken, der anzeigt, wie viel schon geladen ist.
        """
        arcade.start_render()
        if not self.done:
            arcade.draw_text("Loading", self.window.width / 2, self.window.height / 2, arcade.color.GUPPIE_GREEN, 64,
                         anchor_x="center", anchor_y="center", align="center", width=self.window.width)

        self.started = True
        self.draw_bar()
        self.manager.draw()

    def setup(self):
        pass



    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

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
                eingabe = self.input_text.text.strip()
                if len(eingabe) > 0:
                    dateiname = (f"res/data/{eingabe}.json")
                    player=self.window.views["game"].player_sprite
                    if os.path.exists(dateiname):
                        with open(f"res/data/{eingabe}.json", "r") as ifile:
                            player.data= json.load(ifile)
                    else:
                        with open(f"res/data/{eingabe}.json", "w") as ofile:
                            pass
                    self.window.show_view(self.window.views["game"])

