
import arcade

# Fenstergrösse beim Start des Programms
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "ElectriCity"

FONT_SIZE = 12
FONT_SIZE_H1 = 20
FONT_SIZE_H2 = 16


TILE_SCALING = 1.0
SPRITE_SIZE = 32

# Geschwindigkeit des Players
MOVEMENT_SPEED = 3

# Start Map und Startposition
STARTING_MAP = "city"
STARTING_X = 2
STARTING_Y = 14

# Tastatur mapping
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]

# Geschwindigkeit mit der die Kamera dem Player folgt
CAMERA_SPEED = 0.1
