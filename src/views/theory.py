import arcade
import arcade.gui
import json

from src.views.question import Question
from src.views.image import Image

from src.ui.labels import create_title_label
from src.ui.texts import create_theory_text
from src.ui.buttons import create_back_button
from src.ui.buttons import create_next_button
from src.ui.buttons import create_image_button


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
        self.data = None

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

    def setup(self):
        """
        View initialisieren.
        Es wird die Theorie für den Raum und das Buch angezeigt.
        """

        # Alle UI Elemente löschen
        self.manager.clear()

        # JSON-File für Theorie einlesen
        with open(f"res/data/t_{self.room}_{self.book}.json", "r", encoding="'utf-8") as ifile:
            self.data = json.load(ifile)

            # Titel-Element erzeugen
            if "Titel" in self.data:
                title_label = create_title_label(self.data["Titel"])
                self.manager.add(title_label)

            # Theorie-Text Element erzeugen
            if "Theorie" in self.data:
                text = "\n".join(self.data["Theorie"])
                theory_text = create_theory_text(text)
                self.manager.add(theory_text)

            if "Bilder" in self.data:
                bilder = self.data["Bilder"]
                for i, bild in enumerate(bilder):
                    bild_button = create_image_button(i, self.on_click_bild)
                    self.manager.add(bild_button)

            back_button = create_back_button("Zurück", self.on_click_back)
            self.manager.add(back_button)

            next_button = create_next_button("Weiter", self.on_click_next)
            self.manager.add(next_button)

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
            self.window.show_view(self.window.views["game"])

    def on_click_bild(self, event):
        if event.source.text == "Bild 1":
            v = Image(self.data["Bilder"][0], self)
            v.setup()
            self.window.show_view(v)

        elif event.source.text == "Bild 2":
            v = Image(self.data["Bilder"][1], self)
            v.setup()
            self.window.show_view(v)

    def on_click_back(self, event):
        self.window.show_view(self.window.views["game"])

    def on_click_next(self, event):
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
