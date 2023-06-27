import arcade
import arcade.gui
import json

import src.const as const
from src.data.game import gd
from src.views.message_view import MessageView

from src.data.theory import Theory
from src.data.image import Image
from src.data.task import Task


class BookView(arcade.View):
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

        self.title = ""
        self.theory = None
        self.tasks = []
        self.cur_task = 0

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        # Buch einlesen (json)
        self.read_book()

        # Buch darstellen
        self.create_ui()

    def setup(self):
        """
        View initialisieren.
        Es wird die Theorie für den Raum und das Buch angezeigt.
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
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)

        self.tasks[self.cur_task].on_key_press(key, modifiers)

    def read_book(self):

        # JSON-File für Buch einlesen
        with open(f"res/data/book_{self.room_nr}_{self.book_nr}.json", "r", encoding="'utf-8") as ifile:
            data = json.load(ifile)

            # Titel-Element einlesen
            if "Titel" in data:
                self.title = data["Titel"]

            # Theorie-Text Element einlesen
            self.theory = Theory()
            if "Theorie" in data:
                self.theory.text = data["Theorie"]

            if "Bilder" in data:
                bilder = data["Bilder"]
                for bild in bilder:
                    image = Image()
                    if "Datei" in bild:
                        image.image_file = bild["Datei"]
                        if "Titel" in bild:
                            image.title = bild["Titel"]
                    if "Beschreibung" in bild:
                        image.description = bild["Beschreibung"]
                    self.theory.images.append(image)

            # Aufgaben Element einlesen
            if "Aufgaben" in data:
                aufgaben = data["Aufgaben"]
                for aufgabe in aufgaben:
                    task = Task()
                    if "Aufgabe" in aufgabe:
                        task.question = aufgabe["Aufgabe"]
                    if "Typ" in aufgabe:
                        task.type = aufgabe["Typ"]
                    if "Richtig" in aufgabe:
                        task.correct_answer = aufgabe["Richtig"]
                    if "Nachkommastellen" in aufgabe:
                        task.digits = aufgabe["Nachkommastellen"]
                    if "Antworten" in aufgabe:
                        task.answers = aufgabe["Antworten"]
                    if "Variablen" in aufgabe:
                        task.variables = aufgabe["Variablen"]
                    self.tasks.append(task)

    def create_ui(self):

        # Alle UI Elemente löschen
        self.manager = arcade.gui.UIManager()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text=self.title,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)

        self.manager.add(titel.with_border())

        self.theory.create_ui(self, self.manager)

        if self.cur_task < len(self.tasks):
            self.tasks[self.cur_task].create_ui(self, self.manager)
