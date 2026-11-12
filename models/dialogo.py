
class Dialogo:
    def __init__(
        self,
        id: str,
        fala: str,
        escolhas: list[dict]
    ):
        self.id = id
        self.fala = fala
        self.escolhas = escolhas
