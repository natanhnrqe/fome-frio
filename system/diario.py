
class DiarioDeBordo:
    def __init__(self):
        self.pistas = {}

    def registrar_pista(self, pista):
        if pista.id in self.pistas:
            return False

        self.pistas[pista.id] = pista
        return True

    def possui_pista(self, pista_id: str) -> bool:
        return pista_id in self.pistas

    def obter_pista(self, pista_id: str):
        return self.pistas.get(pista_id)

    def listar_pistas(self) -> list:
        return list(self.pistas.values())

    def listar_simbolos(self) -> list:
        return [
            pista.simbolo
            for pista in self.pistas.values()
        ]

    def quantidade_pistas(self) -> int:
        return len(self.pistas)

    def limpar(self):
        self.pistas.clear()
