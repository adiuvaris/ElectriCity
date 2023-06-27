
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

        self.menu = menu

        # UIManager braucht es für arcade
        self.input_text = None
        self.manager = None
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

    def on_click_back(self, event):
        """
        Klick-handler, wenn "Zurück zum Spiel" angeklickt wurde
        :param event:
        """
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

        self.manager = arcade.gui.UIManager()

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
                                   width=self.window.width, height=gd.scale(30),
                                   text="Fenstergrösse in Prozent:",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="left",
                                   font_size=gd.scale(const.FONT_SIZE_H2),
                                   multiline=False)

        self.manager.add(label)

        self.input_text = arcade.gui.UIInputText(x=gd.scale(340), y=gd.scale(600),
                                                 width=gd.scale(290), height=gd.scale(30),
                                                 font_size=gd.scale(const.FONT_SIZE_H2), text=str(scale))

        self.manager.add(self.input_text)

        button = arcade.gui.UIFlatButton(x=gd.scale(20), y=gd.scale(20),
                                         width=gd.scale(290), text="Zurück")

        button.on_click = self.on_click_back

        self.manager.add(button)
