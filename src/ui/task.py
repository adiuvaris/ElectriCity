import arcade
import arcade.gui

from src.data.game import gd


class Task:
    """
    Basis-Klasse für eine Aufgabe
    """

    def __init__(self, aufgabe: dict):
        """
        Konstruktor
        """

        # Member definieren
        self.aufgabe = []
        self.tipp = ""

        self.input_answer = None
        self.manager = None
        self.correct = False
        self.callback = None

        self.lose_sound = arcade.load_sound(":sounds:lose.wav")
        self.ok_sound = arcade.load_sound(":sounds:ok.wav")
        self.msg_active = False

        if "Aufgabe" in aufgabe:
            self.aufgabe = aufgabe["Aufgabe"]

        if "Tipp" in aufgabe:
            self.tipp = aufgabe["Tipp"]

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):
        """
        User-Interface erstellen - nur den Rahmen für die Aufgabe
        :param ui_manager: Arcade UIManager
        :param callback: Funktion, die zum Abschluss der Aufgabe aufgerufen werden soll
        """

        self.manager = ui_manager
        self.callback = callback

        # Rahmen für den Aufgabenblock einfügen
        widget = arcade.gui.UIWidget(x=gd.scale(450), y=gd.scale(10), width=gd.scale(820), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        self.manager.add(border)

    def on_key_press(self, key, modifiers):
        """
        Callback, wenn eine Taste gedrückt wurde
        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Wenn eine Meldung angezeigt wird, dann den Tasten ignorieren
        if self.msg_active:
            return

        # Escape geht in jedem Fall zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.callback()
