
import os
import arcade
from collections import OrderedDict
from os.path import isfile, join
import src.const as const
from src.data.game import gd


class GameMap:
    """
    Container für alle Map-relevanten Daten
    """

    name = None
    scene = None
    map_layers = None
    map_size = None
    properties = None
    background_color = arcade.color.ALMOND


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

    # Spritelisten aus der Map übernehmen
    game_map.map_layers = my_map.sprite_lists

    # Map Grösse bestimmen
    game_map.map_size = my_map.width, my_map.height

    # Hintergrundfarbe setzen
    game_map.background_color = my_map.background_color

    # Einstellungen der Map übernehmen
    game_map.properties = my_map.properties

    # Layer mit Name 'blocking' als Mauer betrachten, welche Player-Sprite nicht passieren kann.
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
    mypath = gd.get_abs_path("res/maps")

    # Einmal eine Liste von allem Map-Files erstellen, die in der Folge geladen werden.
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

    # Letzten Eintrag aus der File-Liste holen und laden. Der Filename
    # wird dabei aus der Liste entfernt.
    map_name = load_maps.map_file_names.pop(0)
    load_maps.map_list[map_name] = load_map(f"{mypath}/{map_name}.json")

    # Progress berechnen für die Fortschrittsanzeige (in Prozent)
    files_left = load_maps.file_count - len(load_maps.map_file_names)
    progress = 100 * files_left / load_maps.file_count

    # Bestimmen, ob wir fertig sind.
    # Das ist passiert, sobald die Liste der Map-Files leer ist.
    done = len(load_maps.map_file_names) == 0

    return done, progress, load_maps.map_list


# Statische Daten der Maps, damit sie im Speicher bleiben, und nicht immer neu geladen werden müssen
load_maps.map_file_names = None
load_maps.map_list = None
load_maps.file_count = None
