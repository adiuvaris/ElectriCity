import arcade
import arcade.gui

from src.data.game import gd
from src.ui.attributed_text import AttributedText


class Quiz:
    """
    Klasse für eine Quiz-Aufgabe
    """

    def __init__(self):
        self.text = ""

    def create_ui(self, ui_manager: arcade.gui.UIManager):

        widget = arcade.gui.UIWidget(x=gd.scale(10), y=gd.scale(10), width=gd.scale(420), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        ui_manager.add(border)

        text = AttributedText(x=gd.scale(20), y=gd.scale(340),
                              width=gd.scale(400), height=gd.scale(300), text=self.text)

        ui_manager.add(text)
