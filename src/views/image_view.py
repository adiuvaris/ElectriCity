import os
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd

from src.data.image import Image


class ImageView(arcade.View):
    """
    Klasse für die View mit einem Bild
    """

    def __init__(self, figure: Image, view):
        """
        Konstruktor
        """

        super().__init__()

        self.figure = figure
        self.view = view

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

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.view)

    def create_ui(self):

        self.manager = arcade.gui.UIManager()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text=self.figure.title,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)

        self.manager.add(titel.with_border())

        # Bild Element erzeugen - falls Datei existiert
        filename = f"res/data/{self.figure.image_file}"
        if os.path.exists(filename):

            bs = arcade.Sprite(filename=filename)

            h = bs.height
            w = bs.width

            x = gd.scale(20)
            y = gd.scale(120)
            w = gd.scale(1240)
            h = gd.scale(520)

            image_sprite = arcade.gui.UISpriteWidget(x=x, y=y, width=w, height=h, sprite=bs)
            self.manager.add(image_sprite)
