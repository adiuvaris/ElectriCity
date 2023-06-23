import math

# Alle gültigen math Funktionen in eine Liste füllen
ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}


class Term(object):
    """
    Klasse, die einen Term mit Variablen berechnen kann.
    Es dürfen mathematische Funktion von Python verwendet werden z.B. sqrt für Wurzel
    """

    def __init__(self):
        self.variables = {}

    def calc(self, term):
        """
        Wert des Terms mit den vorgängig definierten Variablen-Werten berechnen
        :param term: String mit der Formel
        :return: berechneter Wert
        """

        # Prüfen, ob die Formel i.O. ist
        code = compile(term, "<string>", "eval")

        for name in code.co_names:
            if name not in ALLOWED_NAMES and name not in self.variables:
                raise NameError(f"The use of '{name}' is not allowed")

        # Wert berechnen und zurückgeben
        val = eval(term, self.variables, ALLOWED_NAMES)
        return val

    def add_variable(self, name, value):
        """
        Variable und deren Wert hinzufügen
        :param name: String mit dem Variablen-Namen
        :param value: int oder float des Variablen-Werts
        """
        self.variables[name] = value
