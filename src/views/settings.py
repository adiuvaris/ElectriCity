
import arcade


class Settings(arcade.View):
    """
    Klasse für die View mit den Einstellungen - macht zurzeit noch nichts
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

        arcade.start_render()
        arcade.draw_text(
            "Settings",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
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

        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zum Menü
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["menu"])
