import arcade
import arcade.gui

import src.const as const

from src.data.game import gd

from src.maps import load_maps
from src.views.game_view import GameView
from src.views.help_view import HelpView


class StartView(arcade.View):
    """
    Klasse für die View beim Laden der Daten (Maps und Views)
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()

        # Attribute definieren
        self.started = False
        self.done = False
        self.progress = 0
        self.map_list = None

        self.manager = arcade.gui.UIManager()
        self.input_text = None
        self.create_ui()

    def on_draw(self):
        """
        Zeichnet die View. Es wird ein Text "Loading" ausgegeben und ein
        Fortschrittsbalken, der anzeigt, wie viel schon geladen ist.
        """
        arcade.start_render()
        if not self.done:
            self.draw_bar()

        self.started = True
        self.manager.draw()

    def setup(self):
        pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """
        self.create_ui()

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

        # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
        if self.input_text is not None:
            event = arcade.gui.UIMousePressEvent(
                x=self.input_text.x + 1, y=self.input_text.y + 1, button=0, modifiers=0, source=self)
            self.input_text.on_event(event)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn die View unsichtbar wird
        """

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_update(self, delta_time: float):
        """
        Diese Funktion wird von arcade immer wieder aufgerufen. Sie ruft
        die Funktion load_maps solange auf, bis diese angibt, dass alles
        geladen ist. Danach wird zur GameView gewechselt.

        :param delta_time: vergangene Zeit seit letztem Aufruf
        """
        if self.started:
            if not self.done:
                self.done, self.progress, self.map_list = load_maps()
            if self.done:
                self.window.game_view = GameView(self.map_list)
                self.window.game_view.setup()

    def draw_bar(self):
        """
        Zeichnet den Fortschrittsbalken. Es wird ein schwarzer Balken gezeichnet, der den Progress-Wert
        im Verhältnis zur Fensterbreite darstellt.
        """
        # Hintergrund zeichnen
        if self.progress < 100:
            arcade.draw_rectangle_filled(center_x=self.window.width / 2, center_y=20,
                                         width=self.window.width, height=20, color=arcade.color.BLACK)

        # Aktuelle Breite berechnen
        bar_width = self.window.width * (self.progress / 100.0)

        # Gefüllten Teil zeichnen
        arcade.draw_rectangle_filled(center_x=self.window.width / 2 - 0.5 * (self.window.width - bar_width),
                                     center_y=20, width=bar_width, height=20, color=arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        if key == arcade.key.F1 or key == arcade.key.NUM_F1:
            hint = HelpView("anleitung.json", self)
            self.window.show_view(hint)

        if key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:

            if self.done:
                player_name = self.input_text.text.strip()
                if len(player_name) > 0:
                    gd.init_player(player_name)

                    # Fenstergrösse für die gewünschte Skalierung anpassen
                    w = gd.scale(const.SCREEN_WIDTH)
                    h = gd.scale(const.SCREEN_HEIGHT)
                    self.window.set_size(w, h)
                    self.window.center_window()

                    # Game über die Anpassung informieren und anzeigen
                    self.window.game_view.on_resize(w, h)
                    self.window.show_view(self.window.game_view)

    def create_ui(self):
        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=670,
                                   width=self.window.width, height=30,
                                   text="Starte ElectriCity",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=const.FONT_SIZE_H1,
                                   multiline=False)
        self.manager.add(titel.with_border())

        label = arcade.gui.UILabel(x=20,
                                   y=600,
                                   width=290,
                                   height=30,
                                   text="Gib deinen Namen ein:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=const.FONT_SIZE_H2,
                                   multiline=False)

        self.manager.add(label)

        self.input_text = arcade.gui.UIInputText(x=340, y=600,
                                                 width=290, height=30,
                                                 font_size=const.FONT_SIZE_H2, text="")
        self.manager.add(self.input_text.with_border())

        hint = arcade.gui.UILabel(x=20,
                                   y=200,
                                   width=1280,
                                   height=30,
                                   text="Drücke die Taste 'F1' für eine kurze Anleitung.",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   font_size=const.FONT_SIZE_H2,
                                  align="center",
                                   multiline=False)

        self.manager.add(hint)
