import arcade


class Animation(arcade.Sprite):
    """
    Klasse für eine einfache Animation mit mehreren Frames in einem Bild.
    Das Einzel-Bild muss 1240x520 Pixel gross sein. Die Frames werden in der Bilddatei nebeneinander erwartet.
    Bei 10 Frames muss das ganze Bild also 12400x520 Pixel gross sein.
    """

    def __init__(self, filename, frames):
        """
        Konstruktor
        """

        # Basis-Konstruktor aufrufen
        super().__init__()

        # Texturen (Bild) für Sprite laden
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
        """
        Anzeige aktualisieren
        """

        # Nach 1/4 Sekunde das nächste Bild anzeigen
        self.dauer = self.dauer + delta_time
        if self.dauer > 0.25:
            self.dauer = 0.0
            self.cur_texture_index = self.cur_texture_index + 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0

            # Textur anzeigen
            self.texture = self.textures[self.cur_texture_index]
