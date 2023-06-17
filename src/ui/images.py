import arcade
import arcade.gui

import src.const as const


def create_image_sprite(datei):
    fx = arcade.get_window().width / const.SCREEN_WIDTH
    fy = arcade.get_window().height / const.SCREEN_HEIGHT

    x = 30 * fx
    y = 220 * fy
    w = 1140 * fx
    h = 580 * fy

    bs = arcade.Sprite(filename=f"res/data/{datei}")

    h = bs.height
    w = bs.width

    image_sprite = arcade.gui.UISpriteWidget(x=x, y=y, width=w, height=h, sprite=bs)

    return image_sprite
