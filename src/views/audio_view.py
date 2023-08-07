import os
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd

from src.sprites.animation import Animation
from src.data.media import Media


class AudioView(arcade.View):
    """
    Klasse für die View mit einem Bild
    """

    def __init__(self, figure: Media, view):
        """
        Konstruktor
        """

        super().__init__()

        self.figure = figure
        self.view = view

        self.media = None
        self.media_player = None

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

        if self.media is not None:
            if self.media.is_playing(self.media_player):
                return

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.view)

    def on_update(self, delta_time: float):
        pass

    def create_ui(self):

        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)

        self.manager.clear()

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
        if self.figure.illustration is not "":
            mypath = gd.get_abs_path("res/images")
            filename = f"{mypath}/{self.figure.illustration}"
            if os.path.exists(filename):
                self.sprite = arcade.Sprite(filename=filename)

                x = gd.scale(20)
                y = gd.scale(120)
                w = gd.scale(1240)
                h = gd.scale(520)

                widget = arcade.gui.UISpriteWidget(x=x, y=y, width=w, height=h, sprite=self.sprite)
                self.manager.add(widget)

        # Audio abspielen- falls Datei existiert
        mypath = gd.get_abs_path("res/sounds")
        filename = f"{mypath}/{self.figure.filename}"
        if os.path.exists(filename):
            self.media = arcade.load_sound(filename)
            self.media_player = arcade.play_sound(self.media, volume=gd.get_volume() / 100.0)

