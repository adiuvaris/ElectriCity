import arcade
import arcade.gui
import json

import src.const as const
from src.data.game import gd

from src.base.term import Term

from src.ui.message_box import MessageBox

from src.data.theory import Theory
from src.data.media import Media
from src.data.task import Task
from src.data.task_createor import create_task

from src.views.image_view import ImageView


class BookView(arcade.View):
    """
    Klasse für die View mit Theorie oder Aufgabe
    """

    def __init__(self, room_nr, book_nr):
        """
        Konstruktor
        """

        super().__init__()

        self.lose_sound = arcade.load_sound(":sounds:lose.wav")
        self.ok_sound = arcade.load_sound(":sounds:ok.wav")

        self.room_nr = room_nr
        self.book_nr = book_nr

        self.title = ""
        self.theory = None
        self.tasks = []
        self.cur_task = 0
        self.correct = False
        self.msg_active = False

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

    def on_media_click(self, event):
        for media in self.theory.medias:
            medium: Media = media

            if event.source.text == medium.description:
                if medium.typ == "image":
                    image_view = ImageView(medium, self)
                    self.window.show_view(image_view)
                elif media.typ == "audio":
                    pass

    def on_key_press(self, key, modifiers):

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)

        task = self.tasks[self.cur_task]
        task.on_key_press(key, modifiers)

    def read_book(self):

        # JSON-File für Buch einlesen
        mypath = gd.get_abs_path("res/data")
        with open(f"{mypath}/book_{self.room_nr}_{self.book_nr}.json", "r", encoding="'utf-8") as ifile:
            data = json.load(ifile)

            # Titel-Element einlesen
            if "Titel" in data:
                self.title = data["Titel"]

            # Theorie-Text Element einlesen
            self.theory = Theory()
            if "Theorie" in data:
                self.theory.text = data["Theorie"]

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
                    self.theory.medias.append(media)

            # Aufgaben Element einlesen
            if "Aufgaben" in data:
                aufgaben = data["Aufgaben"]
                for aufgabe in aufgaben:
                    task = create_task(aufgabe)
                    self.tasks.append(task)

            gd.init_book(self.room_nr, self.book_nr, len(self.tasks))

    def create_ui(self):

        self.correct = False

        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)

        self.manager.clear()

        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text=self.title,
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)

        self.manager.add(titel.with_border())

        self.theory.create_ui(self.manager, callback=self.on_media_click)

        if self.cur_task < len(self.tasks):
            self.tasks[self.cur_task].create_ui(self.manager, self.on_end_task)
        else:
            self.window.show_view(self.window.game_view)

        self.manager.trigger_render()

    def on_end_task(self):
        if self.tasks[self.cur_task].correct:
            gd.set_task(self.room_nr, self.book_nr, self.cur_task)
            self.cur_task = self.cur_task + 1
            self.create_ui()

