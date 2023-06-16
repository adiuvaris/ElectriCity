import arcade
import arcade.gui
import json

import src.const as const
from src.views.question import Question


class Theory(arcade.View):
    """
    Klasse für die View mit Theorie oder Aufgabe
    """

    def __init__(self, room, book):
        """
        Konstruktor
        """

        super().__init__()

        self.room = room
        self.book = book

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

    def setup(self):
        """
        View initialisieren.
        Es wird die Theorie für den Raum und das Buch angezeigt.
        """

        self.manager.clear()

        fx = self.window.width / const.SCREEN_WIDTH
        fy = self.window.height / const.SCREEN_HEIGHT

        with open(f"res/data/t_{self.room}_{self.book}.json", "r", encoding="'utf-8") as ifile:
            d = json.load(ifile)
            titel = d["Titel"]
            text = "\n".join(d["Text"])

            x = 30 * fx
            y = 740 * fy
            w = 1140 * fx
            h = 30 * fy
            fs = 20 * fy
            ui_titel_label = arcade.gui.UILabel(x=x,
                                                y=y,
                                                width=w,
                                                height=h,
                                                text=titel,
                                                text_color=[0, 0, 0],
                                                bold=True,
                                                align="center",
                                                font_size=fs,
                                                multiline=False)

            self.manager.add(
                ui_titel_label.with_space_around(top=5, left=5, bottom=5, right=5, bg_color=[220, 220, 220]))

            x = 30 * fx
            y = 110 * fy
            w = 1140 * fx
            h = 580 * fy
            fs = 14 * fy
            ui_text_label = arcade.gui.UITextArea(x=x,
                                                  y=y,
                                                  width=w,
                                                  height=h,
                                                  text=text,
                                                  text_color=[0, 0, 0],
                                                  font_size=fs,
                                                  multiline=True)

            self.manager.add(
                ui_text_label.with_space_around(top=5, left=5, bottom=5, right=5, bg_color=[240, 240, 240]))

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

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
            self.window.show_view(self.window.views["game"])

    def on_click_quiz(self, event):
        """
        Weiter
        :param event:
        """

        v = Question(self.room, self.book)
        v.setup()
        self.window.show_view(v)

    def on_resize(self, width, height):
        """
        Wird von arcade aufgerufen, wenn die Fenstergrösse ändert.

        :param width: neue Breite
        :param height: neue Höhe
        """
        self.setup()
