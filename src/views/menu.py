
import arcade
import arcade.gui


class Menu(arcade.View):
    """
    Klasse für die View mit dem Menü
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        # Vertikales Layout für die Schalter erstellen
        self.v_box = arcade.gui.UIBoxLayout()

        # Button
        resume_button = arcade.gui.UIFlatButton(text="Zurück zum Spiel", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))
        resume_button.on_click = self.on_click_resume

        # Button
        settings_button = arcade.gui.UIFlatButton(text="Einstellungen", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        settings_button.on_click = self.on_click_settings

        # Button
        new_game_button = arcade.gui.UIFlatButton(text="Neues Spiel", width=200)
        self.v_box.add(new_game_button.with_space_around(bottom=20))
        new_game_button.on_click = self.on_click_new_game

        # Button
        quit_button = arcade.gui.UIFlatButton(text="Programm beenden", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit

        # Widget, das als Anker für die Buttons dient, damit diese zentriert angezeigt werden.
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

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

        # Der UI-Manager muss deaktiviet werden
        self.manager.disable()

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

        self.clear()
        self.manager.draw()

    def on_click_resume(self, event):
        """
        Klick handler wenn "Zurück zum Spiel" angeklickt wurde
        :param event:
        """

        self.window.show_view(self.window.views["game"])

    def on_click_settings(self, event):
        """
        Klick handler wenn "Einstellungen" angeklickt wurde
        :param event:
        """

        self.window.show_view(self.window.views["settings"])

    def on_click_new_game(self, event):
        """
        Klick handler wenn "Neues Spiel" angeklickt wurde
        :param event:
        """

        # Game View neu initialisieren und dann anzeigen
        self.window.views["game"].setup()
        self.window.show_view(self.window.views["game"])

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
            self.window.show_view(self.window.views["game"])
