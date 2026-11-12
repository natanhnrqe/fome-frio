
class DistribuidorPistas:

    DISTRIBUICAO = {
        "hipoteses_assassino": "sala_capitao",
        "evidencia_morte_secundaria": "local_vitima_secundaria",
        "regra_morte_secundaria": "enfermaria"
    }

    def distribuir(self, pistas, caso, locais):

        locais_por_id = {
            local.id: local
            for local in locais
        }

        local_por_personagem = {}

        for local in locais:
            for personagem_id in local.personagens:
                local_por_personagem[personagem_id] = local.id

        local_secundario = local_por_personagem.get(
            caso.vitima_secundaria_id
        )

        if local_secundario is None:
            raise ValueError(
                "Não foi encontrado um local para a vítima secundária."
            )

        for pista in pistas:

            destino = self.DISTRIBUICAO.get(pista.id)

            if destino is None:
                # Pistas de diálogo preservam seu personagem responsável.
                pista.local_id = None
                continue

            if destino == "local_vitima_secundaria":
                local_id = local_secundario
            else:
                local_id = destino

            if local_id not in locais_por_id:
                raise ValueError(
                    f"Local '{local_id}' não encontrado."
                )

            pista.local_id = local_id

        return pistas
