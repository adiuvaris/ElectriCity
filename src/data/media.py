class Media:
    """
    Klasse für die Anzeige eines Bildes oder der Ausgabe einer Tondatei
    Typ kann "image" oder "audio" sein
    """

    def __init__(self, typ):
        """
        Konstruktor
        """

        # Member definieren
        self.filename = ""
        self.frames = 0
        self.title = ""
        self.description = ""
        self.typ = typ
        self.illustration = ""
