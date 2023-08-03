import random
import string
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.base.term import Term
from src.ui.attributed_text import AttributedText
from src.ui.message_box import MessageBox


class Wort:
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


class Task:
    def __init__(self):
        self.art = ""
        self.aufgabe = []
        self.answers = {}
        self.correct_answer = ""
        self.type = "Zahl"
        self.digits = 0
        self.variables = {}
        self.cur_variables = {}
        self.input_answer = None
        self.manager = None
        self.correct = False
        self.worte = []
        self.paare = []

        self.buttons = {}
        self.grid = []

        self.such_worte = {}
        self.cur_such_wort = None
        self.first_button = None
        self.first_button_text = ""
        self.aufgabe_text = None

        self.callback = None

        self.lose_sound = arcade.load_sound(":sounds:lose.wav")
        self.ok_sound = arcade.load_sound(":sounds:ok.wav")
        self.msg_active = False

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):

        self.manager = ui_manager
        self.callback = callback

        # Aktuelle Variablen mit zufälligem Wert aus der Liste der möglichen Werte füllen
        self.cur_variables.clear()
        for k, werte in self.variables.items():
            random.shuffle(werte)

            # Weil die Werte nun zufällig angeordnet sind, kann man einfach der erste nehmen
            # es wird ein zufälliger Wert aus den gegebenen Werten sein
            self.cur_variables[k] = werte[0]

        # Rahmen für den Aufgabenblock
        widget = arcade.gui.UIWidget(x=gd.scale(450), y=gd.scale(10), width=gd.scale(820), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        self.manager.add(border)

        if self.art == "Frage":
            self.create_frage_ui()

        if self.art == "Memory":
            self.create_memory_ui()

        if self.art == "Wortsuche":
            self.create_wortsuche_ui()

    def create_frage_ui(self):

        # Aufgaben-Text
        text = AttributedText(x=gd.scale(460), y=gd.scale(120),
                              width=gd.scale(800), height=gd.scale(520),
                              text=self.aufgabe, variables=self.cur_variables)

        self.manager.add(text)

        if self.type == "Multi":

            # Antworten zufällig anordnen
            items = list(self.answers.items())
            random.shuffle(items)

            i = 0
            for k, v in items:

                x = gd.scale(460)
                y = gd.scale(70)

                if i == 1:
                    x = gd.scale(870)
                elif i == 2:
                    y = gd.scale(20)
                elif i == 3:
                    x = gd.scale(870)
                    y = gd.scale(20)

                w = gd.scale(390)
                h = gd.scale(30)

                style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
                ib = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=v, style=style)
                ib.on_click = self.on_frage_click

                self.manager.add(ib)

                i = i + 1

        elif self.type == "Zahl":

            x = gd.scale(460)
            y = gd.scale(70)
            w = gd.scale(390)
            h = gd.scale(30)
            fs = gd.scale(const.FONT_SIZE_H2)

            label = arcade.gui.UILabel(x=x,
                                       y=y,
                                       width=w,
                                       height=h,
                                       text="Antwort:",
                                       text_color=[0, 0, 0],
                                       bold=True,
                                       align="right",
                                       font_size=fs,
                                       multiline=False)

            self.manager.add(label)

            x = gd.scale(870)
            y = gd.scale(70)
            w = gd.scale(390)
            h = gd.scale(30)
            fs = gd.scale(const.FONT_SIZE_H2)

            self.input_answer = arcade.gui.UIInputText(x=x, y=y, width=w, height=h, font_size=fs, text="")
            self.manager.add(self.input_answer.with_border())

            # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
            if self.input_answer is not None:
                event = arcade.gui.UIMousePressEvent(
                    x=self.input_answer.x + 1, y=self.input_answer.y + 1, button=0, modifiers=0, source=self)

                self.input_answer.on_event(event)

        elif self.type == "Text":
            x = gd.scale(460)
            y = gd.scale(70)
            w = gd.scale(390)
            h = gd.scale(30)
            fs = gd.scale(const.FONT_SIZE_H2)

            label = arcade.gui.UILabel(x=x,
                                       y=y,
                                       width=w,
                                       height=h,
                                       text="Antwort:",
                                       text_color=[0, 0, 0],
                                       bold=True,
                                       align="right",
                                       font_size=fs,
                                       multiline=False)

            self.manager.add(label)

            x = gd.scale(870)
            y = gd.scale(70)
            w = gd.scale(390)
            h = gd.scale(30)
            fs = gd.scale(const.FONT_SIZE_H2)

            self.input_answer = arcade.gui.UIInputText(x=x, y=y, width=w, height=h, font_size=fs, text="")
            self.manager.add(self.input_answer.with_border())

            # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
            if self.input_answer is not None:
                event = arcade.gui.UIMousePressEvent(
                    x=self.input_answer.x + 1, y=self.input_answer.y + 1, button=0, modifiers=0, source=self)

                self.input_answer.on_event(event)

    def on_frage_click(self, event):

        if self.msg_active:
            return

        msg = "Das ist leider falsch"
        sound = self.lose_sound

        for k, v in self.answers.items():
            if event.source.text == v:
                if k == self.correct_answer:
                    msg = "Das ist korrekt"
                    sound = self.ok_sound
                    self.correct = True
                    break

        arcade.play_sound(sound, volume=gd.get_volume() / 100.0)

        self.msg_active = True
        msg_box = MessageBox(msg=msg, callback=self.on_ok)
        self.manager.add(msg_box)

    def on_key_press(self, key, modifiers):
        if self.msg_active:
            return

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.callback()

        # Prüfen, ob eine Antwort eingetippt wurde
        if key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:
            if self.input_answer is not None:
                # Antwort prüfen
                eingabe = self.input_answer.text.strip()
                eingabe.replace('\n', '')
                if len(eingabe) > 0:
                    self.check_answer(eingabe)
                else:
                    self.input_answer.text = eingabe

    def check_answer(self, answer):
        if self.msg_active:
            return

        msg = "Das ist leider falsch"
        sound = self.lose_sound

        if self.type == "Zahl":

            # Bei einer Zahl muss die Antwort anhand der Formel berechnet werden
            answer = float(answer)
            term = Term()
            term.variables = self.cur_variables
            val = term.calc(self.correct_answer)

            # Stimmt die Antwort?
            if val == answer:
                msg = "Das ist korrekt"
                sound = self.ok_sound
                self.correct = True

        if self.type == "Text":

            # Stimmt die Antwort (gross/klein ignorieren)?
            if answer.lower() == self.correct_answer.lower():
                msg = "Das ist korrekt"
                sound = self.ok_sound
                self.correct = True

        arcade.play_sound(sound, volume=gd.get_volume() / 100.0)

        if self.input_answer is not None:
            event = arcade.gui.UIMousePressEvent(
                x=self.input_answer.x - 1, y=self.input_answer.y - 1, button=0, modifiers=0, source=self)

            self.input_answer.on_event(event)

        self.msg_active = True
        msg_box = MessageBox(msg=msg, callback=self.on_ok)
        self.manager.add(msg_box)

    def on_ok(self, event):
        self.msg_active = False
        if self.correct:
            self.callback()

    def create_memory_ui(self):

        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=self.aufgabe)

        self.manager.add(self.aufgabe_text)

        w = 200
        h = 200

        mypath = gd.get_abs_path("res/data")
        avatar_path = mypath + "/back.png"
        te = arcade.load_texture(avatar_path, x=0, y=0, width=200, height=200)

        self.grid = [[0 for i in range(0, 4)] for j in range(0, 3)]

        for i in range(4):
            for j in range(3):
                x = 460 + i * w
                y = 30 + j * h
                ib = arcade.gui.UITextureButton(x=gd.scale(x), y=gd.scale(y), width=gd.scale(w), height=gd.scale(h), texture=te)
                ib.on_click = self.on_memory_click
                self.manager.add(ib)

                self.buttons[(i, j)] = ib

    def on_memory_click(self, event):
        for k in self.buttons:
            b = self.buttons[k]
            if b == event.source:
                mypath = gd.get_abs_path("res/data")
                # te = arcade.load_texture(avatar_path, x=0, y=0, width=200, height=200)
                # b.texture = te
                self.manager.trigger_render()

    def create_wortsuche_ui(self):

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

        for i in range(20):
            for j in range(20):
                x = 560 + i * w
                y = 30 + j * h
                ib = arcade.gui.UIFlatButton(x=gd.scale(x), y=gd.scale(y), width=gd.scale(w), height=gd.scale(h), text=self.grid[i][j])
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
                        self.first_button.text = self.first_button_text
                        self.first_button = None
                    else:
                        such_wort = self.cur_such_wort

                        if such_wort.start_x == i and such_wort.start_y == j:
                            such_wort.start_found = True

                        elif such_wort.end_x == i and such_wort.end_y == j:
                            such_wort.end_found = True

                        if such_wort.start_found and such_wort.end_found:
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

                            aufgabe_text = self.aufgabe.copy()
                            aufgabe_text.extend(self.worte)
                            self.manager.remove(self.aufgabe_text)
                            self.aufgabe_text = AttributedText(
                                x=gd.scale(20), y=gd.scale(20),
                                width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)

                            self.manager.add(self.aufgabe_text)

                            if len(self.worte) == 0:
                                self.correct = True
                                self.callback()

                        else:
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
            print(word, " inserted at ", [such_wort.start_x, such_wort.start_y], [such_wort.end_x, such_wort.end_y])
            return True

        return False
