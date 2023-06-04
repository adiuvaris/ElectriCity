
# import json
# from typing import Callable


import arcade
import arcade.gui
from arcade.experimental.lights import Light
from pyglet.math import Vec2

import src.const as const
from src.sprites.player import Player


class Game(arcade.View):

    def __init__(self, map_list):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Player Sprite
        self.player_sprite = None
        self.player_sprite_list = None

        # Zuletzt gedrückte Taste
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Physics Engine
        self.physics_engine = None

        # Maps
        self.map_list = map_list

        # Aktuelle Map
        self.cur_map_name = None

        # Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Licht
        x = 100
        y = 200
        radius = 150
        mode = "soft"
        color = arcade.csscolor.WHITE
        self.player_light = Light(x, y, radius, color, mode)

    def switch_map(self, map_name, start_x, start_y):
        self.cur_map_name = map_name

        self.my_map = self.map_list[self.cur_map_name]

        if self.my_map.background_color:
            arcade.set_background_color(self.my_map.background_color)

        map_height = self.my_map.map_size[1]
        self.player_sprite.center_x = (
            start_x * const.SPRITE_SIZE + const.SPRITE_SIZE / 2
        )
        self.player_sprite.center_y = (map_height - start_y) * const.SPRITE_SIZE - const.SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.setup_physics()

        if self.my_map.light_layer:
            self.my_map.light_layer.resize(self.window.width, self.window.height)

    def setup_physics(self):
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.my_map.scene["wall_list"]
        )

    def setup(self):

        # Player erzeugen
        self.player_sprite = Player(":characters:Female/Female 18-4.png")

        # Player platzieren
        start_x = const.STARTING_X
        start_y = const.STARTING_Y
        self.switch_map(const.STARTING_MAP, start_x, start_y)
        self.cur_map_name = const.STARTING_MAP

    def on_draw(self):

        arcade.start_render()
        cur_map = self.map_list[self.cur_map_name]

        # Alles "belichten"
        with cur_map.light_layer:
            arcade.set_background_color(cur_map.background_color)

            # Scrolling Camera
            self.camera_sprites.use()
            map_layers = cur_map.map_layers

            # Szene zeichen
            cur_map.scene.draw()

            # Player zeichnen
            self.player_sprite_list.draw()

        if cur_map.light_layer:
            cur_map.light_layer.draw(ambient_color=arcade.color.WHITE)

        # Scroll Camera
        self.camera_gui.use()

        # draw GUI
        self.ui_manager.draw()

    def scroll_to_player(self, speed=const.CAMERA_SPEED):
        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

    def on_show_view(self):
        my_map = self.map_list[self.cur_map_name]
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

    def on_update(self, delta_time):

        # Geschwindigkeit berechnen
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        is_moving_up = (
            self.up_pressed
            and not self.down_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        is_moving_down = (
            self.down_pressed
            and not self.up_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        is_moving_right = (
            self.right_pressed
            and not self.left_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        is_moving_left = (
            self.left_pressed
            and not self.right_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        is_moving_up_left = (
            self.up_pressed
            and self.left_pressed
            and not self.down_pressed
            and not self.right_pressed
        )

        is_moving_down_left = (
            self.down_pressed
            and self.left_pressed
            and not self.up_pressed
            and not self.right_pressed
        )

        is_moving_up_right = (
            self.up_pressed
            and self.right_pressed
            and not self.down_pressed
            and not self.left_pressed
        )

        is_moving_down_right = (
            self.down_pressed
            and self.right_pressed
            and not self.up_pressed
            and not self.left_pressed
        )

        if is_moving_up:
            self.player_sprite.change_y = const.MOVEMENT_SPEED

        if is_moving_down:
            self.player_sprite.change_y = -const.MOVEMENT_SPEED

        if is_moving_left:
            self.player_sprite.change_x = -const.MOVEMENT_SPEED

        if is_moving_right:
            self.player_sprite.change_x = const.MOVEMENT_SPEED

        if is_moving_up_left:
            self.player_sprite.change_y = const.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -const.MOVEMENT_SPEED / 1.5

        if is_moving_up_right:
            self.player_sprite.change_y = const.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = const.MOVEMENT_SPEED / 1.5

        if is_moving_down_left:
            self.player_sprite.change_y = -const.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -const.MOVEMENT_SPEED / 1.5

        if is_moving_down_right:
            self.player_sprite.change_y = -const.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = const.MOVEMENT_SPEED / 1.5

        # Player bewegen
        self.physics_engine.update()

        # Player animation
        self.player_sprite_list.on_update(delta_time)

        self.player_light.position = self.player_sprite.position

        # Türen prüfen
        map_layers = self.map_list[self.cur_map_name].map_layers

        # Hat es Türen
        if "doors" in map_layers:

            # Wurde die Türe getroffen
            doors_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["doors"]
            )

            # Ja
            if len(doors_hit) > 0:
                # Nötig Infos holen
                map_name = doors_hit[0].properties["next_map"]
                start_x = doors_hit[0].properties["start_x"]
                start_y = doors_hit[0].properties["start_y"]

                # Neue Map anzeigen
                self.switch_map(map_name, start_x, start_y)
            else:

                # Keine Türe getroffen, also normal scrollen
                self.scroll_to_player()
        else:

            # Keine Türe, also normal scrollen
            self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        if key in const.KEY_UP:
            self.up_pressed = True
        elif key in const.KEY_DOWN:
            self.down_pressed = True
        elif key in const.KEY_LEFT:
            self.left_pressed = True
        elif key in const.KEY_RIGHT:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])

    def on_key_release(self, key, modifiers):
        if key in const.KEY_UP:
            self.up_pressed = False
        elif key in const.KEY_DOWN:
            self.down_pressed = False
        elif key in const.KEY_LEFT:
            self.left_pressed = False
        elif key in const.KEY_RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.destination_point = x, y

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass

    def on_resize(self, width, height):
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
        cur_map = self.map_list[self.cur_map_name]

        if cur_map.light_layer:
            cur_map.light_layer.resize(width, height)
