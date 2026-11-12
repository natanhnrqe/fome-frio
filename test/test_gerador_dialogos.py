
from data.carregador import carregar_personagens

from system.gerador_caso import GeradorCaso
from system.gerador_dialogos import GeradorDialogos
from system.sistema_dialogo import SistemaDialogo


personagens = carregar_personagens()

caso = GeradorCaso().gerar(personagens)

gerador = GeradorDialogos()
dialogos = gerador.gerar(caso, personagens)

# Cada personagem vivo deve ter dois nós de diálogo.
personagens_vivas = [
    personagem_id
    for personagem_id in personagens
    if personagem_id not in caso.vitimas_ids
]

assert len(dialogos) == len(personagens_vivas) * 2

for personagem_id in personagens_vivas:
    inicio_id = f"{personagem_id}_inicio"
    perguntas_id = f"{personagem_id}_perguntas"

    assert inicio_id in dialogos
    assert perguntas_id in dialogos

    assert dialogos[inicio_id].personagem_id == personagem_id
    assert dialogos[perguntas_id].personagem_id == personagem_id

# Testa o fluxo de uma conversa.
personagem_teste = personagens_vivas[0]
sistema = SistemaDialogo(dialogos)

sistema.iniciar(f"{personagem_teste}_inicio")

assert not sistema.esta_encerrado()

escolha = sistema.selecionar_escolha(0)
assert escolha.proxima_etapa == f"{personagem_teste}_perguntas"

escolha = sistema.selecionar_escolha(0)
assert escolha.proxima_etapa is None
assert sistema.esta_encerrado()

# As vítimas não podem ter diálogos.
for vitima_id in caso.vitimas_ids:
    assert f"{vitima_id}_inicio" not in dialogos
    assert f"{vitima_id}_perguntas" not in dialogos

print("Assassino:", personagens[caso.assassino_id].nome)
print("Vítimas:", [
    personagens[id].nome for id in caso.vitimas_ids
])
print("Personagens com diálogos:", len(personagens_vivas))
print("Todos os testes passaram!")
