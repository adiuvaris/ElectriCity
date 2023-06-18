import arcade
import arcade.gui

import src.const as const


def create_theory_text(text):
    x = 30
    y = 190
    w = 900
    h = 780
    fs = 16
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
    x = 990
    y = 190
    w = 900
    h = 780
    fs = 16
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
