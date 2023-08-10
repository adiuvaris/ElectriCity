import arcade
import arcade.gui

from src.data.game import gd
from src.ui.attributed_text import AttributedText


class Quiz:
    """
    Klasse für eine Quiz-Aufgabe
    """

    def __init__(self):
        """
        Konstruktor
        """

        # Member definieren
        self.text = ""

    def create_ui(self, ui_manager: arcade.gui.UIManager):
        """
        User-Interface erstellen
        :param ui_manager: Arcade UIManager
        """

        # Text anzeigen
        text = AttributedText(x=gd.scale(20), y=gd.scale(340),
                              width=gd.scale(400), height=gd.scale(300), text=self.text)
        ui_manager.add(text)
