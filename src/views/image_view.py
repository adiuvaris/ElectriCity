import os

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.media import Media
from src.sprites.animation import Animation


class ImageView(arcade.View):
    """
    Klasse für die View mit einem Bild
    """

    def __init__(self, media: Media, view):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Member definieren
        self.media = media
        self.view = view
        self.sprite = None

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

    def on_update(self, delta_time: float):

        if self.media.frames > 0:
            self.sprite.on_update(delta_time)

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
                                   text=self.media.title,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        # Bild Element erzeugen - falls Datei existiert
        mypath = gd.get_abs_path("res/images")
        filename = f"{mypath}/{self.media.filename}"
        if os.path.exists(filename):

            if self.media.frames > 0:
                self.sprite = Animation(filename=filename, frames=self.media.frames)
            else:
                self.sprite = arcade.Sprite(filename=filename)

            x = gd.scale(20)
            y = gd.scale(120)
            w = gd.scale(1240)
            h = gd.scale(520)

            widget = arcade.gui.UISpriteWidget(x=x, y=y, width=w, height=h, sprite=self.sprite)
            self.manager.add(widget)
