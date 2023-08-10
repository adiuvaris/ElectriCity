import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.media import Media
from src.ui.attributed_text import AttributedText
from src.views.audio_view import AudioView
from src.views.image_view import ImageView


class Theory:
    """
    Klasse für den Theorie-Teil eines Buches, der links angezeigt wird
    """

    def __init__(self):
        """
        Konstruktor
        """

        # Member definieren
        self.text = ""
        self.medias = []
        self.parent = None

    def create_ui(self, ui_manager: arcade.gui.UIManager, parent: arcade.View):
        """
        User-Interface erstellen
        :param ui_manager: Arcade UIManager
        :param parent: aufrufende View
        """

        # Referenz auf view speichern
        self.parent = parent

        # Rahmen links zeichnen
        widget = arcade.gui.UIWidget(x=gd.scale(10), y=gd.scale(10), width=gd.scale(420), height=gd.scale(640))
        border = arcade.gui.UIBorder(child=widget)
        ui_manager.add(border)

        # Text ausgeben - oben links
        text = AttributedText(x=gd.scale(20), y=gd.scale(120),
                              width=gd.scale(400), height=gd.scale(520), text=self.text)
        ui_manager.add(text)

        # Buttons für Medien erzeugen
        w = gd.scale(190)
        h = gd.scale(30)
        for i, medium in enumerate(self.medias):
            medium: Media = medium

            # Position des i-ten Buttons berechnen
            x = gd.scale(20)
            y = gd.scale(70)
            if i == 1:
                x = gd.scale(230)
            elif i == 2:
                y = gd.scale(20)
            elif i == 3:
                x = gd.scale(230)
                y = gd.scale(20)

            style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
            ib = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=medium.description, style=style)
            ib.on_click = self.on_media_click
            ui_manager.add(ib)

    def on_media_click(self, event):
        """
        Callback für die Ausgabe eines Mediums (Bild, Audio etc.)
        :param event: Event von Arcade
        """

        # Medium suchen auf das geklickt wurde
        for media in self.medias:
            medium: Media = media

            if event.source.text == medium.description:
                if medium.typ == "image":

                    # Bild anzeigen
                    image_view = ImageView(medium, self.parent)
                    self.parent.window.show_view(image_view)
                elif media.typ == "audio":

                    # Sound ausgeben
                    audio_view = AudioView(medium, self.parent)
                    self.parent.window.show_view(audio_view)
