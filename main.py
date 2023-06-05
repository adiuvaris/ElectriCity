
import arcade
import src.const as const
from src.views.loading import Loading


class MainWindow(arcade.Window):
    """
    Hauptfenster des Programms als Instanz eines arcade-windows
    """

    def __init__(self):
        """
        Konstruktor.
        Initialisiert das Fenster und definiert Pfade
        """

        super().__init__(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, const.SCREEN_TITLE, resizable=True)
        self.views = {}

        # Pfade zu einzelnen Ressourcen definieren, damit im Programm
        # leichter darauf zugegriffen werden kann.
        arcade.resources.add_resource_handle("maps", "res/maps")
        arcade.resources.add_resource_handle("characters", "res/characters")
        arcade.resources.add_resource_handle("sounds", "res/sounds")


def main():
    """
    Hauptfunktion des Programms.
    Startet den Main-Loop von arcade.
    """

    window = MainWindow()
    window.center_window()
    start_view = Loading()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
