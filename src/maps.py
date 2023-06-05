
import os
import arcade
from collections import OrderedDict
from os.path import isfile, join
from arcade.experimental.lights import Light, LightLayer
import src.const as const


class GameMap:
    """
    Container für alle Map-relevanten Daten
    """

    name = None
    scene = None
    map_layers = None
    light_layer = None
    map_size = None
    properties = None
    background_color = arcade.color.AMAZON


def load_map(map_name):
    """
    Eine einzelne Map mit dem Namen map_name in eine Instanz von GameMap laden
    :param map_name: Name der map
    :return: die neue Instanz von GameMap mit den geladenen Daten
    """

    # Ein neues Objekt für die Map anlegen und die Liste der Layer vorbereiten
    game_map = GameMap()
    game_map.map_layers = OrderedDict()

    # Liste der blockierenden sprites init
    layer_options = {
        "blocking": {
            "use_spatial_hash": True,
        },
    }

    # Map einlesen und Szene erzeugen
    my_map = arcade.tilemap.load_tilemap(map_name, scaling=const.TILE_SCALING, layer_options=layer_options)
    game_map.scene = arcade.Scene.from_tilemap(my_map)

    # Licht init
    game_map.light_layer = LightLayer(100, 100)
    x = 0
    y = 0
    radius = 1
    mode = "soft"
    color = arcade.csscolor.WHITE
    dummy_light = Light(x, y, radius, color, mode)
    game_map.light_layer.add(dummy_light)

    # Spritelisten aus der Map übernehmen
    game_map.map_layers = my_map.sprite_lists

    # Map Grösse bestimmen
    game_map.map_size = my_map.width, my_map.height

    # Hintergrundfarbe setzen
    game_map.background_color = my_map.background_color

    # Einstellungen der Map übernehmen
    game_map.properties = my_map.properties

    # Layer mit Name 'blocking' als Mauer betrachten
    game_map.scene.add_sprite_list("wall_list", use_spatial_hash=True)
    for layer, sprite_list in game_map.map_layers.items():
        if "blocking" in layer:
            game_map.scene.remove_sprite_list_by_object(sprite_list)
            game_map.scene["wall_list"].extend(sprite_list)

    return game_map


def load_maps():
    """
    Maps laden.
    Die Funktion muss so lange aufgerufen werden, bis sie done=True zurückgibt

    :return: Gibt ein Tuple zurück, zuerst ein bool, ob alle Maps geladen sind
             dann folgt der Progress-Wert von 0..100 und zuletzt die Liste der Maps
    """

    # Verzeichnis in dem die Maps liegen
    mypath = "res/maps"

    # Einmal eine Liste von allem Map-Files erstellen
    if load_maps.map_file_names is None:

        # Dictionary für alle Maps
        load_maps.map_list = {}

        # Alle Dateien mit der Endung .json als Map laden
        load_maps.map_file_names = [
            f[:-5]
            for f in os.listdir(mypath)
            if isfile(join(mypath, f)) and f.endswith(".json")
        ]
        load_maps.map_file_names.sort()
        load_maps.file_count = len(load_maps.map_file_names)

    # Loop über die Map-Liste und laden der Maps in die statischen Variablen
    map_name = load_maps.map_file_names.pop(0)
    load_maps.map_list[map_name] = load_map(f"res/maps/{map_name}.json")

    # Progress berechnen für die Fortschrittsanzeige
    files_left = load_maps.file_count - len(load_maps.map_file_names)
    progress = 100 * files_left / load_maps.file_count

    # Bestimmen, ob wir fertig sind.
    done = len(load_maps.map_file_names) == 0
    return done, progress, load_maps.map_list


# Statische Daten der Maps, damit sie im Speicher bleiben, und nicht immer neu geladen werden müssen
load_maps.map_file_names = None
load_maps.map_list = None
load_maps.file_count = None
