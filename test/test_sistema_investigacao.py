
from data.carregador import carregar_personagens
from data.locais import carregar_locais

from system.gerador_caso import GeradorCaso
from system.gerador_pistas import GeradorPistas
from system.distribuidor_pistas import DistribuidorPistas
from system.sistema_investigacao import SistemaInvestigacao
from system.diario import DiarioDeBordo
from scenes.mapa import Mapa


personagens = carregar_personagens()
locais = carregar_locais()

caso = GeradorCaso().gerar(personagens)

pistas = GeradorPistas().gerar(caso, personagens)

pistas = DistribuidorPistas().distribuir(
    pistas,
    caso,
    locais
)

mapa = Mapa(locais)
diario = DiarioDeBordo()

sistema = SistemaInvestigacao(
    mapa=mapa,
    diario=diario,
    pistas={pista.id: pista for pista in pistas}
)

total_descobertas = 0

for local in locais:
    mapa.acessar_local(local.id)

    resultado = sistema.investigar_local()

    novas = resultado["pistas_novas"]
    total_descobertas += len(novas)

    print(f"\nLocal: {local.nome}")

    if novas:
        for pista in novas:
            print(f"Nova pista: {pista.simbolo}")
            print(pista.descricao)
    else:
        print("Nenhuma pista encontrada.")

# Todas as seis pistas devem estar distribuídas.
assert total_descobertas == len(pistas)

# Investigar novamente não deve duplicar pistas.
resultado_repetido = sistema.investigar_local()
assert resultado_repetido["pistas_novas"] == []

assert diario.quantidade_pistas() == len(pistas)

print("\nTodas as pistas foram encontradas sem duplicação!")
