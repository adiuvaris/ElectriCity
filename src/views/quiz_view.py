import random

import arcade
import arcade.gui
import json

import src.const as const
from src.data.game import gd

from src.base.term import Term

from src.ui.message_box import MessageBox

from src.data.quiz import Quiz
from src.data.image import Image
from src.data.task import Task
from src.data.task_createor import create_task

from src.views.image_view import ImageView


class QuizView(arcade.View):
    """
    Klasse für die View mit Quiz-Aufgaben für den Zutritt zu einem Raum
    """

    def __init__(self, room_nr):
        """
        Konstruktor
        """

        super().__init__()

        self.lose_sound = arcade.load_sound(":sounds:lose.wav")
        self.ok_sound = arcade.load_sound(":sounds:ok.wav")

        self.room_nr = room_nr

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        self.title = ""
        self.quiz = None
        self.tasks = []
        self.correct = False
        self.msg_active = False

        # Fragen einlesen (json) und zufällig eine auswählen
        self.read_quiz()
        self.cur_task = random.randint(0, len(self.tasks) - 1)

        # Die Frage darstellen
        self.create_ui()

    def setup(self):
        """
        View initialisieren.
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
        self.tasks[self.cur_task].on_key_press(key, modifiers)

    def read_quiz(self):

        # JSON-File mit Quiz-Fragen einlesen
        mypath = gd.get_abs_path("res/data")
        with open(f"{mypath}/quiz_{self.room_nr}.json", "r", encoding="'utf-8") as ifile:
            data = json.load(ifile)

            # Quiz-Text Element einlesen
            self.quiz = Quiz()
            if "Beschreibung" in data:
                self.quiz.text = data["Beschreibung"]

            # Aufgaben Element einlesen
            if "Aufgaben" in data:
                aufgaben = data["Aufgaben"]
                for aufgabe in aufgaben:
                    task = create_task(aufgabe)
                    self.tasks.append(task)

    def create_ui(self):

        self.correct = False

        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)

        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text="Quiz",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)

        self.manager.add(titel.with_border())

        self.quiz.create_ui(self.manager)

        if self.cur_task < len(self.tasks):
            self.tasks[self.cur_task].create_ui(self.manager, self.on_end_task)
        else:
            self.window.show_view(self.window.game_view)

        self.manager.trigger_render()

    def on_end_task(self):
        if self.tasks[self.cur_task].correct:
            gd.set_room_key(self.room_nr)
        self.window.show_view(self.window.game_view)
