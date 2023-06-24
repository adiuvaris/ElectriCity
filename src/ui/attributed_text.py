import arcade
import arcade.gui
import pyglet.window.key
from arcade.gui.surface import Surface
from pyglet.text.document import AbstractDocument
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED
from typing import Optional

import src.const as const
from src.data.game_data import gd


class AttributedText(arcade.gui.UIWidget):
    """
    Klasse für einen Text, der mit Attributen versehen sein kann, um
    Text zu strukturieren
    """
    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = 800,
                 height: float = 40,
                 text=None):
        """
        :param x: x-Koordinate links unten
        :param y: y-Koordinate links unten
        :param width: Breite
        :param height: Höhe
        :param text: Text mit Attributen
        """

        super().__init__(x, y, width, height)

        if text is None:
            text = []

        self.text = "\n\n\n".join(text)
        self.prepare_text()

        # Text in Dokument von pyglet abbilden
        self.doc: AbstractDocument = pyglet.text.decode_attributed(self.text)

        # Scrolling konfigurieren
        self.scroll_speed = const.FONT_SIZE
        self.layout = pyglet.text.layout.ScrollableTextLayout(
            self.doc, width=self.width, height=self.height, multiline=True)

    def prepare_text(self):

        fn = "{font_name 'Arial'}"
        fs = "{font_size " + str(gd.scale(const.FONT_SIZE)) + "}{bold False}"
        h1 = "{font_size " + str(gd.scale(const.FONT_SIZE_H1)) + "}{bold True}"
        h2 = "{font_size " + str(gd.scale(const.FONT_SIZE_H2)) + "}{bold True}"

        self.text = fn + self.text
        self.text = fs + self.text

        self.text = self.text.replace("<h1>", h1)
        self.text = self.text.replace("</h1>", fs)
        self.text = self.text.replace("<h2>", h2)
        self.text = self.text.replace("</h2>", fs)
        self.text = self.text.replace("<b>", "{bold True}")
        self.text = self.text.replace("</b>", "{bold False}")
        self.text = self.text.replace("<i>", "{italic True}")
        self.text = self.text.replace("</i>", "{italic False}")
        self.text = self.text.replace("<np>", "{font_name 'Courier New'}")
        self.text = self.text.replace("</np>", "{font_name 'Arial'}")

    def do_render(self, surface: Surface):
        self.prepare_render(surface)
        with surface.ctx.pyglet_rendering():
            self.layout.draw()

    def on_event(self, event: arcade.gui.UIEvent) -> Optional[bool]:

        # Handelt es sich um ein Scroll-Event?
        if isinstance(event, arcade.gui.UIMouseScrollEvent):

            # Befindet sich die Maus im Text?
            if self.rect.collide_with_point(event.x, event.y):

                # View-Position anpassen und neu zeichnen lassen
                self.layout.view_y += event.scroll_y * self.scroll_speed
                self.trigger_full_render()

        if super().on_event(event):
            return EVENT_HANDLED

        return EVENT_UNHANDLED
