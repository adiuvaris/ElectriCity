
import arcade

from src.maps import load_maps
from src.views.game import Game

# from src.views.main_menu import MainMenu
# from src.views.settings import Settings


class Loading(arcade.View):

    def __init__(self):
        super().__init__()
        self.started = False
        self.progress = 0
        self.map_list = None
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Loading...", self.window.width / 2, self.window.height / 2, arcade.color.GUPPIE_GREEN, 64,
                         anchor_x="center", anchor_y="center", align="center", width=self.window.width)

        self.started = True
        self.draw_bar()

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        if self.started:
            done, self.progress, self.map_list = load_maps()
            if done:
                self.window.views["game"] = Game(self.map_list)
                self.window.views["game"].setup()

                # self.window.views["main_menu"] = MainMenu()
                # self.window.views["main_menu"].setup()

                # self.window.views["settings"] = Settings()
                # self.window.views["settings"].setup()

                self.window.show_view(self.window.views["game"])

    def draw_bar(self):
        # Hintergrund zeichnen
        if self.progress < 100:
            arcade.draw_rectangle_filled(center_x=self.window.width / 2, center_y=20,
                                         width=self.window.width, height=20, color=arcade.color.BLACK)

        # Aktuelle Breite berechnen
        bar_width = self.window.width * (self.progress / 100.0)

        # Gefüllten Teil zeichnen
        arcade.draw_rectangle_filled(center_x=self.window.width / 2 - 0.5 * (self.window.width - bar_width),
                                     center_y=20, width=bar_width, height=20, color=arcade.color.WHITE)
