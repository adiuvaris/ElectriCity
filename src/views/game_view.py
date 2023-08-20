import os

import arcade
import arcade.gui
from pyglet.math import Vec2

import src.const as const
from src.data.game import gd
from src.sprites.player import Player
from src.views.book_view import BookView
from src.views.help_view import HelpView
from src.views.menu_view import MenuView
from src.views.quiz_view import QuizView


class GameView(arcade.View):
    """
    View des Spiels mit der Darstellung der Map (city, room, view)
    """

    def __init__(self, map_list):
        """
        Konstruktor, der alle Attribute anlegt und arcade initialisiert.

        :param map_list: Die globale Liste der geladenen Maps
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        arcade.set_background_color(arcade.color.ALMOND)

        # Manager für das User Interface aktivieren
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Member definieren
        self.laser_sound = arcade.load_sound(":sounds:laser.wav")
        self.door_open_sound = arcade.load_sound(":sounds:door_open.wav")
        self.door_close_sound = arcade.load_sound(":sounds:door_close.wav")
        self.book_sound = arcade.load_sound(":sounds:book.wav")
        self.lose_sound = arcade.load_sound(":sounds:lose.wav")

        # Player Sprite
        self.player_sprite = Player(gd.get_avatar())
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
        self.my_map = None

        # Meldungstext init
        self.message = ""
        self.title = arcade.Text("", 0, 0, arcade.color.BLACK, gd.scale(const.FONT_SIZE_H2), bold=True, anchor_y="center")

        # Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

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

        # Physik in der View initialisieren
        self.setup_physics()

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        mypath = gd.get_abs_path("res/data")
        filename = f"{mypath}/{map_name}.json"
        if os.path.exists(filename):
            hint_file = f"{map_name}.json"
            hint = HelpView(hint_file, self)
            self.window.show_view(hint)

    def setup_physics(self):
        """
        Physik der View initialisieren
        """

        # Einfache Physik mit der wall_list als blockierende Elemente
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.my_map.scene["wall_list"])

    def setup(self):
        """
        View initialisieren.
        Player Sprite anlegen und positionieren sowie die aktuelle Map anzeigen
        """

        # Player erzeugen
        self.player_sprite = Player(gd.get_avatar())

        # Aktuelle Map anzeigen
        start_x = const.STARTING_X
        start_y = const.STARTING_Y
        self.switch_map(const.STARTING_MAP, start_x, start_y)
        self.cur_map_name = const.STARTING_MAP

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """
        self.clear()

        arcade.start_render()
        cur_map = self.map_list[self.cur_map_name]

        arcade.set_background_color(cur_map.background_color)

        # Scrolling Camera
        self.camera_sprites.use()

        # Szene zeichen
        cur_map.scene.draw()

        # Player zeichnen
        self.player_sprite_list.draw()

        if len(self.message) > 0:
            self.title.text = self.message

            w = self.title.content_width
            h = self.title.content_height * 1.2

            arcade.draw_rectangle_filled(
                self.player_sprite.center_x + w / 2, self.player_sprite.center_y + h / 2, w, h, arcade.color.ALMOND)

            self.title.x = self.player_sprite.center_x
            self.title.y = self.player_sprite.center_y + h / 2

            self.title.draw()

        # Kameraposition anpassen
        self.camera_gui.use()

        # Arcade auffordern den Rest zu zeichnen
        self.ui_manager.draw()

    def scroll_to_player(self, speed=const.CAMERA_SPEED):
        """
        Ansicht der Map mit dem Player abgleichen.
        Damit wird erreicht, dass Player Sprite immer im Bereich des Fensters bleibt,
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

        # In dieser Ansicht braucht es keinen Mauszeiger
        self.window.set_mouse_visible(False)

        # Player Avatar setzen
        self.player_sprite.set_avatar(gd.get_avatar())

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn eine andere View sichtbar wird
        """

        # In allen anderen Ansichten braucht es einen Mauszeiger
        self.window.set_mouse_visible(True)

    def on_update(self, delta_time):
        """
        Wird von arcade aufgerufen, damit wir auf Veränderungen in der View
        reagieren können. Player Sprite bewegen und auf Kollisionen mit Türen
        reagieren.

        :param delta_time: vergangene Zeit seit letztem Aufruf
        """

        if self.physics_engine is None:
            return

        # Richtung des Player Sprites berechnen, wenn entsprechende Tasten gedrückt sind.
        # Dazu werden alle aktuellen Tastendrücke beachtet und dann die
        # X- und Y-Änderungen definiert.
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        self.message = ""

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

                # Nötige Infos holen, damit die neue Map angezeigt werden kann
                map_name = doors_hit[0].properties["next_map"]
                start_x = doors_hit[0].properties["start_x"]
                start_y = doors_hit[0].properties["start_y"]

                if map_name == "city" or gd.has_room_key(map_name[5:]):
                    if map_name == "city":
                        arcade.play_sound(self.door_close_sound, volume=gd.get_volume() / 100.0)
                    else:
                        arcade.play_sound(self.door_open_sound, volume=gd.get_volume() / 100.0)

                    # Neue Map anzeigen
                    self.switch_map(map_name, start_x, start_y)
                else:
                    # Fehlermeldung ausgeben
                    self.message = "Du hast keinen Schlüssel!"

            else:

                # Keine Türe getroffen, also normal scrollen, damit Player Sprite
                # etwa in der Mitte des Fensters bleibt.
                self.scroll_to_player()
        else:

            # Keine Türe, also normal scrollen
            self.scroll_to_player()

        if "quiz" in map_layers:

            # Wurde die Türe getroffen
            quiz_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["quiz"]
            )

            # Ja - es gibt eine Kollision
            if len(quiz_hit) > 0:

                # Nötige Infos holen
                room = quiz_hit[0].properties["room"]
                start_quiz = True

                # Ab Raum zwei prüfen, ob der vorherige Raum fertig gelöst wurde
                if int(room) > 1:

                    # String mit vorherigem Raum basteln und prüfen
                    check_room = str(int(room) - 1).zfill(2)
                    if not gd.has_all_tasks(check_room):
                        # Es wurde noch nicht alle Aufgaben gelöst, also Meldung anzeigen
                        # und Quiz nicht starten
                        start_quiz = False
                        self.message = f"Haus {int(check_room)} ist noch nicht gelöst!"

                if start_quiz:
                    arcade.play_sound(self.laser_sound, volume=gd.get_volume() / 100.0)

                    # Player positionieren und Bewegung stoppen, damit nach dem Schliessen der Info-View
                    # nicht gleich wieder ein Hit erfolgt
                    if self.up_pressed:
                        self.up_pressed = False
                        self.player_sprite.center_y = quiz_hit[0].center_y - const.SPRITE_SIZE

                    if self.down_pressed:
                        self.down_pressed = False
                        self.player_sprite.center_y = quiz_hit[0].center_y + const.SPRITE_SIZE

                    if self.left_pressed:
                        self.left_pressed = False
                        self.player_sprite.center_x = quiz_hit[0].center_x + const.SPRITE_SIZE

                    if self.right_pressed:
                        self.right_pressed = False
                        self.player_sprite.center_x = quiz_hit[0].center_x - const.SPRITE_SIZE

                    quiz = QuizView(room)
                    self.window.show_view(quiz)

            else:

                # Keine Türe getroffen, also normal scrollen, damit Player Sprite
                # etwa in der Mitte des Fensters bleibt.
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
                room_nr = views_hit[0].properties["room"]
                book_nr = views_hit[0].properties["book"]
                if "correct" in views_hit[0].properties:
                    res2 = eval(views_hit[0].properties["correct"])
                    pass
                if "wrong" in views_hit[0].properties:
                    pass

                start_book = True

                # Ab Buch zwei prüfen, ob das vorherige Buch fertig gelöst wurde
                if int(book_nr) > 1:

                    # String mit vorherigem Raum basteln und prüfen
                    check_book = str(int(book_nr) - 1).zfill(2)
                    if not gd.has_all_tasks(room_nr, check_book):
                        # Es wurde noch nicht alle Aufgaben gelöst, also Meldung anzeigen
                        # und Buch nicht starten
                        start_book = False
                        self.message = f"Buch {int(check_book)} ist noch nicht gelöst!"

                if start_book:

                    arcade.play_sound(self.book_sound, volume=gd.get_volume() / 100.0)

                    # Player positionieren und Bewegung stoppen, damit nach dem Schliessen der Info-View
                    # nicht gleich wieder ein Hit erfolgt
                    if self.up_pressed:
                        self.up_pressed = False
                        self.player_sprite.center_y = views_hit[0].center_y - const.SPRITE_SIZE - const.SPRITE_SIZE / 2

                    if self.down_pressed:
                        self.down_pressed = False
                        self.player_sprite.center_y = views_hit[0].center_y + const.SPRITE_SIZE + const.SPRITE_SIZE / 2

                    if self.left_pressed:
                        self.left_pressed = False
                        self.player_sprite.center_x = views_hit[0].center_x + const.SPRITE_SIZE + const.SPRITE_SIZE / 2

                    if self.right_pressed:
                        self.right_pressed = False
                        self.player_sprite.center_x = views_hit[0].center_x - const.SPRITE_SIZE - const.SPRITE_SIZE / 2

                    # Neue view anzeigen
                    v = BookView(room_nr, book_nr)
                    v.setup()
                    self.window.show_view(v)

            else:

                # Keine Türe getroffen, also normal scrollen, damit Player Sprite
                # etwa in der Mitte des Fensters bleibt.
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
        elif key == arcade.key.F1:
            # Anleitung
            hint = HelpView("anleitung.json", self)
            self.window.show_view(hint)

        elif key == arcade.key.M or key == arcade.key.ESCAPE:

            # Hauptmenü
            menu = MenuView()
            self.window.show_view(menu)

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

        :param width: neue Breite
        :param height: neue Höhe
        """

        # Die Grössenänderung an die "Kamera" weitergeben
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
