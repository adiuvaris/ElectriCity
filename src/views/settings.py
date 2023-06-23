
import arcade
import arcade.gui

import src.const as const

from src.base.term import Term
from src.data.game_data import GameData
from src.ui.attributed_text import AttributedText


class Settings(arcade.View):
    """
    Klasse für die View mit den Einstellungen - macht zurzeit noch nichts
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        self.input_text = None

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

        if key == arcade.key.ENTER:
            scale = self.input_text.text.strip()
            if scale.isnumeric():

                game_data = GameData()
                game_data.set_scale(int(scale))

                w = game_data.do_scale(const.SCREEN_WIDTH)
                h = game_data.do_scale(const.SCREEN_HEIGHT)

                self.window.set_size(w, h)
                self.window.center_window()

                self.window.views["game"].on_resize(w, h)
                self.window.views["menu"].on_resize(w, h)
                self.window.views["settings"].on_resize(w, h)

        # Escape geht zurück zum Menü
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["menu"])

    def on_click_back(self, event):
        """
        Klick-handler, wenn "Zurück zum Spiel" angeklickt wurde
        :param event:
        """

        self.window.show_view(self.window.views["menu"])

    def on_resize(self, width, height):
        """
        Wird von arcade aufgerufen, wenn die Fenstergrösse ändert.

        :param width: neue Breite
        :param height: neue Höhe
        """
        self.create_ui()

    def create_ui(self):
        game_data = GameData()
        scale = game_data.get_scale()

        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=game_data.do_scale(660),
                                   width=self.window.width, height=game_data.do_scale(30),
                                   text="Einstellungen",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=game_data.do_scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        label = arcade.gui.UILabel(x=game_data.do_scale(20), y=game_data.do_scale(600),
                                   width=self.window.width, height=game_data.do_scale(30),
                                   text="Fenstergrösse in Prozent:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="left",
                                   font_size=game_data.do_scale(const.FONT_SIZE_H2),
                                   multiline=False)

        self.manager.add(label)

        self.input_text = arcade.gui.UIInputText(x=game_data.do_scale(340), y=game_data.do_scale(600),
                                                 width=game_data.do_scale(290), height=game_data.do_scale(30),
                                                 font_size=game_data.do_scale(const.FONT_SIZE_H2), text=str(scale))

        self.manager.add(self.input_text)

        button = arcade.gui.UIFlatButton(x=game_data.do_scale(20), y=game_data.do_scale(20),
                                         width=game_data.do_scale(290), text="Zurück")

        button.on_click = self.on_click_back

        self.manager.add(button)

        self.manager.trigger_render()
