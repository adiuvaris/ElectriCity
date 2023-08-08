import arcade
import arcade.gui

from src.data.game import gd


class Task:
    """
    Basis-Klasse für eine Aufgabe
    """

    def __init__(self, aufgabe: dict):
        self.aufgabe = []
        self.tipp = ""

        self.input_answer = None
        self.manager = None
        self.correct = False
        self.callback = None

        self.lose_sound = arcade.load_sound(":sounds:lose.wav")
        self.ok_sound = arcade.load_sound(":sounds:ok.wav")
        self.msg_active = False

        self.dauer = 0.0

        if "Aufgabe" in aufgabe:
            self.aufgabe = aufgabe["Aufgabe"]

        if "Tipp" in aufgabe:
            self.tipp = aufgabe["Tipp"]

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):

        self.manager = ui_manager
        self.callback = callback

        # Rahmen für den Aufgabenblock
        widget = arcade.gui.UIWidget(x=gd.scale(450), y=gd.scale(10), width=gd.scale(820), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        self.manager.add(border)

    def on_update(self, delta_time: float, window: arcade.Window):
        pass

    def on_key_press(self, key, modifiers):
        if self.msg_active:
            return

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.callback()
