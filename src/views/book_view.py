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

    def on_answer_click(self, event):

        if self.msg_active:
            return

        task = self.tasks[self.cur_task]

        msg = "Das ist leider falsch"
        sound = self.lose_sound

        for k, v in task.answers.items():
            if event.source.text == v:
                if k == task.correct_answer:
                    msg = "Das ist korrekt"
                    sound = self.ok_sound
                    gd.set_task(self.room_nr, self.book_nr, self.cur_task)
                    self.cur_task = self.cur_task + 1
                    self.correct = True
                    break

        arcade.play_sound(sound, volume=gd.get_volume() / 100.0)

        self.msg_active = True
        msg_box = MessageBox(msg=msg, callback=self.on_ok)
        self.manager.add(msg_box)

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        if self.msg_active:
            return

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)

        # Prüfen, ob eine Antwort eingetippt wurde
        if key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:
            task = self.tasks[self.cur_task]
            if task.input_answer is not None:
                # Antwort prüfen
                eingabe = task.input_answer.text.strip()
                self.check_answer(eingabe)

    def check_answer(self, answer):

        if self.msg_active:
            return

        msg = "Das ist leider falsch"
        sound = self.lose_sound
        task = self.tasks[self.cur_task]

        if task.type == "Zahl":

            # Bei einer Zahl muss die Antwort anhand der Formel berechnet werden
            answer = float(answer)
            term = Term()
            term.variables = task.cur_variables
            val = term.calc(task.correct_answer)

            # Stimmt die Antwort?
            if val == answer:
                msg = "Das ist korrekt"
                sound = self.ok_sound
                self.correct = True
                gd.set_task(self.room_nr, self.book_nr, self.cur_task)
                self.cur_task = self.cur_task + 1

        if task.type == "Text":

            # Stimmt die Antwort (gross/klein ignorieren)?
            if answer.lower() == task.correct_answer.lower():
                msg = "Das ist korrekt"
                sound = self.ok_sound
                self.correct = True
                gd.set_task(self.room_nr, self.book_nr, self.cur_task)
                self.cur_task = self.cur_task + 1

        arcade.play_sound(sound, volume=gd.get_volume() / 100.0)

        if task.input_answer is not None:
            event = arcade.gui.UIMousePressEvent(
                x=task.input_answer.x - 1, y=task.input_answer.y - 1, button=0, modifiers=0, source=self)

            task.input_answer.on_event(event)

        self.msg_active = True
        msg_box = MessageBox(msg=msg, callback=self.on_ok)
        self.manager.add(msg_box)

    def on_ok(self):
        self.msg_active = False
        if self.correct:
            self.create_ui()

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
            self.tasks[self.cur_task].create_ui(self.manager, self.on_answer_click)
        else:
            self.window.show_view(self.window.game_view)

        self.manager.trigger_render()
