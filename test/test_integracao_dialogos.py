
from data.carregador import carregar_personagens
from data.locais import carregar_locais

from system.gerador_caso import GeradorCaso
from system.gerador_pistas import GeradorPistas
from system.gerador_dialogos import GeradorDialogos
from system.distribuidor_pistas import DistribuidorPistas

from system.diario import DiarioDeBordo
from system.sistema_dialogo import SistemaDialogo
from system.controlador_investigacao import ControladorInvestigacao


personagens = carregar_personagens()
locais = carregar_locais()

caso = GeradorCaso().gerar(personagens)

pistas_lista = GeradorPistas().gerar(caso, personagens)

pistas = {
    pista.id: pista
    for pista in pistas_lista
}

DistribuidorPistas().distribuir(
    pistas_lista,
    caso,
    locais
)

dialogos = GeradorDialogos().gerar(
    caso,
    personagens,
    pistas
)

diario = DiarioDeBordo()
sistema_dialogo = SistemaDialogo(dialogos)

controlador = ControladorInvestigacao(
    sistema_dialogo,
    diario,
    pistas
)

# Procura um personagem que tenha uma pista.
personagem_com_pista = None

for personagem_id in personagens:
    if personagem_id in caso.vitimas_ids:
        continue

    dialogo = dialogos[f"{personagem_id}_perguntas"]

    if dialogo.escolhas[0].pista_id is not None:
        personagem_com_pista = personagem_id
        break

assert personagem_com_pista is not None

# Inicia a conversa.
controlador.iniciar_conversa(
    f"{personagem_com_pista}_inicio"
)

# Avança para a etapa das perguntas.
controlador.selecionar_escolha(0)

# Seleciona a resposta que revela a pista.
resultado = controlador.selecionar_escolha(0)

assert resultado["pista"] is not None
assert resultado["pista_nova"] is True

assert diario.quantidade_pistas() == 1

# Não deve registrar a mesma pista novamente.
assert diario.registrar_pista(resultado["pista"]) is False

print("Personagem:", personagens[personagem_com_pista].nome)
print("Pista descoberta:", resultado["pista"].simbolo)
print("Quantidade no diário:", diario.quantidade_pistas())

print("\nIntegração dos diálogos validada!")
