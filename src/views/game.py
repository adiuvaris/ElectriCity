
import arcade
import arcade.gui
from arcade.experimental.lights import Light
from pyglet.math import Vec2
import src.const as const
from src.sprites.player import Player


class Game(arcade.View):
    """
    View des Spiels mit der Darstellung der Map (city, room, test)
    """

    def __init__(self, map_list):
        """
        Konstruktor, der alle Attribute anlegt und arcade initialisiert.

        :param map_list: Die globale Liste der geladenen Maps
        """

        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        # Manager für das User Interface aktivieren
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

        # Licht initialisieren
        x = 100
        y = 200
        radius = 150
        mode = "soft"
        color = arcade.csscolor.WHITE
        self.player_light = Light(x, y, radius, color, mode)

    def switch_map(self, map_name, start_x, start_y):
        """
        Anzeige einer bestimmten Map

        :param map_name: Map, die angezeigt werden soll
        :param start_x: Startposition in X Richtung
        :param start_y: Startposition in Y Richtung
        """

        # Aktuell Map übernehmen
        self.cur_map_name = map_name
        self.my_map = self.map_list[self.cur_map_name]

        # Wenn in der Map eine Hintergrundfarbe definiert ist, diese übernehmen
        if self.my_map.background_color:
            arcade.set_background_color(self.my_map.background_color)

        # Daten von der Map in diese View übernehmen
        map_height = self.my_map.map_size[1]
        self.player_sprite.center_x = (start_x * const.SPRITE_SIZE + const.SPRITE_SIZE / 2)
        self.player_sprite.center_y = (map_height - start_y) * const.SPRITE_SIZE - const.SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        # Physik und Licht in der View initialisieren
        self.setup_physics()
        if self.my_map.light_layer:
            self.my_map.light_layer.resize(self.window.width, self.window.height)

    def setup_physics(self):
        """
        Physik der View initialieren
        """

        # Einfache Physik mit der wall_list als blockierende Elemente
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.my_map.scene["wall_list"])

    def setup(self):
        """
        View initialisieren.
        Das Player Sprite anlegen und positionieren sowie die aktuelle Map anzeigen
        """

        # Player erzeugen
        self.player_sprite = Player(":characters:Female/Female 18-4.png")

        # Aktuelle Map anzeigen
        start_x = const.STARTING_X
        start_y = const.STARTING_Y
        self.switch_map(const.STARTING_MAP, start_x, start_y)
        self.cur_map_name = const.STARTING_MAP

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

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

        # Kameraposition anpassen
        self.camera_gui.use()

        # Arcade auffordern den Rest zu zeichnen
        self.ui_manager.draw()

    def scroll_to_player(self, speed=const.CAMERA_SPEED):
        """
        Ansicht der Map mit dem Player abgleichen.
        Damit wird erreicht, dass das Player Sprite immer im Bereich des Fensters bleibt,
        wenn es bewegt wird.
        Das meiste macht arcade. Wir müssen nur einen Vektor vom Player Sprite
        zum Zentrum des Fensters übergeben.

        :param speed: Geschwindigkeit
        """

        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

        # Wenn in der Map eine Hintergrundfarbe definiert ist, diese übernehmen
        my_map = self.map_list[self.cur_map_name]
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

    def on_update(self, delta_time):
        """
        Wird von arcade aufgerufen, damit wir auf Veränderungen in der View
        reagieren können. Das Player Sprite bewegen und auf Kollisionen mit Türen
        reagieren.

        :param delta_time: vergangene Zeit seit letztem Aufruf
        """

        # Richtung des Player Sprites berechnen, wenn entsprechende Tasten gedrückt sind.
        # Dazu werden alle aktuellen Tastendrücke beachtet und dann die
        # X- und Y-Änderungen definiert.
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

        # Kollisionen mit Türen prüfen
        map_layers = self.map_list[self.cur_map_name].map_layers

        # Hat es Türen
        if "doors" in map_layers:

            # Wurde die Türe getroffen
            doors_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["doors"]
            )

            # Ja - es gibt eine Kollision
            if len(doors_hit) > 0:

                # Nötig Infos holen, damit die neue Map angezeigt werden kann
                map_name = doors_hit[0].properties["next_map"]
                start_x = doors_hit[0].properties["start_x"]
                start_y = doors_hit[0].properties["start_y"]

                # Neue Map anzeigen
                self.switch_map(map_name, start_x, start_y)
            else:

                # Keine Türe getroffen, also normal scrollen, damit das Player Sprite
                # etwa in der Mitte des Fenster bleibt.
                self.scroll_to_player()
        else:

            # Keine Türe, also normal scrollen
            self.scroll_to_player()

        # Hat es Views
        if "views" in map_layers:

            # Wurde eine View getroffen
            views_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["views"]
            )

            # Ja - es gibt eine Kollision
            if len(views_hit) > 0:

                # Detail holen, damit die View angezeigt werden kann
                view_name = views_hit[0].properties["view"]
                next_x = views_hit[0].properties["next_x"]
                next_y = views_hit[0].properties["next_y"]

                # Player positionieren und Bewegung stoppen, damit nach dem Schliessen der Info-View
                # nicht gleich wieder ein Hit erfolgt
                map_height = self.my_map.map_size[1]
                self.player_sprite.center_x = (next_x * const.SPRITE_SIZE + const.SPRITE_SIZE / 2)
                self.player_sprite.center_y = (map_height - next_y) * const.SPRITE_SIZE - const.SPRITE_SIZE / 2
                self.up_pressed = False
                self.down_pressed = False
                self.left_pressed = False
                self.right_pressed = False

                # Neue view anzeigen
                self.window.views["info"].setup(view_name)
                self.window.show_view(self.window.views["info"])

            else:

                # Keine Türe getroffen, also normal scrollen, damit das Player Sprite
                # etwa in der Mitte des Fenster bleibt.
                self.scroll_to_player()
        else:

            # Keine Türe, also normal scrollen
            self.scroll_to_player()


    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.
        Der Wert wird in die entsprechenden Attribute übernommen.
        Die Tastendrücke werden effektiv in der Funktion on_update behandelt.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        if key in const.KEY_UP:
            self.up_pressed = True
        elif key in const.KEY_DOWN:
            self.down_pressed = True
        elif key in const.KEY_LEFT:
            self.left_pressed = True
        elif key in const.KEY_RIGHT:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:

            # Die Escape Taste startet das Hauptmenü
            self.window.show_view(self.window.views["menu"])

    def on_key_release(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste losgelassen wird.

        Der Wert wird in die entsprechenden Attribute übernommen.
        Die Tastendrücke werden effektiv in der Funktion on_update behandelt.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        if key in const.KEY_UP:
            self.up_pressed = False
        elif key in const.KEY_DOWN:
            self.down_pressed = False
        elif key in const.KEY_LEFT:
            self.left_pressed = False
        elif key in const.KEY_RIGHT:
            self.right_pressed = False

    def on_resize(self, width, height):
        """
        Wird von arcade aufgerufen, wenn die Fenstergrösse ändert.

        :param width: Neue Breite
        :param height: Neue Höhe
        """

        # Die Grössenänderung an die "Kamera" weitergeben
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
        cur_map = self.map_list[self.cur_map_name]

        if cur_map.light_layer:
            cur_map.light_layer.resize(width, height)
