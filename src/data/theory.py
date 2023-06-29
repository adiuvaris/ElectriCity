import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.image import Image
from src.views.image_view import ImageView
from src.ui.attributed_text import AttributedText


class Theory:
    def __init__(self):
        self.text = ""
        self.images = []
        self.parent = None

    def create_ui(self, parent: arcade.Window, ui_manager: arcade.gui.UIManager):

        self.parent = parent

        widget = arcade.gui.UIWidget(x=gd.scale(10), y=gd.scale(10), width=gd.scale(620), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        ui_manager.add(border)

        text = AttributedText(x=gd.scale(20), y=gd.scale(120),
                              width=gd.scale(600), height=gd.scale(520), text=self.text)

        ui_manager.add(text)

        for i, img in enumerate(self.images):
            img: Image = img

            x = gd.scale(20)
            y = gd.scale(70)

            if i == 1:
                x = gd.scale(330)
            elif i == 2:
                y = gd.scale(20)
            elif i == 3:
                x = gd.scale(330)
                y = gd.scale(20)

            w = gd.scale(290)
            h = gd.scale(30)

            style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
            ib = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=img.title, style=style)
            ib.on_click = self.on_image_click

            ui_manager.add(ib)

    def on_image_click(self, event):
        for img in self.images:
            img: Image = img

            if event.source.text == img.title:
                image_view = ImageView(img, self.parent)
                self.parent.window.show_view(image_view)
