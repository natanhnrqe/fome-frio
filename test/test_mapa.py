
from scenes.mapa import Mapa
from data.locais import carregar_locais


locais = carregar_locais()
mapa = Mapa(locais)

# Inicia a exploração
mapa.iniciar_exploracao("enfermaria")

local = mapa.obter_local_atual()

print("Local atual:", local.nome)
print("Descrição:", local.descricao)
print("Personagens:", mapa.listar_personagens_no_local())

# Retorna ao mapa
mapa.voltar_ao_mapa()

# Acessa outro ambiente
mapa.acessar_local("farol")

print("Novo local:", mapa.obter_local_atual().nome)

# Lista locais visitados
for local in mapa.listar_locais_visitados():
    print(local.nome)
