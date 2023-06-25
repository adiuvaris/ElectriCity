import arcade
from arcade.gui.mixins import UIMouseFilterMixin
from arcade.gui.widgets import UILayout, UIAnchorWidget, UITextArea, UIFlatButton, UIBoxLayout

import src.const as const
from src.data.game import gd


class MessageView(UIMouseFilterMixin, UIAnchorWidget):

    def __init__(self, msg: str, buttons=("Ok",), callback=None):

        w = gd.scale(640)
        h = gd.scale(480)
        fs = gd.scale(const.FONT_SIZE_H2)
        space = gd.scale(10)

        self._text_area = UITextArea(text=msg,
                                     width=w - space,
                                     height=h - space,
                                     font_size=fs,
                                     text_color=arcade.color.BLACK)

        style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
        button_group = UIBoxLayout(vertical=False)
        for button_text in buttons:
            button = UIFlatButton(text=button_text, style=style)
            button_group.add(button.with_space_around(left=space))
            button.on_click = self.on_ok

        self._callback = callback

        group = UILayout(width=w, height=h, children=[
            UIAnchorWidget(child=self._text_area, anchor_x="left", anchor_y="top", align_x=space, align_y=-space),
            UIAnchorWidget(child=button_group, anchor_x="right", anchor_y="bottom", align_x=-space, align_y=space)
        ]).with_space_around(bg_color=(220, 220, 220))

        super().__init__(child=group)

    def on_ok(self, event):
        self.parent.remove(self)
        if self._callback is not None:
            self._callback(event.source.text)

