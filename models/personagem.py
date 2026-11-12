
class Personagem:
    def __init__(
        self,
        id: str,
        nome: str,
        cargo: str,
        nacionalidade: str,
        arma: str
    ):
        self.id = id
        self.nome = nome
        self.cargo = cargo
        self.nacionalidade = nacionalidade
        self.arma = arma

    def __repr__(self):
        return f"Personagem(nome='{self.nome}', cargo='{self.cargo}')"
