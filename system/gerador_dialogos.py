
from models.dialogos import Dialogo, EscolhaDialogo


class GeradorDialogos:

    def gerar(self, caso, personagens, pistas):

        dialogos = {}

        personagens_vivos = [
            personagem_id
            for personagem_id in personagens
            if personagem_id not in caso.vitimas_ids
        ]

        # Identifica qual personagem deve revelar cada pista.
        pistas_por_personagem = {}

        for pista in pistas.values():
            if pista.personagem_id is not None:
                pistas_por_personagem[pista.personagem_id] = pista.id

        for personagem_id in personagens_vivos:

            personagem = personagens[personagem_id]

            inicio_id = f"{personagem_id}_inicio"
            perguntas_id = f"{personagem_id}_perguntas"

            pista_id = pistas_por_personagem.get(personagem_id)

            if pista_id is not None:

                pista = pistas[pista_id]

                resposta = (
                    "Tenho informações importantes para a investigação: "
                    f"{pista.descricao}"
                )

                texto_escolha = (
                    "Perguntar sobre o paradeiro dos tripulantes "
                    "durante o assassinato."
                )

            else:

                resposta = (
                    "Não tenho informações concretas que possam "
                    "ajudar na investigação."
                )

                texto_escolha = (
                    "Perguntar se sabe de algo sobre o assassinato."
                )

            dialogos[inicio_id] = Dialogo(
                id=inicio_id,
                personagem_id=personagem_id,
                falante=personagem.nome,
                fala=(
                    f"Sou {personagem.nome}, "
                    f"{personagem.cargo.lower()} da tripulação. "
                    "O que deseja saber?"
                ),
                escolhas=[
                    EscolhaDialogo(
                        texto="Perguntar sobre a situação da ilha.",
                        resposta=(
                            "A situação está cada vez mais complicada. "
                            "Precisamos descobrir o que aconteceu."
                        ),
                        proxima_etapa=perguntas_id
                    )
                ]
            )

            dialogos[perguntas_id] = Dialogo(
                id=perguntas_id,
                personagem_id=personagem_id,
                falante=personagem.nome,
                fala="O que gostaria de saber?",
                escolhas=[
                    EscolhaDialogo(
                        texto=texto_escolha,
                        resposta=resposta,
                        proxima_etapa=None,
                        pista_id=pista_id
                    )
                ]
            )

        return dialogos
