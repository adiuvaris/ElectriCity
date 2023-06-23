
class Singleton(type):
    """
    Klasse die bewirkt, dass abgeleitete Klassen nur eine Instanz haben können
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Erstellt die Instanz oder gibt die erstellte zurück, wenn die Instanz schon existiert.
        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
