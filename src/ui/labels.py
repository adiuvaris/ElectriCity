import arcade
import arcade.gui

import src.const as const


def create_title_label(text):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 30 * fx
    y = 740 * fy
    w = 1140 * fx
    h = 30 * fy
    fs = 20 * fy

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
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 30 * fx
    y = 110 * fy
    w = 300 * fx
    h = 30 * fy
    fs = 20 * fy

    label = arcade.gui.UILabel(x=x,
                               y=y,
                               width=w,
                               height=h,
                               text=text,
                               text_color=[0, 0, 0],
                               bold=True,
                               align="left",
                               font_size=fs,
                               multiline=False)

    return label
