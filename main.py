
import arcade
import pyglet.window
import src.const as const
from src.data.game import gd
from src.views.start_view import StartView


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

        # Game View
        self.game_view = None

        # Pfade zu einzelnen Ressourcen definieren, damit im Programm
        # leichter darauf zugegriffen werden kann.
        arcade.resources.add_resource_handle("maps", gd.get_abs_path("res/maps"))
        arcade.resources.add_resource_handle("sounds", gd.get_abs_path("res/sounds"))


def main():
    """
    Hauptfunktion des Programms.
    Startet den Main-Loop von arcade.
    """

    # Window Instanz erzeugen und zentrieren.
    window = MainWindow()
    window.center_window()

    # Loading View erzeugen und starten
    start_view = StartView()
    start_view.setup()
    window.show_view(start_view)

    # Arcade Endlos-Schleife starten.
    arcade.run()


if __name__ == "__main__":
    main()

# Bilden mit folgendem Kommando Python Package PyInstaller muss installiert sein.
# Die *.player Files in res/data vorher löschen.
#   WINDOWS: pyinstaller main.py  --add-data "res;res" --windowed --name ElectriCity
#   MAC:     pyinstaller main.py  --add-data "res:res" --windowed --name ElectriCity
