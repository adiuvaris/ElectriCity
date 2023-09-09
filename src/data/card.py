class Card:
    """
    Klasse für eine Karte im Memory- oder Puzzle Spiel
    """

    def __init__(self):
        """
        Konstruktor
        """

        # Member definieren
        self.bild = ""
        self.key = ""
        self.button = None
        self.position = ()
        self.sound = None
