
from data.carregador import (
    carregar_dialogos,
    carregar_pistas
)

from system.sistema_dialogo import SistemaDialogo
from system.diario import DiarioDeBordo
from system.controlador_investigacao import ControladorInvestigacao


dialogos = carregar_dialogos()
pistas = carregar_pistas()

sistema_dialogo = SistemaDialogo(dialogos)
diario = DiarioDeBordo()

investigacao = ControladorInvestigacao(
    sistema_dialogo=sistema_dialogo,
    diario=diario,
    pistas=pistas
)

investigacao.iniciar_conversa("alizandro_inicio")

while not investigacao.conversa_encerrada():
    dialogo = investigacao.obter_dialogo_atual()

    print(f"\n{dialogo.falante.upper()}: {dialogo.fala}")

    for indice, escolha in enumerate(investigacao.obter_escolhas()):
        print(f"{indice + 1}. {escolha.texto}")

    try:
        indice = int(input("\nEscolha: ")) - 1

        resultado = investigacao.selecionar_escolha(indice)

        print(f"\nResposta: {resultado['escolha'].resposta}")

        if resultado["pista"] is not None:
            if resultado["pista_nova"]:
                print("\n*** NOVA PISTA DESCOBERTA ***")
                print(resultado["pista"].simbolo)
                print(resultado["pista"].descricao)
            else:
                print("\nVocê já possui essa pista no diário.")

    except (ValueError, IndexError) as erro:
        print(f"\nErro: {erro}")

print("\nInvestigação encerrada.")

print("\n===== DIÁRIO DE BORDO =====")

for pista in investigacao.obter_pistas_diario():
    print(f"{pista.simbolo}: {pista.descricao}")

print("\nTotal de pistas:", investigacao.quantidade_pistas())
