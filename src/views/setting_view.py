import os
from os.path import isfile, join

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd


class SettingView(arcade.View):
    """
    Klasse für die View mit den Einstellungen - macht zurzeit noch nichts
    """

    def __init__(self, menu):
        """
        Konstruktor
        """

        super().__init__()

        # Verzeichnis in dem die Player-Daten liegen
        mypath = "res/avatars"

        # Alle Dateien mit der Endung .png laden
        self.avatars = [
            f"res/avatars/{f}"
            for f in os.listdir(mypath)
            if isfile(join(mypath, f)) and f.endswith(".png")
        ]

        self.menu = menu

        # UIManager braucht es für arcade
        self.input_text = None
        self.manager = arcade.gui.UIManager()
        self.create_ui()

        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """
        self.clear()
        self.manager.draw()

    def setup(self):
        """
        View initialisieren.
        Macht zurzeit noch nichts
        """
        pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """
        self.manager.enable()

        # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
        event = arcade.gui.UIMousePressEvent(
            x=self.input_text.x + 1, y=self.input_text.y + 1, button=0, modifiers=0, source=self)
        self.input_text.on_event(event)

        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn die View unsichtbar wird
        """

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        if key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:
            scale = self.input_text.text.strip()
            if scale.isnumeric():

                gd.set_scale(int(scale))

                w = gd.scale(const.SCREEN_WIDTH)
                h = gd.scale(const.SCREEN_HEIGHT)

                self.window.set_size(w, h)
                self.window.center_window()

                # Game über die Anpassung informieren
                self.window.game_view.on_resize(w, h)
                self.menu.on_resize(w, h)
                self.on_show_view()

        # Escape geht zurück zum Menü
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.menu)

    def on_resize(self, width, height):
        """
        Wird von arcade aufgerufen, wenn die Fenstergrösse ändert.

        :param width: neue Breite
        :param height: neue Höhe
        """
        self.create_ui()

    def create_ui(self):
        scale = gd.get_scale()

        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)

        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text="Einstellungen",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        label = arcade.gui.UILabel(x=gd.scale(20), y=gd.scale(600),
                                   width=gd.scale(290), height=gd.scale(30),
                                   text="Fenstergrösse in Prozent:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)

        self.manager.add(label)

        self.input_text = arcade.gui.UIInputText(x=gd.scale(340), y=gd.scale(600),
                                                 width=gd.scale(290), height=gd.scale(30),
                                                 font_size=gd.scale(const.FONT_SIZE_H2), text=str(scale))

        self.manager.add(self.input_text)

        label = arcade.gui.UILabel(x=gd.scale(20), y=gd.scale(500),
                                   width=gd.scale(290),
                                   height=30,
                                   text="Wähle einen Avatar:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)

        self.manager.add(label)

        mypath = "res/avatars"

        x = gd.scale(340)
        y = gd.scale(480)
        for avatar in self.avatars:
            te = arcade.load_texture(avatar, x=0, y=0, width=const.SPRITE_SIZE, height=const.SPRITE_SIZE)
            if avatar == gd.get_avatar():
                ib = arcade.gui.UITextureButton(x=x, y=y, width=gd.scale(40), height=gd.scale(40), texture=te).with_border()
            else:
                ib = arcade.gui.UITextureButton(x=x, y=y, width=gd.scale(40), height=gd.scale(40), texture=te)

            ib.on_click = self.on_click
            self.manager.add(ib)


            x = x + gd.scale(50)

    def on_click(self, event):
        x = event.x - gd.scale(340)
        idx = int(x / gd.scale(50))
        if 0 <= idx < len(self.avatars):
            gd.set_avatar(self.avatars[idx])
            self.create_ui()
