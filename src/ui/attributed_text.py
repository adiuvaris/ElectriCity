from typing import Optional

import arcade
import arcade.gui
import pyglet.window.key
from arcade.gui.surface import Surface
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED
from pyglet.text.document import AbstractDocument

import src.const as const
from src.data.game import gd


class AttributedText(arcade.gui.UIWidget):
    """
    Klasse für einen Text, der mit Attributen versehen sein kann, um
    Text zu strukturieren (Kursiv, Fett, Variablen etc.)
    """

    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = 800,
                 height: float = 40,
                 text=None,
                 variables=None):
        """
        Konstruktor

        :param x: x-Koordinate links unten
        :param y: y-Koordinate links unten
        :param width: Breite
        :param height: Höhe
        :param text: Text mit Attributen
        """

        # Basiskonstruktor aufrufen
        super().__init__(x, y, width, height)

        # Sicherstellen, dass variables ein dict ist
        if variables is None:
            variables = {}

        # Sicherstellen, dass text eine Liste ist
        if text is None:
            text = []

        # Member init
        self.variables = variables
        self.text = "\n\n\n".join(text)
        self.prepare_text()

        # Text in Dokument von pyglet abbilden
        self.doc: AbstractDocument = pyglet.text.decode_attributed(self.text)

        # Scrolling konfigurieren
        self.scroll_speed = const.FONT_SIZE
        self.layout = pyglet.text.layout.ScrollableTextLayout(
            self.doc, width=self.width, height=self.height, multiline=True)

    def prepare_text(self):
        """
        Text für pyglet anpassen
        """

        # Standardschriften für pyglet setzten
        fn = "{font_name 'Arial'}"
        fs = "{font_size " + str(gd.scale(const.FONT_SIZE)) + "}{bold False}"
        h1 = "{font_size " + str(gd.scale(const.FONT_SIZE_H1)) + "}{bold True}"
        h2 = "{font_size " + str(gd.scale(const.FONT_SIZE_H2)) + "}{bold True}"

        self.text = fn + self.text
        self.text = fs + self.text

        # Attribute für pyglet umsetzen
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

        # Variablen-Werte eintragen
        for k, v in self.variables.items():
            var_name = "<" + k + ">"
            self.text = self.text.replace(var_name, str(v))

    def do_render(self, surface: Surface):
        """
        Text aufbereiten
        """

        self.prepare_render(surface)
        with surface.ctx.pyglet_rendering():
            self.layout.draw()

    def on_event(self, event: arcade.gui.UIEvent) -> Optional[bool]:
        """
        Events im Text verarbeiten (scrolling)
        """

        # Handelt es sich um ein Scroll-Event?
        if isinstance(event, arcade.gui.UIMouseScrollEvent):

            # Befindet sich die Maus im Text?
            if self.rect.collide_with_point(event.x, event.y):
                # View-Position anpassen und neu zeichnen lassen
                self.layout.view_y += event.scroll_y * self.scroll_speed
                self.trigger_full_render()

        # Basisklasse aufrufen
        if super().on_event(event):
            return EVENT_HANDLED

        return EVENT_UNHANDLED
