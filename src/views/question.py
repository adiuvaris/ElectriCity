import arcade
import arcade.gui
import json

from src.ui.labels import create_title_label
from src.ui.labels import create_answer_label
from src.ui.texts import create_question_text
from src.ui.buttons import create_answer_button
from src.ui.inputs import create_answer_input


class Question(arcade.View):
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

        self.input_text: arcade.gui.UIInputText = arcade.gui.UIInputText()

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

    def setup(self):
        """
        View initialisieren.
        Es wird die Aufgabe für den Raum und das Buch angezeigt.
        """

        # Alle UI Elemente löschen
        self.manager.clear()

        # JSON-File für Aufgabe einlesen
        with open(f"res/data/q_{self.room}_{self.book}.json", "r", encoding="'utf-8") as ifile:
            data = json.load(ifile)

            # Titel-Element erzeugen
            if "Titel" in data:
                title_label = create_title_label(data["Titel"])
                self.manager.add(title_label)

            # Aufgaben-Text Element erzeugen
            if "Aufgabe" in data:
                text = "\n".join(data["Aufgabe"])
                question_text = create_question_text(text)
                self.manager.add(question_text)

            if "Typ" in data:
                if data["Typ"] == "Multi":
                    if "Antworten" in data:
                        antworten = data["Antworten"]
                        if "A" in antworten:
                            antwort_button = create_answer_button(1, antworten["A"], self.on_click_a)
                            self.manager.add(antwort_button)
                        if "B" in antworten:
                            antwort_button = create_answer_button(2, antworten["B"], self.on_click_b)
                            self.manager.add(antwort_button)
                        if "C" in antworten:
                            antwort_button = create_answer_button(3, antworten["C"], self.on_click_c)
                            self.manager.add(antwort_button)
                        if "D" in antworten:
                            antwort_button = create_answer_button(4, antworten["D"], self.on_click_d)
                            self.manager.add(antwort_button)

                elif data["Typ"] == "Zahl":

                    label = create_answer_label("Antwort:")
                    self.manager.add(label)

                    self.input_text = create_answer_input()
                    answer_input = arcade.gui.UIBorder(self.input_text)
                    self.manager.add(answer_input)

                elif data["Typ"] == "Text":
                    pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
        if self.input_text is not None:
            event = arcade.gui.UIMousePressEvent(
                x=self.input_text.x + 1, y=self.input_text.y + 1, button=0, modifiers=0, source=self)
            self.input_text.on_event(event)

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

    def on_resize(self, width, height):
        """
        Wird von arcade aufgerufen, wenn die Fenstergrösse ändert.

        :param width: neue Breite
        :param height: neue Höhe
        """
        self.setup()

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
