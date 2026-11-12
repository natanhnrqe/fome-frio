
import json
from pathlib import Path

from models.personagem import Personagem
from models.pista import Pista


from models.dialogos import Dialogo, EscolhaDialogo


def carregar_dialogos() -> dict[str, Dialogo]:
    dados = carregar_json("dialogos.json")

    dialogos = {}

    for dado in dados:
        escolhas = [
            EscolhaDialogo(
                texto=escolha["texto"],
                resposta=escolha["resposta"],
                proxima_etapa=escolha.get("proxima_etapa"),
                pista_id=escolha.get("pista_id")
            )
            for escolha in dado["escolhas"]
        ]

        dialogo = Dialogo(
            id=dado["id"],
            personagem_id=dado.get("personagem_id"),
            falante=dado["falante"],
            fala=dado["fala"],
            escolhas=escolhas
        )

        dialogos[dialogo.id] = dialogo

    return dialogos



def carregar_json(nome_arquivo: str):
    caminho = Path(__file__).with_name(nome_arquivo)

    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def carregar_personagens() -> dict[str, Personagem]:
    dados = carregar_json("personagens.json")

    personagens = {}

    for dado in dados:
        personagem = Personagem(
            id=dado["id"],
            nome=dado["nome"],
            cargo=dado["cargo"],
            nacionalidade=dado["nacionalidade"],
            arma=dado["arma"]
        )

        personagens[personagem.id] = personagem

    return personagens



def carregar_pistas() -> dict[str, Pista]:
    dados = carregar_json("pistas.json")
    pistas = {}

    for dado in dados:
        pista = Pista(
            id=dado["id"],
            simbolo=dado["simbolo"],
            descricao=dado["descricao"],
            expressao=dado["expressao"],
            significado=dado.get("significado", dado["descricao"])
        )

        pistas[pista.id] = pista

    return pistas
