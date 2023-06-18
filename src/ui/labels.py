import arcade
import arcade.gui

import src.const as const


def create_title_label(text):

    x = 30
    y = 1000
    w = 1860
    h = 30
    fs = 24

    label = arcade.gui.UILabel(x=x,
                               y=y,
                               width=w,
                               height=h,
                               text=text,
                               text_color=[0, 0, 0],
                               bold=True,
                               align="center",
                               font_size=fs,
                               multiline=False)

    title_label = label.with_space_around(top=5, left=5, bottom=5, right=5, bg_color=[220, 220, 220])

    return title_label


def create_answer_label(text):
    x = 990
    y = 110
    w = 430
    h = 50
    fs = 24

    label = arcade.gui.UILabel(x=x,
                               y=y,
                               width=w,
                               height=h,
                               text=text,
                               text_color=[0, 0, 0],
                               bold=True,
                               align="right",
                               font_size=fs,
                               multiline=False)

    return label
