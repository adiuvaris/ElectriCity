import random
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.ui.attributed_text import AttributedText


class Task:
    def __init__(self):
        self.question = ""
        self.answers = {}
        self.correct_answer = 0
        self.type = "Zahl"
        self.digits = 0
        self.variables = {}
        self.cur_variables = {}
        self.input_answer = None
        self.manager = None
        self.correct = False

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):

        self.manager = ui_manager

        # Aktuelle Variablen mit zufälligem Wert aus der Lite der möglichen Werte füllen
        self.cur_variables.clear()
        for k, werte in self.variables.items():
            random.shuffle(werte)

            # Weil die Werte nun zufällig angeordnet sind, kann man einfach der erste nehmen
            # es wird ein zufälliger Wert aus den gegebenen Werten sein
            self.cur_variables[k] = werte[0]

        # Rahmen für den Aufgabenblock
        widget = arcade.gui.UIWidget(x=gd.scale(650), y=gd.scale(10), width=gd.scale(620), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        ui_manager.add(border)

        # Aufgaben-Text
        text = AttributedText(x=gd.scale(660), y=gd.scale(120),
                              width=gd.scale(600), height=gd.scale(520),
                              text=self.question, variables=self.cur_variables)

        ui_manager.add(text)

        if self.type == "Multi":

            # Antworten zufällig anordnen
            items = list(self.answers.items())
            random.shuffle(items)

            i = 0
            for k, v in items:

                x = gd.scale(660)
                y = gd.scale(70)

                if i == 1:
                    x = gd.scale(970)
                elif i == 2:
                    y = gd.scale(20)
                elif i == 3:
                    x = gd.scale(970)
                    y = gd.scale(20)

                w = gd.scale(290)
                h = gd.scale(30)

                style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
                ib = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=v, style=style)
                ib.on_click = callback

                ui_manager.add(ib)

                i = i + 1

        elif self.type == "Zahl":

            x = gd.scale(660)
            y = gd.scale(70)
            w = gd.scale(290)
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

            ui_manager.add(label)

            x = gd.scale(970)
            y = gd.scale(70)
            w = gd.scale(290)
            h = gd.scale(30)
            fs = gd.scale(const.FONT_SIZE_H2)

            self.input_answer = arcade.gui.UIInputText(x=x, y=y, width=w, height=h, font_size=fs, text="")
            ui_manager.add(self.input_answer.with_border())

            # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
            if self.input_answer is not None:
                event = arcade.gui.UIMousePressEvent(
                    x=self.input_answer.x + 1, y=self.input_answer.y + 1, button=0, modifiers=0, source=self)

                self.input_answer.on_event(event)

        elif self.type == "Text":
            x = gd.scale(660)
            y = gd.scale(70)
            w = gd.scale(290)
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

            ui_manager.add(label)

            x = gd.scale(970)
            y = gd.scale(70)
            w = gd.scale(290)
            h = gd.scale(30)
            fs = gd.scale(const.FONT_SIZE_H2)

            self.input_answer = arcade.gui.UIInputText(x=x, y=y, width=w, height=h, font_size=fs, text="")
            ui_manager.add(self.input_answer.with_border())

            # Eingabefeld aktivieren - so tun, als ob in das Feld geklickt wurde
            if self.input_answer is not None:
                event = arcade.gui.UIMousePressEvent(
                    x=self.input_answer.x + 1, y=self.input_answer.y + 1, button=0, modifiers=0, source=self)

                self.input_answer.on_event(event)

