class Wort:
    """
    Klasse für ein Wort in der Wortsuche
    """

    def __init__(self, wort):
        self.wort = wort
        self.start_pos = ()
        self.end_pos = ()
        self.start_found = False
        self.end_found = False
        self.positionen = []

