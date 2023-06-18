import arcade
import arcade.gui

import src.const as const


def create_image_button(number, label, callback):
    x = 30
    y = 110

    if number == 1:
        x = 500
    elif number == 2:
        y = 30
    elif number == 3:
        x = 500
        y = 30

    w = 430
    h = 50

    image_button = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=label)
    image_button.on_click = callback

    return image_button


def create_answer_button(number, label, callback):
    x = 990
    y = 110

    if number == 1:
        x = 1460
    elif number == 2:
        y = 30
    elif number == 3:
        x = 1460
        y = 30

    w = 430
    h = 50

    answer_button = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=label)
    answer_button.on_click = callback

    return answer_button


