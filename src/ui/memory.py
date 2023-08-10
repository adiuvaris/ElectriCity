import random
import time

import arcade
import arcade.gui

import src.const as const
from src.data.card import Card
from src.data.game import gd
from src.ui.attributed_text import AttributedText
from src.ui.task import Task


class Memory(Task):
    """
    Klasse für eine Aufgabe, die als Memory angezeigt wird
    """

    def __init__(self, aufgabe: dict):
        """
        Konstruktor
        :param aufgabe: eingelesene JSON-Struktur der Aufgabe
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__(aufgabe)

        # Member definieren
        self.karten = []
        self.aufgabe_text = None
        self.first_card = None
        self.second_card = None

        # Karten aus der Aufgabe in eine Liste von Card Objekten übernehmen
        if "Karten" in aufgabe:
            karten = aufgabe["Karten"]
            for k in karten:
                card = Card()
                if "Bild" in k:
                    card.bild = k["Bild"]
                if "Key" in k:
                    card.key = k["Key"]
                self.karten.append(card)

    def create_ui(self, ui_manager: arcade.gui.UIManager, callback):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        :param ui_manager: Arcade UIManager
        :param callback: Funktion, die zum Abschluss der Aufgabe aufgerufen werden soll
        """

        # Basisklasse aufrufen
        super().create_ui(ui_manager, callback)

        # Aufgabentext auf der linken Seite
        self.aufgabe_text = AttributedText(
            x=gd.scale(20), y=gd.scale(20),
            width=gd.scale(400), height=gd.scale(300), text=self.aufgabe)
        self.manager.add(self.aufgabe_text)

        # Breite und Höhe der Karten auf dem Bildschirm festlegen
        w = 200
        h = 150

        # Bild für Rückseite der Karten laden
        mypath = gd.get_abs_path("res/images")
        avatar_path = mypath + "/back.png"
        te = arcade.load_texture(avatar_path, x=0, y=0, width=200, height=200)

        # Liste der Karten mischen, damit das Memory immer anders aussieht.
        random.shuffle(self.karten)

        # Karten auf ein 4x4 Raster legen und Buttons erzeugen
        idx = 0
        for i in range(4):
            for j in range(4):

                # Da self.karten gemischt wurde, kann hier immer das nächste Element verwendet werden
                karte = self.karten[idx]
                karte.position = (i, j)
                idx = idx + 1

                # Position des Buttons berechnen
                x = 460 + i * w
                y = 30 + j * h
                style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}
                karte.button = arcade.gui.UITextureButton(x=gd.scale(x + 5), y=gd.scale(y + 5),
                                                          width=gd.scale(w - 10), height=gd.scale(h - 10), texture=te,
                                                          style=style)
                karte.button.on_click = self.on_memory_click
                self.manager.add(karte.button)

    def on_memory_click(self, event):
        """
        Callback für den Klick auf eine Karte
        :param event: Event von Arcade
        """

        # Wenn schon zwei Karten aufgedeckt sind, dann nichts mehr tun
        if self.first_card is not None and self.second_card is not None:
            return

        # Angeklickte Karte suchen
        for karte in self.karten:
            if karte.button == event.source:

                # Vorderseite der Karte anzeigen
                mypath = gd.get_abs_path("res/images")
                avatar_path = mypath + "/" + karte.bild
                te = arcade.load_texture(avatar_path, x=0, y=0, width=400, height=400)
                karte.button.texture = te
                self.manager.trigger_render()

                # Wenn das die erste Karte ist, dann diese merken und sonst nichts mehr tun.
                if self.first_card is None:
                    self.first_card = karte
                else:

                    # Wenn das die erste und die zweite Karte gleich sind, dann gilt das nicht
                    if karte == self.first_card:
                        return

                    # Zweite Karte merken
                    self.second_card = karte

                    # Aufgabentext anpassen
                    self.manager.remove(self.aufgabe_text)
                    aufgabe_text = self.aufgabe.copy()
                    aufgabe_text.append("Weiter mit der Leer-Taste.")
                    self.aufgabe_text = AttributedText(
                        x=gd.scale(20), y=gd.scale(20),
                        width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)
                    self.manager.add(self.aufgabe_text)
                    self.manager.trigger_render()

                    # Mit dem Ton schon mal anzeigen, ob die Karten passen oder nicht
                    if self.first_card.key == self.second_card.key:
                        arcade.play_sound(self.ok_sound, volume=gd.get_volume() / 100.0)
                    else:
                        arcade.play_sound(self.lose_sound, volume=gd.get_volume() / 100.0)

                # Die Karte wurde gefunden, also können wir die Schleife verlassen
                break

    def on_key_press(self, key, modifiers):
        """
        Callback, wenn eine Taste gedrückt wurde
        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Taste auch an Basisklasse melden
        super().on_key_press(key, modifiers)

        # Leertaste gedrückt?
        if key == arcade.key.SPACE or key == arcade.key.NUM_SPACE:

            # Wenn zwei Karten gedreht sind, dann Anzeige aufräumen
            if self.first_card is not None and self.second_card is not None:

                # Aufgabentext anpassen
                self.manager.remove(self.aufgabe_text)
                aufgabe_text = self.aufgabe.copy()
                self.aufgabe_text = AttributedText(
                    x=gd.scale(20), y=gd.scale(20),
                    width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)
                self.manager.add(self.aufgabe_text)

                # Die Karten passen zusammen, also aus der Anzeige entfernen
                if self.first_card.key == self.second_card.key:

                    # Buttons von der Anzeige entfernen
                    self.manager.remove(self.first_card.button)
                    self.manager.remove(self.second_card.button)

                    # Karten aus der Liste der Karten entfernen
                    self.karten.remove(self.first_card)
                    self.karten.remove(self.second_card)

                    # Wenn alle Kartenpaare gefunden wurden, dann kann der Spieler die View verlassen
                    if len(self.karten) == 0:
                        self.correct = True

                        # Aufgabentext anpassen
                        self.manager.remove(self.aufgabe_text)
                        aufgabe_text = self.aufgabe.copy()
                        aufgabe_text.append("Mit der Esc-Taste geht es zum Spiel zurück.")
                        self.aufgabe_text = AttributedText(
                            x=gd.scale(20), y=gd.scale(20),
                            width=gd.scale(400), height=gd.scale(300), text=aufgabe_text)
                        self.manager.add(self.aufgabe_text)

                else:
                    # Die Karten passen nicht, "zur Strafe" muss der Spieler etwas warten
                    time.sleep(2.0)

                    # Beide Karten wieder "umdrehen", also auf den Buttons die Rückseite anzeigen
                    mypath = gd.get_abs_path("res/images")
                    avatar_path = mypath + "/back.png"
                    te = arcade.load_texture(avatar_path, x=0, y=0, width=200, height=200)
                    self.first_card.button.texture = te
                    self.second_card.button.texture = te

                # Die gemerkten Karten zurücksetzen, damit das nächste Paar gesucht werden kann
                self.first_card = None
                self.second_card = None
