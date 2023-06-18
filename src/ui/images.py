import arcade
import arcade.gui

import src.const as const


def create_image_sprite(datei):
    x = 30
    y = 220
    w = 1140
    h = 580

    bs = arcade.Sprite(filename=f"res/data/{datei}")

    h = bs.height
    w = bs.width

    image_sprite = arcade.gui.UISpriteWidget(x=x, y=y, width=w, height=h, sprite=bs)

    return image_sprite
