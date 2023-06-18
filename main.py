
import arcade
import pyglet.window
import src.const as const
from src.views.loading import Loading


class MainWindow(arcade.Window):
    """
    Hauptfenster des Programms als Instanz eines arcade-windows
    """

    def __init__(self):
        """
        Konstruktor.
        Initialisiert das Fenster und definiert Pfade zu Ressourcen
        """

        super().__init__(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, const.SCREEN_TITLE,
                         style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)

        # Dictionary für geladene Views
        self.views = {}

        # Pfade zu einzelnen Ressourcen definieren, damit im Programm
        # leichter darauf zugegriffen werden kann.
        arcade.resources.add_resource_handle("maps", "res/maps")
        arcade.resources.add_resource_handle("characters", "res/characters")
        arcade.resources.add_resource_handle("sounds", "res/sounds")
        arcade.resources.add_resource_handle("textures", "res/textures")


def main():
    """
    Hauptfunktion des Programms.
    Startet den Main-Loop von arcade.
    """

    # Window Instanz erzeugen und zentrieren.
    window = MainWindow()
    window.center_window()

    # Loading View erzeugen und starten
    start_view = Loading()
    start_view.setup()
    window.show_view(start_view)

    # Arcade Endlos-Schleife starten.
    arcade.run()


if __name__ == "__main__":
    main()

# Bilden mit folgendem Kommando
#   WINDOWS: pyinstaller main.py --add-data "res;res --windowed"
#   MAC:     pyinstaller main.py --add-data "res:res --windowed"
