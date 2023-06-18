import arcade
import arcade.gui

import src.const as const


def create_answer_input():
    x = 1460
    y = 110
    w = 430
    h = 50
    fs = 24

    input_text = arcade.gui.UIInputText(x=x, y=y, width=w, height=h, font_size=fs, text="")

    return input_text
