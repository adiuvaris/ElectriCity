import json
import os

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.ui.attributed_text import AttributedText
from src.data.media import Media
from src.views.image_view import ImageView
from src.views.audio_view import AudioView


class HelpView(arcade.View):
    """
    Klasse für die View mit einem Text
    """

    def __init__(self, filename, parent, exit_program=False):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Member definieren
        self.parent = parent
        self.exit_program = exit_program
        self.text = []
        self.titel = ""
        self.medias = []

        # JSON-File für Text einlesen
        mypath = gd.get_abs_path("res/data")
        filename = f"{mypath}/{filename}"
        if os.path.exists(filename):
            with open(filename, "r", encoding="'utf-8") as ifile:
                data = json.load(ifile)
                if "Titel" in data:
                    self.titel = data["Titel"]
                if "Text" in data:
                    self.text = data["Text"]

                # Audio Elemente einlesen
                if "Audios" in data:
                    audios = data["Audios"]
                    for audio in audios:
                        media = Media("audio")
                        if "Datei" in audio:
                            media.filename = audio["Datei"]
                        if "Titel" in audio:
                            media.title = audio["Titel"]
                        if "Beschreibung" in audio:
                            media.description = audio["Beschreibung"]
                        if "Illustration" in audio:
                            media.illustration = audio["Illustration"]
                        self.medias.append(media)

                # Bild Elemente einlesen
                if "Bilder" in data:
                    bilder = data["Bilder"]
                    for bild in bilder:
                        image = Media("image")
                        if "Datei" in bild:
                            image.filename = bild["Datei"]
                        if "Titel" in bild:
                            image.title = bild["Titel"]
                        if "Beschreibung" in bild:
                            image.description = bild["Beschreibung"]
                        if "Frames" in bild:
                            image.frames = bild["Frames"]
                        self.medias.append(image)

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        self.create_ui()

    def setup(self):
        """
        View initialisieren.
        Es wird ein Bild angezeigt.
        """
        pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn die View unsichtbar wird
        """

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zum Aufrufer
        if key == arcade.key.ESCAPE:

            # Falls gewünscht das Programm verlassen
            if self.exit_program:
                self.window.close()
            else:
                self.window.show_view(self.parent)

    def create_ui(self):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        """

        # Zuerst mal Elemente löschen
        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)
        self.manager.clear()

        # Titeltext oben in der Mitte
        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text=self.titel,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        b = gd.scale(5)

        text = AttributedText(x=gd.scale(240), y=gd.scale(120),
                              width=gd.scale(800),
                              height=gd.scale(520),
                              text=self.text).with_space_around(b, b, b, b).with_border()

        self.manager.add(text)

        # Buttons für Medien erzeugen
        w = gd.scale(190)
        h = gd.scale(30)
        y = gd.scale(610)
        x = gd.scale(1060)
        for medium in self.medias:
            medium: Media = medium

            style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
            ib = arcade.gui.UIFlatButton(x=x, y=y, width=w, height=h, text=medium.description, style=style)
            ib.on_click = self.on_media_click
            self.manager.add(ib)
            y = y - gd.scale(50)

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
                    image_view = ImageView(medium, self)
                    self.parent.window.show_view(image_view)
                elif media.typ == "audio":

                    # Sound ausgeben
                    audio_view = AudioView(medium, self)
                    self.parent.window.show_view(audio_view)
