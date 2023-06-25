import arcade
from arcade.gui.mixins import UIMouseFilterMixin
from arcade.gui.widgets import UILayout, UIAnchorWidget, UITextArea, UIFlatButton, UIBoxLayout

import src.const as const
from src.data.game import gd


class MessageView(UIMouseFilterMixin, UIAnchorWidget):

    def __init__(self, text):

        x = gd.scale(20)
        y = gd.scale(70)
        w = gd.scale(640)
        h = gd.scale(480)

        self._text_area = UITextArea(text=text,
                                     width=w,
                                     height=h,
                                     text_color=arcade.color.BLACK)

        button = UIFlatButton(text="OK")
        button.on_click = self.on_ok

        w = gd.scale(640)
        h = gd.scale(480)

        group = UILayout(width=w, height=h, children=[self._text_area, button])

        super().__init__(child=group)

    def on_ok(self, event):
        self.parent.remove(self)
