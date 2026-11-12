
from data.carregador import carregar_personagens
from data.locais import carregar_locais

from system.gerador_caso import GeradorCaso
from system.gerador_pistas import GeradorPistas
from system.distribuidor_pistas import DistribuidorPistas


personagens = carregar_personagens()
locais = carregar_locais()

gerador_caso = GeradorCaso()
gerador_pistas = GeradorPistas()
distribuidor = DistribuidorPistas()

caso = gerador_caso.gerar(personagens)

pistas = gerador_pistas.gerar(caso, personagens)

pistas_distribuidas = distribuidor.distribuir(
    pistas,
    caso,
    locais
)

print("\nDISTRIBUIÇÃO DAS PISTAS")

for pista in pistas_distribuidas:
    local = next(
        local for local in locais
        if local.id == pista.local_id
    )

    personagem = (
        personagens[pista.personagem_id].nome
        if pista.personagem_id
        else "Nenhum — evidência ambiental"
    )

    print(f"\nPista: {pista.id}")
    print(f"Local: {local.nome}")
    print(f"Personagem relacionado: {personagem}")

    assert pista.local_id is not None

print("\nTodas as pistas foram distribuídas!")
