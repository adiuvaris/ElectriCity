
import os
import arcade
from src.sprites.character import Character

from src.data.game import gd


class Player(Character):
    """
    Player Sprite, basierend auf der Klasse Character
    """

    def __init__(self, avatar):
        """
        Konstruktor.

        :param avatar: Dateiname mit den Texturen für die Sprite
        """

        super().__init__(avatar)

        # Ton für Schritte laden
        self.sound_update = 0
        self.footstep_sound = None
        mypath = gd.get_abs_path("res/sounds")
        filename = f"{mypath}/footstep.wav"
        if os.path.exists(filename):
            self.footstep_sound = arcade.load_sound(filename)

    def set_avatar(self, avatar):
        super().set_avatar(avatar)

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
            self.sound_update = 0
            if self.footstep_sound is not None:
                arcade.play_sound(self.footstep_sound, volume=gd.get_volume() / 100.0)
