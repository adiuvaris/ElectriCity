import os

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.media import Media
from src.ui.attributed_text import AttributedText


class AudioView(arcade.View):
    """
    Klasse für das Abspielen einer Audio-Datei.
    Es kann eine Illustration angezeigt werden.
    Die Ausgabe kann nicht gestoppt werden.
    """

    def __init__(self, media: Media, parent):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Member definieren
        self.media = media
        self.parent = parent

        self.sound = None
        self.media_player = None
        self.sprite = None

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        # Anzeigeelemente erstellen
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
        Callback, wenn eine Taste gedrückt wurde
        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Solange die Ausgabe läuft, keine Tasten akzeptieren
        if self.sound is not None:

            if key == arcade.key.KEY_0 or key == arcade.key.NUM_0:
                self.media_player.seek(0.0)

            if self.sound.is_playing(self.media_player):

                if key == arcade.key.SPACE:
                    self.media_player.pause()

                if (key == arcade.key.UP or key == arcade.key.NUM_UP or
                        key == arcade.key.RIGHT or key == arcade.key.NUM_RIGHT):
                    if self.media_player.volume < 1.0:
                        self.media_player.volume = self.media_player.volume + 0.1

                if (key == arcade.key.DOWN or key == arcade.key.NUM_DOWN or
                        key == arcade.key.LEFT or key == arcade.key.NUM_LEFT):
                    if self.media_player.volume > 0.1:
                        self.media_player.volume = self.media_player.volume - 0.1

                return

            else:
                if key == arcade.key.SPACE:
                    self.media_player.play()

        # Escape geht zurück zur aufrufenden View
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
                                   text=self.media.title,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        hinweis = ["Die Ausgabe kann mit der <i><b>Leertaste</b></i> pausiert werden. Mit der Taste <i><b>Null</b></i> beginnt das Gespräch von vorne.",
                   "Mit den <i><b>Pfeiltasten</b></i> kann die Lautstärke angepasst werden."]
        text = AttributedText(x=gd.scale(20), y=gd.scale(20),
                              width=gd.scale(1240),
                              height=gd.scale(80),
                              text=hinweis)

        self.manager.add(text)

        # Bild Element erzeugen - falls Datei existiert
        if self.media.illustration != "":
            mypath = gd.get_abs_path("res/images")
            filename = f"{mypath}/{self.media.illustration}"
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
        filename = f"{mypath}/{self.media.filename}"
        if os.path.exists(filename):
            self.sound = arcade.load_sound(filename)
            self.media_player = arcade.play_sound(self.sound, volume=gd.get_volume() / 100.0)
