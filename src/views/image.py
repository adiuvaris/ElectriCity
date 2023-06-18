import arcade
import arcade.gui

from src.ui.labels import create_title_label
from src.ui.images import create_image_sprite


class Image(arcade.View):
    """
    Klasse für die View mit einem Bild
    """

    def __init__(self, bild, view):
        """
        Konstruktor
        """

        super().__init__()

        self.bild = bild
        self.view = view

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

    def setup(self):
        """
        View initialisieren.
        Es wird ein Bild angezeigt.
        """

        # Alle UI Elemente löschen
        self.manager.clear()

        # Titel-Element erzeugen
        if "Titel" in self.bild:
            title_label = create_title_label(self.bild["Titel"])
            self.manager.add(title_label)

        # Bild Element erzeugen
        if "Datei" in self.bild:
            image = create_image_sprite(self.bild["Datei"])
            self.manager.add(image)

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

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.view)

