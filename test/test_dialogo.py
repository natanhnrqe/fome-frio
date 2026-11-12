
from data.carregador import carregar_dialogos
from system.sistema_dialogo import SistemaDialogo


dialogos = carregar_dialogos()
sistema = SistemaDialogo(dialogos)

sistema.iniciar("alizandro_inicio")

while not sistema.esta_encerrado():
    dialogo = sistema.obter_dialogo_atual()

    print(f"\n{dialogo.falante.upper()}: {dialogo.fala}")

    for indice, escolha in enumerate(dialogo.escolhas):
        print(f"{indice + 1}. {escolha.texto}")

    indice = int(input("\nEscolha: ")) - 1

    try:
        escolha = sistema.selecionar_escolha(indice)
        print(f"\nResposta: {escolha.resposta}")

        if escolha.pista_id:
            print(f"Pista desbloqueada: {escolha.pista_id}")

    except (IndexError, ValueError) as erro:
        print("Erro:", erro)

print("\nConversa encerrada.")
