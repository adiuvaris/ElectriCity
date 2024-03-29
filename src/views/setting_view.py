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

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Verzeichnis in dem die Player-Daten liegen
        mypath = gd.get_abs_path("res/avatars")

        # Alle Avatar Dateien mit der Endung .png laden
        self.avatars = [
            f"{f}"
            for f in os.listdir(mypath)
            if isfile(join(mypath, f)) and f.endswith(".png")
        ]

        # Member definieren
        self.menu = menu
        self.input_scale = None
        self.input_volume = None
        self.active_input = None

        # UIManager braucht es für arcade
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

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """
        # Escape geht zurück zum Menü
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.menu)

        # ENTER startet das Spiel, aber nur wenn der Name des Spielers nicht leer ist
        if key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:
            input_text = self.active_input.text.strip()
            input_text.replace('\n', '')
            if input_text.isnumeric():
                if self.active_input == self.input_scale:

                    # Nur Werte zwischen 50 und 200 erlauben
                    scale = int(input_text)
                    if scale < 50:
                        scale = 50
                    elif scale > 200:
                        scale = 200

                    self.input_scale.text = str(scale)
                    gd.set_scale(scale)

                    w = gd.scale(const.SCREEN_WIDTH)
                    h = gd.scale(const.SCREEN_HEIGHT)

                    self.window.set_size(w, h)
                    self.window.center_window()

                    # Game über die Anpassung informieren
                    self.window.game_view.on_resize(w, h)
                    self.menu.on_resize(w, h)
                    self.on_resize(w, h)

                    # Nächstes Eingabefeld aktivieren.
                    self.active_input = self.input_volume

                elif self.active_input == self.input_volume:

                    # Nur Werte zwischen 0 und 100 erlauben
                    volume = int(input_text)
                    if volume < 0:
                        volume = 0
                    elif volume > 100:
                        volume = 100

                    self.input_volume.text = str(volume)
                    gd.set_volume(volume)

                    # Nächstes Eingabefeld aktivieren.
                    self.active_input = self.input_scale

                # Event erzeugen, um zu emulieren, dass im nächsten Eingabefeld geklickt worden sei
                event = arcade.gui.UIMousePressEvent(
                    x=self.active_input.x + 1, y=self.active_input.y + 1, button=0, modifiers=0, source=self)
                self.input_volume.on_event(event)
                self.input_scale.on_event(event)

            else:
                if self.active_input == self.input_scale:
                    self.active_input.text = str(gd.get_scale())
                elif self.active_input == self.input_volume:
                    self.active_input.text = str(gd.get_volume())

    def on_click(self, event):
        """
        Klick auf Avatar verarbeiten

        :param event: Event von Arcade
        """

        # Koordinaten umrechnen
        x = event.x - gd.scale(340)
        idx = int(x / gd.scale(50))
        if 0 <= idx < len(self.avatars):

            # Gewählten Avatar in die Spieler-Daten eintragen und UI neu zeichnen
            gd.set_avatar(self.avatars[idx])
            self.create_ui()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        Wird von arcade aufgerufen bei Mausklick.
        Hier wird das aktuelle Eingabefeld festgelegt, wenn in ein solches geklickt wird

        :param x: x-Koordinate
        :param y: y-Koordinate
        :param button: Maustaste
        :param modifiers: Shift, Alt etc.
        """

        if self.input_scale.rect.collide_with_point(x, y):
            self.active_input = self.input_scale

        elif self.input_volume.rect.collide_with_point(x, y):
            self.active_input = self.input_volume

        # Funktion in der Basisklasse aufrufen
        super().on_mouse_press(x=x, y=y, button=button, modifiers=modifiers)

    def on_resize(self, width, height):
        """
        Wird von arcade aufgerufen, wenn die Fenstergrösse ändert.

        :param width: neue Breite
        :param height: neue Höhe
        """
        self.create_ui()

    def create_ui(self):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        """

        # Zuerst mal Elemente löschen
        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)
        self.manager.clear()

        # Aktuelle Werte holen
        scale = gd.get_scale()
        volume = gd.get_volume()

        # Titeltext oben in der Mitte
        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text="Einstellungen",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        # Fenstergrösse
        label = arcade.gui.UILabel(x=gd.scale(20), y=gd.scale(600),
                                   width=gd.scale(290), height=gd.scale(30),
                                   text="Fenstergrösse in Prozent:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)
        self.manager.add(label)

        label = arcade.gui.UILabel(x=gd.scale(500), y=gd.scale(600),
                                   width=gd.scale(290), height=gd.scale(30),
                                   text="(Werte von 50 bis 200)",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)
        self.manager.add(label)

        self.input_scale = arcade.gui.UIInputText(x=gd.scale(340), y=gd.scale(600),
                                                  width=gd.scale(90), height=gd.scale(30),
                                                  font_size=gd.scale(const.FONT_SIZE_H2), text=str(scale))
        self.manager.add(self.input_scale.with_border())

        # Lautstärke
        label = arcade.gui.UILabel(x=gd.scale(20), y=gd.scale(550),
                                   width=gd.scale(290), height=gd.scale(30),
                                   text="Lautstärke in Prozent:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)
        self.manager.add(label)

        label = arcade.gui.UILabel(x=gd.scale(500), y=gd.scale(550),
                                   width=gd.scale(290), height=gd.scale(30),
                                   text="(Werte von 0 bis 100)",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)
        self.manager.add(label)

        self.input_volume = arcade.gui.UIInputText(x=gd.scale(340), y=gd.scale(550),
                                                   width=gd.scale(90), height=gd.scale(30),
                                                   font_size=gd.scale(const.FONT_SIZE_H2), text=str(volume))
        self.manager.add(self.input_volume.with_border())

        # Avatar Auswahl
        label = arcade.gui.UILabel(x=gd.scale(20), y=gd.scale(500),
                                   width=gd.scale(290),
                                   height=30,
                                   text="Wähle einen Avatar:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)
        self.manager.add(label)

        # Mögliche Avatare anzeigen als Bild
        mypath = gd.get_abs_path("res/avatars")
        x = gd.scale(340)
        y = gd.scale(480)
        for avatar in self.avatars:
            avatar_path = mypath + "/" + avatar
            te = arcade.load_texture(avatar_path, x=0, y=0, width=const.SPRITE_SIZE, height=const.SPRITE_SIZE)
            if avatar == gd.get_avatar():
                ib = arcade.gui.UITextureButton(x=x, y=y, width=gd.scale(40), height=gd.scale(40),
                                                texture=te).with_border()
            else:
                ib = arcade.gui.UITextureButton(x=x, y=y, width=gd.scale(40), height=gd.scale(40), texture=te)

            ib.on_click = self.on_click
            self.manager.add(ib)
            x = x + gd.scale(50)

        # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
        self.active_input = self.input_scale
        event = arcade.gui.UIMousePressEvent(
            x=self.active_input.x + 1, y=self.active_input.y + 1, button=0, modifiers=0, source=self)
        self.input_volume.on_event(event)
        self.input_scale.on_event(event)
