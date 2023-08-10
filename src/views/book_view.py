import json

import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.data.media import Media
from src.ui.theory import Theory
from src.views.quiz_view import create_task


class BookView(arcade.View):
    """
    Klasse für die View mit Theorie und Aufgabe
    """

    def __init__(self, room_nr, book_nr):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # Member definieren
        self.room_nr = room_nr
        self.book_nr = book_nr
        self.title = ""
        self.theory = None
        self.tasks = []
        self.cur_task = 0

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        # Buch einlesen (json)
        self.read_book()

        # Buch darstellen
        self.create_ui()

    def setup(self):
        """
        View initialisieren.
        Es wird die Theorie für den Raum und das Buch angezeigt.
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
        Callback, wenn eine Taste gedrückt wurde
        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zur Map
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)

        # Tastendruck zur aktuellen Aufgabe weitergeben
        task = self.tasks[self.cur_task]
        task.on_key_press(key, modifiers)

    def on_end_task(self):
        """
        Eine Aufgabe wurde erledigt, also die nächste anzeigen
        """

        # Ist die Aufgabe gelöst?
        if self.tasks[self.cur_task].correct:

            # Aufgabe in den Spieler-Daten als gelöst markieren
            gd.set_task(self.room_nr, self.book_nr, self.cur_task)

            # Nächste Aufgabe anzeigen, wenn es eine hat
            self.cur_task = self.cur_task + 1
            self.create_ui()

    def read_book(self):
        """
        JSON Struktur eines Buches einlesen
        """

        # JSON-File für Buch einlesen
        mypath = gd.get_abs_path("res/data")
        with open(f"{mypath}/book_{self.room_nr}_{self.book_nr}.json", "r", encoding="'utf-8") as ifile:

            # date bekommt die JSON-Struktur des Buchs
            data = json.load(ifile)

            # Titel-Element einlesen
            if "Titel" in data:
                self.title = data["Titel"]

            # Theorie-Text Element einlesen
            self.theory = Theory()
            if "Theorie" in data:
                self.theory.text = data["Theorie"]

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
                    self.theory.medias.append(media)

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
                    self.theory.medias.append(image)

            # Aufgaben Elemente einlesen
            if "Aufgaben" in data:
                aufgaben = data["Aufgaben"]
                for aufgabe in aufgaben:
                    task = create_task(aufgabe)
                    self.tasks.append(task)

            # Buch in den Spieler-Daten eintragen
            gd.init_book(self.room_nr, self.book_nr, len(self.tasks))

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
                                   text=self.title,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        # UI der Theorie anzeigen
        self.theory.create_ui(self.manager, self)

        # Falls es eine Aufgabe hat, diese anzeigen
        if self.cur_task < len(self.tasks):
            self.tasks[self.cur_task].create_ui(self.manager, self.on_end_task)
        else:
            self.window.show_view(self.window.game_view)

        self.manager.trigger_render()
