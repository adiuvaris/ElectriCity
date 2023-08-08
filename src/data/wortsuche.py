import random
import string
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.task import Task
from src.ui.attributed_text import AttributedText


class Wort:
    """
    Klasse für ein Wort in der Wortsuche
    """

    def __init__(self, wort):
        self.wort = wort
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.dx = 0
        self.dy = 0
        self.found = False
        self.start_found = False
        self.end_found = False


class Wortsuche(Task):
    """
    Klasse für eine Wortsuche-Aufgabe
    """

    def __init__(self, aufgabe: dict):
        super().__init__(aufgabe)

        self.input_answer = None
        self.manager = None
        self.correct = False
        self.worte = []

        self.buttons = {}
        self.grid = []
        self.grid_fragen = []

        self.such_worte = {}
        self.cur_such_wort = None
        self.first_button = None
        self.first_button_text = ""
        self.aufgabe_text = None

        self.dauer = 0.0

        if "Worte" in aufgabe:
            self.worte = aufgabe["Worte"]

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):

        super().create_ui(ui_manager, callback)

        aufgabe_text = self.aufgabe.copy()
        aufgabe_text.extend(self.worte)
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

        self.manager.add(self.aufgabe_text)

        self.grid = [[random.choice(string.ascii_uppercase) for i in range(0, 20)] for j in range(0, 20)]

        already_taken = []

        for word in self.worte:
            stop = 0
            ok = self.put_word(word, already_taken)
            while not ok and stop < 100:
                ok = self.put_word(word, already_taken)
                stop += 1
            else:
                pass

        w = 30
        h = 30

        style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}

        for i in range(20):
            for j in range(20):
                x = 560 + i * w
                y = 30 + j * h
                ib = arcade.gui.UIFlatButton(x=gd.scale(x), y=gd.scale(y), width=gd.scale(w), height=gd.scale(h),
                                             text=self.grid[i][j], style=style)

                ib.on_click = self.on_wortsuche_click
                self.manager.add(ib)

                self.buttons[(i, j)] = ib

    def on_wortsuche_click(self, event):

        for k in self.buttons:
            b = self.buttons[k]
            if b == event.source and b.text != "":
                i = k[0]
                j = k[1]

                if self.first_button is None:
                    self.first_button = b
                    self.first_button_text = b.text
                    b.text = ""

                    self.cur_such_wort = None

                    for wk in self.such_worte:
                        such_wort = self.such_worte[wk]
                        if such_wort.start_x == i and such_wort.start_y == j:
                            such_wort.start_found = True
                            self.cur_such_wort = such_wort

                        elif such_wort.end_x == i and such_wort.end_y == j:
                            such_wort.end_found = True
                            self.cur_such_wort = such_wort

                else:
                    if self.cur_such_wort is None:
                        arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)
                        self.first_button.text = self.first_button_text
                        self.first_button = None
                    else:
                        such_wort = self.cur_such_wort

                        if such_wort.start_x == i and such_wort.start_y == j:
                            such_wort.start_found = True

                        elif such_wort.end_x == i and such_wort.end_y == j:
                            such_wort.end_found = True

                        if such_wort.start_found and such_wort.end_found:
                            arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)
                            such_wort.found = True
                            x = such_wort.start_x
                            y = such_wort.start_y

                            for i in range(0, len(such_wort.wort)):
                                x_pos = x + such_wort.dx * i
                                y_pos = y + such_wort.dy * i
                                self.buttons[(x_pos, y_pos)].text = ""

                            self.worte.remove(such_wort.wort)
                            self.first_button = None
                            self.cur_such_wort = None

                            self.manager.remove(self.aufgabe_text)

                            if len(self.worte) == 0:
                                self.correct = True

                                aufgabe_text = self.aufgabe.copy()
                                aufgabe_text.append("Mit der Esc-Taste geht es zum Spiel zurück.")
                                self.aufgabe_text = AttributedText(
                                    x=gd.scale(20), y=gd.scale(20),
                                    width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                            else:
                                aufgabe_text = self.aufgabe.copy()
                                aufgabe_text.extend(self.worte)
                                self.aufgabe_text = AttributedText(
                                    x=gd.scale(20), y=gd.scale(20),
                                    width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                            self.manager.add(self.aufgabe_text)

                        else:
                            arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)
                            self.first_button.text = self.first_button_text
                            self.first_button = None
                            self.cur_such_wort = None

                break

        self.manager.trigger_render()

    def put_word(self, word, already_taken):

        width = 20
        height = 20

        rand_word = random.choice([word, word[::-1]])
        d = random.choice([[1, 0], [0, 1], [1, 1]])

        x_size = width if d[0] == 0 else width - len(rand_word)
        y_size = width if d[1] == 0 else height - len(rand_word)
        x = random.randrange(0, x_size)
        y = random.randrange(0, y_size)

        such_wort = Wort(word)
        such_wort.start_x = x
        such_wort.start_y = y
        such_wort.dx = d[0]
        such_wort.dy = d[1]

        problem = False
        for i in range(0, len(rand_word)):
            x_pos = x + d[0] * i
            y_pos = y + d[1] * i
            check = (x_pos, y_pos)
            if check in already_taken:
                problem = True
            else:
                already_taken.append(check)

        if not problem:
            for i in range(0, len(rand_word)):
                x_pos = x + d[0] * i
                y_pos = y + d[1] * i
                self.grid[x_pos][y_pos] = rand_word[i]
                such_wort.end_x = x_pos
                such_wort.end_y = y_pos

            self.such_worte[word] = such_wort
            return True

        return False
