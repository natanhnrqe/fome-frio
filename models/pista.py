
class Pista:
    def __init__(
        self,
        id: str,
        simbolo: str,
        descricao: str,
        expressao: str,
        significado: str,
        local_id: str | None = None,
        personagem_id: str | None = None
    ):
        self.id = id
        self.simbolo = simbolo
        self.descricao = descricao
        self.expressao = expressao
        self.significado = significado
        self.local_id = local_id
        self.personagem_id = personagem_id

    def __repr__(self):
        return f"Pista({self.simbolo}: {self.descricao})"
