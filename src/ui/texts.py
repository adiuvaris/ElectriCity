import arcade
import arcade.gui

import src.const as const


def create_theory_text(text):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 30 * fx
    y = 110 * fy
    w = 910 * fx
    h = 580 * fy
    fs = 14 * fy
    text = arcade.gui.UITextArea(x=x,
                                 y=y,
                                 width=w,
                                 height=h,
                                 text=text,
                                 text_color=[0, 0, 0],
                                 font_size=fs,
                                 multiline=True)

    theory_text = text.with_space_around(top=5, left=5, bottom=5, right=5, bg_color=[240, 240, 240])

    return theory_text


def create_question_text(text):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 30 * fx
    y = 190 * fy
    w = 1140 * fx
    h = 500 * fy
    fs = 14 * fy
    text = arcade.gui.UITextArea(x=x,
                                 y=y,
                                 width=w,
                                 height=h,
                                 text=text,
                                 text_color=[0, 0, 0],
                                 font_size=fs,
                                 multiline=True)

    theory_text = text.with_space_around(top=5, left=5, bottom=5, right=5, bg_color=[240, 240, 240])

    return theory_text
