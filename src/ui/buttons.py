import arcade
import arcade.gui

import src.const as const


def create_back_button(label, callback):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 30 * fx
    y = 30 * fy
    w = 200 * fx
    h = 50 * fy

    back_button = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=label)
    back_button.on_click = callback

    return back_button


def create_next_button(label, callback):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 970 * fx
    y = 30 * fy
    w = 200 * fx
    h = 50 * fy

    next_button = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=label)
    next_button.on_click = callback

    return next_button


def create_answer_button(number, label, callback):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 30 * fx
    y = 110 * fy

    if number == 2:
        x = 500 * fx
        y = 110 * fy
    elif number == 3:
        x = 30 * fx
        y = 30 * fy
    elif number == 4:
        x = 500 * fx
        y = 30 * fy

    w = 450 * fx
    h = 50 * fy

    answer_button = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=label)
    answer_button.on_click = callback

    return answer_button


def create_image_button(number, callback):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 970 * fx
    y = 640 * fy

    if number == 1:
        y = 570 * fy
    elif number == 2:
        y = 500 * fy
    elif number == 3:
        y = 430 * fy
    elif number == 4:
        y = 360 * fy

    w = 200 * fx
    h = 50 * fy

    label = f"Bild {number+1}"

    image_button = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=label)
    image_button.on_click = callback

    return image_button
