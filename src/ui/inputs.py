import arcade
import arcade.gui

import src.const as const


def create_answer_input():
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 240 * fx
    y = 110 * fy
    w = 200 * fx
    h = 30 * fy
    fs = 20 * fy

    input_text = arcade.gui.UIInputText(x=x, y=y, width=w, height=h, font_size=fs, text="")

    return input_text
