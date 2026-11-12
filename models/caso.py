
from dataclasses import dataclass


@dataclass
class Caso:
    assassino_id: str
    vitimas_ids: list[str]
    vitima_assassinato_id: str
    vitima_secundaria_id: str
    causa_morte_secundaria: str

    def __post_init__(self):
        if len(self.vitimas_ids) != 2:
            raise ValueError("O caso deve possuir exatamente duas vítimas.")

        if len(self.vitimas_ids) != len(set(self.vitimas_ids)):
            raise ValueError("As vítimas devem ser personagens diferentes.")

        if self.assassino_id in self.vitimas_ids:
            raise ValueError("O assassino não pode ser uma vítima.")

        if self.vitima_assassinato_id not in self.vitimas_ids:
            raise ValueError("A vítima do assassinato não pertence ao caso.")

        if self.vitima_secundaria_id not in self.vitimas_ids:
            raise ValueError("A vítima secundária não pertence ao caso.")

        if self.vitima_assassinato_id == self.vitima_secundaria_id:
            raise ValueError("As vítimas devem ser diferentes.")
