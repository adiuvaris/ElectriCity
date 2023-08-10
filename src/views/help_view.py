import json
import os

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.ui.attributed_text import AttributedText


class HelpView(arcade.View):
    """
    Klasse für die View mit einem Text
    """

    def __init__(self, filename, parent):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Member definieren
        self.parent = parent
        self.text = []
        self.titel = ""

        # JSON-File für Text einlesen
        mypath = gd.get_abs_path("res/data")
        filename = f"{mypath}/{filename}"
        if os.path.exists(filename):
            with open(filename, "r", encoding="'utf-8") as ifile:
                data = json.load(ifile)
                if "Titel" in data:
                    self.titel = data["Titel"]
                if "Text" in data:
                    self.text = data["Text"]

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        self.create_ui()

    def setup(self):
        """
        View initialisieren.
        Es wird ein Bild angezeigt.
        """
        pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn die View unsichtbar wird
        """

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zum Aufrufer
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.parent)

    def create_ui(self):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        """

        # Zuerst mal Elemente löschen
        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)
        self.manager.clear()

        # Titeltext oben in der Mitte
        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text=self.titel,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        text = AttributedText(x=gd.scale(240), y=gd.scale(120),
                              width=gd.scale(800), height=gd.scale(520), text=self.text)

        self.manager.add(text)
