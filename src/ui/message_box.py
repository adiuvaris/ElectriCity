from typing import Optional

import arcade
import arcade.gui
from arcade.gui.mixins import UIMouseFilterMixin
from arcade.gui.widgets import UILayout, UIAnchorWidget, UITextArea, UIFlatButton, UIBoxLayout
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED

import src.const as const
from src.data.game import gd


class MessageBox(UIMouseFilterMixin, UIAnchorWidget):
    """
    Meldungen anzeigen in einer View
    """

    def __init__(self, msg: str, buttons=("Ok",), callback=None):
        """
        Konstruktor
        :param msg: anzuzeigenden Text
        :param buttons: anzuzeigenden Buttons (Default ist nur OK)
        :param callback: Funktion, die bei einem Klick aufgerufen werden soll
        """

        # Position und Grösse des Textes und des Buttons festlegen
        w = gd.scale(400)
        h = gd.scale(280)
        fs = gd.scale(const.FONT_SIZE_H2)
        space = gd.scale(20)
        button_h = gd.scale(30)

        # Textbereich einfügen
        self._text_area = UITextArea(text=msg,
                                     width=w - 2 * space,
                                     height=h - 3 * space - button_h,
                                     font_size=fs,
                                     text_color=arcade.color.BLACK)

        # Buttons einfügen
        style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
        button_group = UIBoxLayout(vertical=False)
        for button_text in buttons:
            button = UIFlatButton(text=button_text, height=button_h, style=style)
            button_group.add(button.with_space_around(left=space))
            button.on_click = self.on_ok

        self._callback = callback

        # UI-Layouter die Ausrichtung der UI-Elemente anpassen lassen
        group = UILayout(width=w, height=h, children=[
            UIAnchorWidget(child=self._text_area, anchor_x="left", anchor_y="top", align_x=space, align_y=-space),
            UIAnchorWidget(child=button_group, anchor_x="right", anchor_y="bottom", align_x=-space, align_y=space)
        ]).with_border(width=5).with_space_around(bg_color=(220, 220, 220))

        # Konstruktor der Basisklasse aufrufen
        super().__init__(child=group)

    def on_event(self, event: arcade.gui.UIEvent) -> Optional[bool]:
        """
        Events verarbeiten
        :param event: Event, der ausgelöst wurde
        """

        # Update-Event weiter leiten
        if isinstance(event, arcade.gui.UIOnUpdateEvent):
            self.dispatch_event("on_update", event.dt)

        # ESC soll die Meldung schliessen
        if isinstance(event, arcade.gui.UIKeyPressEvent):
            if event.symbol == arcade.key.ESCAPE:
                self.on_ok(event)
                return EVENT_HANDLED

        # Event an UI-Elemente weiterleiten
        for child in self.children:
            if child.dispatch_event("on_event", event):
                return EVENT_HANDLED

        return EVENT_UNHANDLED

    def on_ok(self, event):
        """
        Callback für Klick auf OK
        :param event: Event, der ausgelöst wurde
        """

        # Messagebox entfernen und callback des Erzeugers aufrufen
        self.parent.remove(self)
        if self._callback is not None:
            self._callback(event)
