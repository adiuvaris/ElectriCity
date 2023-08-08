
from src.data.frage import Frage
from src.data.memory import Memory
from src.data.puzzle import Puzzle
from src.data.wortsuche import Wortsuche


def create_task(aufgabe: dict):
    """
    Eine Aufgabe erstellen je nach Art der Aufgabe
    """

    if "Art" in aufgabe:
        art = aufgabe["Art"]

        if art == "Frage":
            frage = Frage(aufgabe)
            return frage

        if art == "Memory":
            memory = Memory(aufgabe)
            return memory

        if art == "Puzzle":
            puzzle = Puzzle(aufgabe)
            return puzzle

        if art == "Wortsuche":
            wortsuche = Wortsuche(aufgabe)
            return wortsuche
