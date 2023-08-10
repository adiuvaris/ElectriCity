import math

# Alle gültigen math Funktionen von Python in eine Liste füllen
ALLOWED_NAMES = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}


class Term:
    """
    Klasse, die einen Term mit Variablen berechnen kann.
    Es dürfen mathematische Funktion von Python verwendet werden z.B. sqrt für Wurzel
    Variablen müssen in den Member variables eingetragen werden (dict {"Var-Name": Zahlwert, ...}).
    """

    def __init__(self):
        """
        Konstruktor
        """

        # Member definieren
        self.variables = {}

    def calc(self, term):
        """
        Wert des Terms mit den vorgängig definierten Variablen-Werten berechnen
        :param term: String mit der Formel
        :return: berechneter Wert
        """

        # Prüfen, ob die Formel i.O. ist
        code = compile(term, "<string>", "eval")

        # Zur Sicherheit prüfen, ob alle verwendeten Variablen und Funktionen erlaubt sind.
        for name in code.co_names:
            if name not in ALLOWED_NAMES and name not in self.variables:
                raise NameError(f"Die Verwendung von '{name}' ist nicht erlaubt.")

        # Wert berechnen und zurückgeben
        val = eval(term, self.variables, ALLOWED_NAMES)
        return val
