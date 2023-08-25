class Labyrinth:
    """
    Klasse für eine Aufgabe im Labyrinth
    """

    def __init__(self, book_nr, room_nr, correct, wrong):
        """
        Konstruktor
        """

        # Member definieren
        self.book_nr = book_nr
        self.room_nr = room_nr
        self.correct = correct
        self.wrong = wrong
