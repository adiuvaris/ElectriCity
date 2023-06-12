
import arcade
import arcade.gui
from src.views.v_01 import V_01

LOREM_IPSUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget pellentesque velit. "
    "Nam eu rhoncus nulla. Fusce ornare libero eget ex vulputate, vitae mattis orci eleifend. "
    "Donec quis volutpat arcu. Proin lacinia velit id imperdiet ultrices. Fusce porta magna leo, "
    "non maximus justo facilisis vel. Duis pretium sem ut eros scelerisque, a dignissim ante "
    "pellentesque. Cras rutrum aliquam fermentum. Donec id mollis mi.\n"
    "\n"
    "Nullam vitae nunc aliquet, lobortis purus eget, porttitor purus. Curabitur feugiat purus sit "
    "amet finibus accumsan. Proin varius, enim in pretium pulvinar, augue erat pellentesque ipsum, "
    "sit amet varius leo risus quis tellus. Donec posuere ligula risus, et scelerisque nibh cursus "
    "ac. Mauris feugiat tortor turpis, vitae imperdiet mi euismod aliquam. Fusce vel ligula volutpat, "
    "finibus sapien in, lacinia lorem. Proin tincidunt gravida nisl in pellentesque. Aenean sed "
    "arcu ipsum. Vivamus quam arcu, elementum nec auctor non, convallis non elit. Maecenas id "
    "scelerisque lectus. Vivamus eget sem tristique, dictum lorem eget, maximus leo. Mauris lorem "
    "tellus, molestie eu orci ut, porta aliquam est. Nullam lobortis tempor magna, egestas lacinia lectus.\n"
    "\n"
    "Nullam vitae nunc aliquet, lobortis purus eget, porttitor purus. Curabitur feugiat purus sit "
    "amet finibus accumsan. Proin varius, enim in pretium pulvinar, augue erat pellentesque ipsum, "
    "sit amet varius leo risus quis tellus. Donec posuere ligula risus, et scelerisque nibh cursus "
    "ac. Mauris feugiat tortor turpis, vitae imperdiet mi euismod aliquam. Fusce vel ligula volutpat, "
    "finibus sapien in, lacinia lorem. Proin tincidunt gravida nisl in pellentesque. Aenean sed "
    "arcu ipsum. Vivamus quam arcu, elementum nec auctor non, convallis non elit. Maecenas id "
    "scelerisque lectus. Vivamus eget sem tristique, dictum lorem eget, maximus leo. Mauris lorem "
    "tellus, molestie eu orci ut, porta aliquam est. Nullam lobortis tempor magna, egestas lacinia lectus.\n"
)


class View(arcade.View):
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

    def setup(self, view_name):
        """
        View initialisieren.
        Es werden die Daten für view_name angezeigt.
        """

        if view_name == "info_01":
            v = V_01()
            v.setup()

            self.window.show_view(v)

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

    def show_info_01(self):

        self.setup("")
        pass
