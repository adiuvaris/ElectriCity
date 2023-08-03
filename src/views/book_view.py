import arcade
import arcade.gui
import json

import src.const as const
from src.data.game import gd

from src.base.term import Term

from src.ui.message_box import MessageBox

from src.data.theory import Theory
from src.data.image import Image
from src.data.task import Task

from src.views.image_view import ImageView


class BookView(arcade.View):
    """
    Klasse für die View mit Theorie oder Aufgabe
    """

    def __init__(self, room_nr, book_nr):
        """
        Konstruktor
        """

        super().__init__()

        self.lose_sound = arcade.load_sound(":sounds:lose.wav")
        self.ok_sound = arcade.load_sound(":sounds:ok.wav")

        self.room_nr = room_nr
        self.book_nr = book_nr

        self.title = ""
        self.theory = None
        self.tasks = []
        self.cur_task = 0
        self.correct = False
        self.msg_active = False

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

    def on_image_click(self, event):
        for img in self.theory.images:
            img: Image = img

            if event.source.text == img.title:
                image_view = ImageView(img, self)
                self.window.show_view(image_view)

    def on_key_press(self, key, modifiers):
        task = self.tasks[self.cur_task]
        task.on_key_press(key, modifiers)

    def read_book(self):

        # JSON-File für Buch einlesen
        mypath = gd.get_abs_path("res/data")
        with open(f"{mypath}/book_{self.room_nr}_{self.book_nr}.json", "r", encoding="'utf-8") as ifile:
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
                    if "Art" in aufgabe:
                        task.art = aufgabe["Art"]
                    if "Aufgabe" in aufgabe:
                        task.aufgabe = aufgabe["Aufgabe"]
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

            gd.init_book(self.room_nr, self.book_nr, len(self.tasks))

    def create_ui(self):

        self.correct = False

        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)

        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text=self.title,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)

        self.manager.add(titel.with_border())

        self.theory.create_ui(self.manager, callback=self.on_image_click)

        if self.cur_task < len(self.tasks):
            self.tasks[self.cur_task].create_ui(self.manager, self.on_end_task)
        else:
            self.window.show_view(self.window.game_view)

        self.manager.trigger_render()

    def on_end_task(self):
        if self.tasks[self.cur_task].correct:
            gd.set_task(self.room_nr, self.book_nr, self.cur_task)
            self.cur_task = self.cur_task + 1
            self.create_ui()

