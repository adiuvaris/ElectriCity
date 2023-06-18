
import arcade
from src.sprites.character import Character


class Player(Character):
    """
    Player Sprite, basierend auf der Klasse Character
    """

    def __init__(self, sheet_name):
        """
        Konstruktor.

        :param sheet_name: Dateiname mit den Texturen für die Sprite
        """

        super().__init__(sheet_name)

        # Ton für Schritte laden
        self.sound_update = 0
        self.footstep_sound = arcade.load_sound(":sounds:footstep00.wav")
        self.data = {}

    def on_update(self, delta_time: float = 1.0 / 60.0):
        """
        Sprite in der Bewegung aktualisieren.

        :param delta_time: Verstrichene Zeit seit dem letzten Aufruf
        """

        # Auswahl des richtigen Teilbildes (Textur) wird von der Klasse
        # Character erledigt.
        super().on_update(delta_time)

        # Ohne Bewegung wird auch kein Ton abgespielt
        if not self.change_x and not self.change_y:
            self.sound_update = 0
            return

        # Töne abspielen nach drei Aufrufen der Funktion
        if self.should_update > 3:
            self.sound_update += 1

        if self.sound_update >= 3:
            arcade.play_sound(self.footstep_sound, volume=0.1)
            self.sound_update = 0
