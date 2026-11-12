
import random

from models.caso import Caso


class GeradorCaso:
    CAUSAS_MORTE_SECUNDARIA = [
        "ataque_de_urso",
        "hipotermia",
        "fome",
        "acidente"
    ]

    def gerar(self, personagens: dict) -> Caso:
        ids_personagens = list(personagens.keys())

        if len(ids_personagens) < 3:
            raise ValueError(
                "São necessários pelo menos três personagens."
            )

        assassino_id = random.choice(ids_personagens)

        candidatos = [
            personagem_id
            for personagem_id in ids_personagens
            if personagem_id != assassino_id
        ]

        vitimas_ids = random.sample(candidatos, 2)

        vitima_assassinato_id = random.choice(vitimas_ids)

        vitima_secundaria_id = next(
            personagem_id
            for personagem_id in vitimas_ids
            if personagem_id != vitima_assassinato_id
        )

        causa_secundaria = random.choice(
            self.CAUSAS_MORTE_SECUNDARIA
        )

        return Caso(
            assassino_id=assassino_id,
            vitimas_ids=vitimas_ids,
            vitima_assassinato_id=vitima_assassinato_id,
            vitima_secundaria_id=vitima_secundaria_id,
            causa_morte_secundaria=causa_secundaria
        )
