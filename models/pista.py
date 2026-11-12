
class Pista:
    def __init__(
        self,
        id: str,
        simbolo: str,
        descricao: str,
        expressao: str
    ):
        self.id = id
        self.simbolo = simbolo
        self.descricao = descricao
        self.expressao = expressao

    def __repr__(self):
        return f"Pista({self.simbolo}: {self.descricao})"
