
import arcade
import arcade.gui
from arcade import load_texture

INFO_TEXT = ("In der Garage steht ein 12V-Akku. Er wird 9,0h lang mit der Ladestromstärke von 5.0A geladen."
             "Welche Ladung (in Ah) hat der Akku beim Ladevorgang aufgenommen?\n\n"
             "Gib dein Resultat in das Eingabefeld ein (nur die Zahl).")


class Q_02(arcade.View):
    """
    Quiz
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

        # Vertikales Layout für die Schalter erstellen
        v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text=INFO_TEXT,
                                              width=800,
                                              height=100,
                                              text_color=[0, 0, 0],
                                              font_size=14,
                                              font_name="Arial")

        bg_tex = load_texture(":textures:grey_panel.png")

        w = self.manager.add(
            arcade.gui.UITexturePane(
                ui_text_label.with_space_around(left=20, right=20),
                tex=bg_tex,
                padding=(20, 20, 20, 20)
            )
        )

        v_box.add(w.with_space_around(bottom=20))

        # Input

        self.input_text = arcade.gui.UIInputText(x=340, y=110, width=200, height=20, text="")

        border = arcade.gui.UIBorder(self.input_text)

        v_box.add(border)

        # Widget, das als Anker für die Buttons dient, damit diese zentriert angezeigt werden.
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=v_box
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

        # Der UI-Manager muss deaktiviert werden
        self.manager.disable()

    def on_draw(self):
        """
        Zeichnet die View. Wird von arcade aufgerufen.
        """

        self.clear()
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        """
        Wird von arcade aufgerufen, wenn eine Taste gedrückt wurde.

        :param key: Taste
        :param modifiers: Shift, Alt etc.
        """

        # Escape geht zurück zum Spiel

        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["game"])

        if key == arcade.key.ENTER:
            eingabe = self.input_text.text.strip()

            if eingabe == "45":
                self.show_message_box("Das ist richtig.")

            else:
                self.show_message_box("Das ist leider falsch.")

    def show_message_box(self, text):
        message_box = arcade.gui.UIMessageBox(
            width=500,
            height=300,
            message_text=text,
            callback=self.on_message_box_close,
            buttons=["Ok"]
        )

        self.manager.add(message_box)

    def on_message_box_close(self, button_text):
        self.window.show_view(self.window.views["game"])

