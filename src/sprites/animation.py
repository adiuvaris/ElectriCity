
import arcade
from src.data.game import gd


class Animation(arcade.Sprite):
    """
    """

    def __init__(self, filename, frames):

        super().__init__()

        # Texturen für Charakter Sprite laden
        self.textures = arcade.load_spritesheet(
            filename,
            sprite_width=1240,
            sprite_height=520,
            columns=frames,
            count=frames,
        )

        # Erste Textur für die Anzeige definieren
        self.dauer = 0.0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]

    def on_update(self, delta_time: float = 1.0 / 60.0):

        self.dauer = self.dauer + delta_time
        if self.dauer > 0.25:
            self.dauer = 0.0
            self.cur_texture_index = self.cur_texture_index + 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0

            # Textur anzeigen
            self.texture = self.textures[self.cur_texture_index]
