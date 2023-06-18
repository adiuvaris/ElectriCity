import arcade
import arcade.gui
import json

from src.views.image import Image

from src.ui.labels import create_title_label
from src.ui.texts import create_theory_text
from src.ui.buttons import create_image_button
from src.ui.labels import create_answer_label
from src.ui.texts import create_question_text
from src.ui.buttons import create_answer_button
from src.ui.inputs import create_answer_input


class Book(arcade.View):
    """
    Klasse für die View mit Theorie oder Aufgabe
    """

    def __init__(self, room_nr, book_nr):
        """
        Konstruktor
        """

        super().__init__()

        self.room_nr = room_nr
        self.book_nr = book_nr
        self.data = None

        self.input_text: arcade.gui.UIInputText = arcade.gui.UIInputText()

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
        with open(f"res/data/book_{self.room_nr}_{self.book_nr}.json", "r", encoding="'utf-8") as ifile:
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
                    bild_button = create_image_button(i, bild["Titel"], self.on_click_bild)
                    self.manager.add(bild_button)

            # Aufgaben-Text Element erzeugen
            if "Aufgabe" in self.data:
                text = "\n".join(self.data["Aufgabe"])
                question_text = create_question_text(text)
                self.manager.add(question_text)

            if "Typ" in self.data:
                if self.data["Typ"] == "Multi":
                    if "Antworten" in self.data:
                        antworten = self.data["Antworten"]
                        if "A" in antworten:
                            antwort_button = create_answer_button(0, antworten["A"], self.on_click_a)
                            self.manager.add(antwort_button)
                        if "B" in antworten:
                            antwort_button = create_answer_button(1, antworten["B"], self.on_click_b)
                            self.manager.add(antwort_button)
                        if "C" in antworten:
                            antwort_button = create_answer_button(2, antworten["C"], self.on_click_c)
                            self.manager.add(antwort_button)
                        if "D" in antworten:
                            antwort_button = create_answer_button(3, antworten["D"], self.on_click_d)
                            self.manager.add(antwort_button)

                elif self.data["Typ"] == "Zahl":

                    label = create_answer_label("Antwort:")
                    self.manager.add(label)

                    self.input_text = create_answer_input()
                    answer_input = arcade.gui.UIBorder(self.input_text)
                    self.manager.add(answer_input)

                elif self.data["Typ"] == "Text":
                    pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

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

        if key == arcade.key.ENTER:

            # Eingabe in Zahl umwandeln
            eingabe = float(self.input_text.text.strip())

            if eingabe == 45.0:
                self.show_message_box("Das ist richtig.")
            else:
                self.show_message_box("Das ist leider falsch.")

    def on_click_bild(self, event):
        if event.source.text == "Bild 1":
            v = Image(self.data["Bilder"][0], self)
            v.setup()
            self.window.show_view(v)

        elif event.source.text == "Bild 2":
            v = Image(self.data["Bilder"][1], self)
            v.setup()
            self.window.show_view(v)

    def on_click_a(self, event):
        """
        Antwort A
        :param event:
        """
        self.show_message_box("Das ist richtig.")

    def on_click_b(self, event):
        """
        Antwort B
        :param event:
        """
        pass

    def on_click_c(self, event):
        """
        Antwort C
        :param event:
        """
        pass

    def on_click_d(self, event):
        """
        Antwort D
        :param event:
        """
        pass

    def show_message_box(self, text):
        message_box = arcade.gui.UIMessageBox(
            width=500,
            height=300,
            message_text=text,
            callback=self.on_message_box_close,
            buttons=["Ok"]
        )

        self.manager.add(message_box)

    def on_message_box_close(self, button_text):
        self.window.show_view(self.window.views["game"])
