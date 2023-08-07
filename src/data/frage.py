import random
import os
import string
import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.base.term import Term
from src.data.task import Task
from src.ui.attributed_text import AttributedText
from src.ui.message_box import MessageBox


class Frage(Task):
    def __init__(self, aufgabe: dict):
        super().__init__(aufgabe)

        self.answers = {}
        self.correct_answer = ""
        self.type = ""
        self.digits = 0
        self.variables = {}
        self.cur_variables = {}

        if "Typ" in aufgabe:
            self.type = aufgabe["Typ"]
        if "Richtig" in aufgabe:
            self.correct_answer = aufgabe["Richtig"]
        if "Nachkommastellen" in aufgabe:
            self.digits = aufgabe["Nachkommastellen"]
        if "Antworten" in aufgabe:
            self.answers = aufgabe["Antworten"]
        if "Variablen" in aufgabe:
            self.variables = aufgabe["Variablen"]

        # Aktuelle Variablen mit zufälligem Wert aus der Liste der möglichen Werte füllen
        self.cur_variables.clear()
        for k, werte in self.variables.items():
            random.shuffle(werte)

            # Weil die Werte nun zufällig angeordnet sind, kann man einfach der erste nehmen
            # es wird ein zufälliger Wert aus den gegebenen Werten sein
            self.cur_variables[k] = werte[0]

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):

        super().create_ui(ui_manager, callback)

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

        super().on_key_press(key, modifiers)

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
            if round(val, self.digits) == round(answer, self.digits):
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

    def on_update(self, delta_time: float, window: arcade.Window):
        pass
