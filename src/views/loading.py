
import arcade

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
        self.started = False
        self.progress = 0
        self.map_list = None
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        """
        Zeichnet die View. Es wird ein Text "Loading" ausgegeben und ein
        Fortschrittsbalken, der anzeigt, wie viel schon geladen ist.
        """
        arcade.start_render()
        arcade.draw_text("Loading...", self.window.width / 2, self.window.height / 2, arcade.color.GUPPIE_GREEN, 64,
                         anchor_x="center", anchor_y="center", align="center", width=self.window.width)

        self.started = True
        self.draw_bar()

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        """
        Diese Funktion wird von arcade immer wieder aufgerufen. Sie ruft
        die Funktion load_maps solange auf, bis diese angibt, dass alles
        geladen ist. Danach wird zur GameView gewechselt.

        :param delta_time: vergangene Zeit seit letztem Aufruf
        """
        if self.started:
            done, self.progress, self.map_list = load_maps()
            if done:
                self.window.views["game"] = Game(self.map_list)
                self.window.views["game"].setup()

                self.window.views["menu"] = Menu()
                self.window.views["menu"].setup()

                self.window.views["settings"] = Settings()
                self.window.views["settings"].setup()

                self.window.show_view(self.window.views["game"])

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
