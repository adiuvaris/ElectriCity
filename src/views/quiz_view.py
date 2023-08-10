import json
import random

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.ui.quiz import Quiz
from src.ui.frage import Frage
from src.ui.memory import Memory
from src.ui.puzzle import Puzzle
from src.ui.wortsuche import Wortsuche


class QuizView(arcade.View):
    """
    Klasse für die View mit Quiz-Aufgaben für den Zutritt zu einem Raum
    """

    def __init__(self, room_nr):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Member definieren
        self.room_nr = room_nr
        self.quiz = None
        self.tasks = []

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

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
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        """

        # Zuerst mal Elemente löschen
        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)
        self.manager.clear()

        # Titeltext oben in der Mitte
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


def create_task(aufgabe: dict):
    """
    Aufgab erstellen je nach Art der Aufgabe
    """

    if "Art" in aufgabe:
        art = aufgabe["Art"]

        if art == "Frage":
            frage = Frage(aufgabe)
            return frage

        if art == "Memory":
            memory = Memory(aufgabe)
            return memory

        if art == "Puzzle":
            puzzle = Puzzle(aufgabe)
            return puzzle

        if art == "Wortsuche":
            wortsuche = Wortsuche(aufgabe)
            return wortsuche
