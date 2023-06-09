
import arcade
import arcade.gui
from arcade import load_texture

from src.views.q_02 import Q_02

INFO_TEXT = ("Super die Basics zum Strom kennst du nun schon, aber das ist lange noch nicht alles!\n\n"
             "Eine sehr wichtige Grösse, wenn man sich mit Strom beschäftigt, ist die Stromstärke I. "
             "Sie kann an einer bestimmten Stelle in z.B. Kabeln gemessen werden.\n\n"
             "Die mittlere, d.h. die durchschnittliche Stromstärke gibt das Verhältnis der dort "
             "vorbeifliessenden Ladungsmenge Q an, die Anzahl der Elektronen, und der Zeitspanne t, "
             "in der gemessen wurde. Daraus ergibt sich die Formel:\n\n\n"
             "Stromstärke = Ladung / Zeit\n\n"
             "I = Q / t\n\n"
             "     Q \n"
             "I = ---\n"
             "     t \n\n"
             )


class V_02(arcade.View):
    """
    Klasse für die View mit Theorie oder Aufgabe
    """

    def __init__(self):
        """
        Konstruktor
        """

        super().__init__()

        # UIManager braucht es für arcade
        self.manager = arcade.gui.UIManager()

    def setup(self):
        """
        View initialisieren.
        Es werden die Daten für view_name angezeigt.
        """

        # Vertikales Layout für den Text erstellen
        v_box = arcade.gui.UIBoxLayout()

        ui_text_label = arcade.gui.UITextArea(text=INFO_TEXT,
                                              width=800,
                                              height=500,
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

        v_box.add(w.with_space_around(bottom=0))

        # Button
        quiz_button = arcade.gui.UIFlatButton(text="Weiter", width=250)
        v_box.add(quiz_button.with_space_around(top=20, bottom=20))
        quiz_button.on_click = self.on_click_quiz

        # Widget, das als Anker für die Buttons dient, damit diese zentriert angezeigt werden.
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=v_box
            )
        )

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

    def on_click_quiz(self, event):
        """
        Weiter
        :param event:
        """

        v = Q_02()
        v.setup()
        self.window.show_view(v)

