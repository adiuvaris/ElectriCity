from enum import Enum

import arcade

import src.const as const
from src.data.game import gd


class Direction(Enum):
    """
    Enum für die Bewegungsrichtungen
    """

    Down = 0
    Left = 1
    Right = 2
    Up = 3


class Character(arcade.Sprite):
    """
    Sprite, mit unterschiedlichen Ansichten je nachdem wie es bewegt wird.
    Die Texturen müssen in einer Bilddatei gespeichert sein.
    Für jede der vier Bewegungsrichtungen muss es drei Texturen (Einzelbilder) geben.
    """

    def __init__(self, avatar):
        """
        Konstruktor.
        Die Texturen des Sprites laden und die Attribute für die erste Textur
        initialisieren.

        :param avatar: Name des Files mit den unterschiedlichen Ansichten
        """

        super().__init__()

        # Textur-Info für die Bewegungsrichtungen.
        # Die Teilbilder 0, 1 und 2 sind für Bewegungen nach unten etc.
        self.info = {
            Direction.Down: [0, 1, 2],
            Direction.Left: [3, 4, 5],
            Direction.Right: [6, 7, 8],
            Direction.Up: [9, 10, 11],
        }

        # Texturen für Charakter Sprite laden
        self.set_avatar(avatar)

        # Erste Textur für die Anzeige definieren
        self.should_update = 0
        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]

    def set_avatar(self, avatar):
        """
        Avatar neu setzen
        :param avatar: Name des Files mit den unterschiedlichen Ansichten
        """

        # Datei einlesen
        mypath = gd.get_abs_path("res/avatars")
        avatar = mypath + "/" + avatar
        self.textures = arcade.load_spritesheet(
            avatar,
            sprite_width=const.SPRITE_SIZE,
            sprite_height=const.SPRITE_SIZE,
            columns=3,
            count=12,
        )

    def on_update(self, delta_time: float = 1.0 / 60.0):
        """
        Anzeige des Sprites aktualisieren, je nachdem wie es bewegt wird.
        :param delta_time:
        """

        # Keine Bewegung, also nichts tun
        if not self.change_x and not self.change_y:
            return

        # Nach drei Aufrufen zur nächsten Textur in der aktuellen Bewegungsrichtung gehen.
        # Damit wird das Armschwingen animiert.
        if self.should_update <= 3:
            self.should_update += 1
        else:
            self.should_update = 0
            self.cur_texture_index += 1

        # Textur für die Richtung der Bewegung bestimmen
        slope = self.change_y / (self.change_x + 0.0001)
        if abs(slope) < 0.8:
            if self.change_x > 0:
                direction = Direction.Right
            else:
                direction = Direction.Left
        else:
            if self.change_y > 0:
                direction = Direction.Up
            else:
                direction = Direction.Down

        # Wenn es den berechneten Textur-Index nicht gibt, dann wird die erste
        # Textur der entsprechenden Richtung verwendet.
        if self.cur_texture_index not in self.info[direction]:
            self.cur_texture_index = self.info[direction][0]

        # Textur anzeigen
        self.texture = self.textures[self.cur_texture_index]
