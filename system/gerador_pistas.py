
import random

from models.pista import Pista


class GeradorPistas:

    CAUSAS_MORTE = {
        "ataque_de_urso": {
            "descricao": (
                "Foram encontradas marcas de garras e mordidas "
                "compatíveis com um ataque de urso."
            ),
            "regra": (
                "Se as lesões forem compatíveis com um ataque "
                "de urso, a morte pode ser atribuída ao animal."
            ),
            "conclusao": (
                "A vítima morreu em decorrência de um ataque de urso."
            )
        },
        "hipotermia": {
            "descricao": (
                "O corpo apresentava sinais de exposição "
                "prolongada ao frio."
            ),
            "regra": (
                "Se os sinais forem compatíveis com hipotermia fatal, "
                "a exposição ao frio explica a morte."
            ),
            "conclusao": "A vítima morreu de hipotermia."
        },
        "fome": {
            "descricao": (
                "Foram encontrados sinais de desnutrição severa."
            ),
            "regra": (
                "Se a desnutrição for severa e prolongada, "
                "ela pode explicar a morte por inanição."
            ),
            "conclusao": "A vítima morreu por inanição."
        },
        "acidente": {
            "descricao": (
                "Os ferimentos são compatíveis com uma queda acidental."
            ),
            "regra": (
                "Se os ferimentos forem compatíveis com uma queda fatal, "
                "o acidente pode explicar a morte."
            ),
            "conclusao": (
                "A vítima morreu em decorrência de um acidente."
            )
        }
    }

    def _gerar_distribuicao_testemunhas(self, suspeitos):
        testemunhas = suspeitos.copy()

        while True:
            random.shuffle(testemunhas)

            if all(
                suspeito_id != testemunha_id
                for suspeito_id, testemunha_id
                in zip(suspeitos, testemunhas)
            ):
                return dict(zip(suspeitos, testemunhas))

    def gerar(self, caso, personagens) -> list[Pista]:

        sobreviventes = [
            personagem_id
            for personagem_id in personagens
            if personagem_id not in caso.vitimas_ids
        ]

        if len(sobreviventes) != 6:
            raise ValueError(
                "A investigação exige exatamente seis sobreviventes."
            )

        suspeitos_inocentes = [
            personagem_id
            for personagem_id in sobreviventes
            if personagem_id != caso.assassino_id
        ]

        testemunhas_por_suspeito = (
            self._gerar_distribuicao_testemunhas(
                suspeitos_inocentes
            )
        )

        # Hipótese inicial: um dos seis sobreviventes é o assassino.
        expressao_inicial = " | ".join(
            f"K_{personagem_id}"
            for personagem_id in sobreviventes
        )

        simbolos = [
            f"K_{personagem_id}"
            for personagem_id in sobreviventes
        ]

        pistas = [
            Pista(
                id="hipoteses_assassino",
                simbolo=" ∨ ".join(simbolos),
                descricao=(
                    "A investigação confirma que o autor do assassinato "
                    "está entre os seis tripulantes que sobreviveram."
                ),
                expressao=expressao_inicial,
                significado=(
                    "Pelo menos um dos seis sobreviventes é o assassino. "
                    "A investigação considera que existe exatamente "
                    "um responsável pelo crime."
                ),
                local_id="sala_capitao"
            )
        ]

        # Evidências que eliminam os cinco suspeitos inocentes.
        for suspeito_id in suspeitos_inocentes:

            suspeito = personagens[suspeito_id]

            testemunha_id = testemunhas_por_suspeito[
                suspeito_id
            ]

            testemunha = personagens[testemunha_id]

            pistas.append(
                Pista(
                    id=f"alibi_{suspeito_id}",
                    simbolo=f"¬K_{suspeito_id}",
                    descricao=(
                        f"Os registros de serviço e o depoimento de "
                        f"{testemunha.nome} confirmam que "
                        f"{suspeito.nome} estava em outro compartimento "
                        "durante todo o intervalo em que ocorreu "
                        "o assassinato."
                    ),
                    expressao=f"~K_{suspeito_id}",
                    significado=(
                        f"Se {suspeito.nome} estava comprovadamente "
                        "em outro compartimento durante todo o período "
                        "do crime, então não poderia ser o assassino."
                    ),
                    personagem_id=testemunha_id
                )
            )

        # Evidências da segunda morte.
        causa = self.CAUSAS_MORTE[
            caso.causa_morte_secundaria
        ]

        pistas.extend([
            Pista(
                id="evidencia_morte_secundaria",
                simbolo="T",
                descricao=(
                    f"{causa['descricao']} "
                    f"A vítima era "
                    f"{personagens[caso.vitima_secundaria_id].nome}."
                ),
                expressao="T",
                significado=(
                    "O corpo apresenta evidências compatíveis "
                    "com a causa investigada."
                )
            ),
            Pista(
                id="regra_morte_secundaria",
                simbolo="T >> U",
                descricao=causa["regra"],
                expressao="T >> U",
                significado=(
                    "Se as evidências forem compatíveis com a causa, "
                    "essa causa explica a morte."
                )
            )
        ])

        return pistas

    def obter_conclusoes(self, caso, personagens):

        assassino = personagens[caso.assassino_id]

        vitima_assassinato = personagens[
            caso.vitima_assassinato_id
        ]

        vitima_secundaria = personagens[
            caso.vitima_secundaria_id
        ]

        causa = self.CAUSAS_MORTE[
            caso.causa_morte_secundaria
        ]

        return {
            "assassinato": {
                "expressao": f"K_{assassino.id}",
                "texto": (
                    f"{assassino.nome} foi responsável pelo "
                    f"assassinato de {vitima_assassinato.nome}."
                )
            },
            "morte_secundaria": {
                "expressao": "U",
                "texto": (
                    f"{vitima_secundaria.nome}: "
                    f"{causa['conclusao']}"
                )
            }
        }
