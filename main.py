
import arcade
import src.const as const
from src.views.loading import Loading


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, const.SCREEN_TITLE, resizable=True)
        self.views = {}

        arcade.resources.add_resource_handle("maps", "res/maps")
        arcade.resources.add_resource_handle("characters", "res/characters")
        arcade.resources.add_resource_handle("sounds", "res/sounds")


def main():
    window = MainWindow()
    window.center_window()
    start_view = Loading()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
