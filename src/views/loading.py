
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
        arcade.draw_text(
            "Loading...",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.started = True
        draw_bar(
            current_amount=self.progress,
            max_amount=100,
            center_x=self.window.width / 2,
            center_y=20,
            width=self.window.width,
            height=10,
            color_a=arcade.color.BLACK,
            color_b=arcade.color.WHITE,
        )

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


def draw_bar(current_amount,
             max_amount,
             center_x,
             center_y,
             width,
             height,
             color_a,
             color_b):

    # Draw the background
    if current_amount < max_amount:
        arcade.draw_rectangle_filled(center_x=center_x,
                                     center_y=center_y,
                                     width=width,
                                     height=height,
                                     color=color_a)

    # Calculate width
    bar_width = width * (current_amount / max_amount)

    # Draw filled part
    arcade.draw_rectangle_filled(center_x=center_x - 0.5 * (width - bar_width),
                                 center_y=center_y,
                                 width=bar_width,
                                 height=height,
                                 color=color_b)
