import arcade
import arcade.gui

import src.const as const
from src.data.game import gd
from src.views.setting_view import SettingView
from src.views.book_view import BookView


class MenuView(arcade.View):
    """
    Klasse für die View mit dem Menü
    """

    def __init__(self):
        """
        Konstruktor
        """

        # Konstruktor der Basisklasse aufrufen
        super().__init__()

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()
        self.create_ui()

    def setup(self):
        """
        View initialisieren.
        Macht zurzeit noch nichts
        """

        pass

    def on_show_view(self):
        """
        Wird von arcade aufgerufen, wenn die View sichtbar wird
        """

        self.manager.enable()
        arcade.set_background_color(arcade.color.ALMOND)

    def on_hide_view(self):
        """
        Wird von arcade aufgerufen, wenn die View unsichtbar wird
        """

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

        self.clear()
        self.manager.draw()

    def on_click_resume(self, event):
        """
        Klick-handler, wenn "Zurück zum Spiel" angeklickt wurde
        :param event:
        """

        self.window.show_view(self.window.game_view)

    def on_click_settings(self, event):
        """
        Klick-handler, wenn "Einstellungen" angeklickt wurde
        :param event:
        """

        settings = SettingView(self)
        self.window.show_view(settings)

    def on_click_final(self, event):
        v = BookView("00", "00")
        v.setup()
        self.window.show_view(v)

        pass

    def on_click_new_game(self, event):
        """
        Klick-handler, wenn "Neues Spiel" angeklickt wurde
        :param event:
        """

        # Start View erzeugen und starten
        self.window.start_view.setup()
        self.window.show_view(self.window.start_view)

    def on_click_quit(self, event):
        """
        Klick handler wenn "Programm beenden" angeklickt wurde
        :param event:
        """

        self.window.close()

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zum Spiel
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.game_view)

    def on_resize(self, width, height):
        """
        Wird von arcade aufgerufen, wenn die Fenstergrösse ändert.

        :param width: neue Breite
        :param height: neue Höhe
        """
        self.create_ui()

    def create_ui(self):
        """
        User-Interface erstellen - ein Button pro Memory-Karte
        """

        # Zuerst mal Elemente löschen
        for widget in self.manager.walk_widgets():
            self.manager.remove(widget)
        self.manager.clear()

        style = {"font_size": gd.scale(const.FONT_SIZE), "bg_color": (100, 100, 100)}

        # Vertikales Layout für die Schalter erstellen
        v_box = arcade.gui.UIBoxLayout()

        # Button
        resume_button = arcade.gui.UIFlatButton(text="Zurück zum Spiel", width=gd.scale(290), height=gd.scale(40), style=style)
        v_box.add(resume_button.with_space_around(bottom=gd.scale(40)))
        resume_button.on_click = self.on_click_resume

        # Button
        settings_button = arcade.gui.UIFlatButton(text="Einstellungen", width=gd.scale(290), height=gd.scale(40), style=style)
        v_box.add(settings_button.with_space_around(bottom=gd.scale(40)))
        settings_button.on_click = self.on_click_settings

        # Der Hinweis für die Abschlussprüfung wurde angezeigt, also auch den entsprechenden Button anzeigen
        if gd.get_final():

            # Button
            quit_button = arcade.gui.UIFlatButton(text="Abschlussprüfung", width=gd.scale(290), height=gd.scale(40), style=style)
            v_box.add(quit_button.with_space_around(bottom=gd.scale(40)))
            quit_button.on_click = self.on_click_final

        # Button
        new_game_button = arcade.gui.UIFlatButton(text="Neues Spiel", width=gd.scale(290), height=gd.scale(40), style=style)
        v_box.add(new_game_button.with_space_around(bottom=gd.scale(40)))
        new_game_button.on_click = self.on_click_new_game

        # Button
        quit_button = arcade.gui.UIFlatButton(text="Spiel beenden", width=gd.scale(290), height=gd.scale(40), style=style)
        v_box.add(quit_button.with_space_around(bottom=gd.scale(40)))
        quit_button.on_click = self.on_click_quit

        # Widget, das als Anker für die Buttons dient, damit diese zentriert angezeigt werden.
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=v_box
            )
        )

        # Titeltext oben in der Mitte
        titel = arcade.gui.UILabel(x=0, y=gd.scale(670),
                                   width=self.window.width, height=gd.scale(30),
                                   text="Menü",
                                   text_color=[0, 0, 0],
                                   bold=True,
                                   align="center",
                                   font_size=gd.scale(const.FONT_SIZE_H1),
                                   multiline=False)
        self.manager.add(titel.with_border())

        self.manager.trigger_render()
