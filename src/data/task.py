import arcade.gui

import src.const as const
from src.data.game_data import gd
from src.ui.attributed_text import AttributedText


class Task:
    def __init__(self):
        self.question = ""
        self.answers = {}
        self.correct_answer = 0
        self.type = "Zahl"
        self.digits = 0
        self.variables = {}

    def create_ui(self, ui_manager: arcade.gui.UIManager):

        widget = arcade.gui.UIWidget(x=gd.scale(650), y=gd.scale(10), width=gd.scale(620), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        ui_manager.add(border)

        text = AttributedText(x=gd.scale(660), y=gd.scale(120),
                              width=gd.scale(600), height=gd.scale(520), text=self.question)

        ui_manager.add(text)

        if self.type == "Multi":

            i = 0
            for k, v in self.answers.items():

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
                ib.on_click = self.on_answer_click

                ui_manager.add(ib)

                i = i + 1

    def on_answer_click(self, event):
        for k, v in self.answers.items():

            if event.source.text == v:
                if k == self.correct_answer:
                    pass

                pass
