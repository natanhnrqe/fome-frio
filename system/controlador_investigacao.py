
class ControladorInvestigacao:

    def __init__(self, sistema_dialogo, diario, pistas):
        self.sistema_dialogo = sistema_dialogo
        self.diario = diario
        self.pistas = pistas

    def iniciar_conversa(self, dialogo_id):
        self.sistema_dialogo.iniciar(dialogo_id)

    def obter_dialogo_atual(self):
        return self.sistema_dialogo.obter_dialogo_atual()

    def obter_escolhas(self):
        return self.sistema_dialogo.obter_escolhas()

    def selecionar_escolha(self, indice):
        escolhas = self.sistema_dialogo.obter_escolhas()

        if indice < 0 or indice >= len(escolhas):
            raise IndexError("Escolha inválida.")

        escolha_selecionada = escolhas[indice]
        pista_id = escolha_selecionada.pista_id

        if pista_id is not None and pista_id not in self.pistas:
            raise ValueError(
                f"Pista '{pista_id}' não encontrada."
            )

        escolha = self.sistema_dialogo.selecionar_escolha(indice)

        pista = None
        pista_nova = False

        if pista_id is not None:
            pista = self.pistas[pista_id]
            pista_nova = self.diario.registrar_pista(pista)

        return {
            "escolha": escolha,
            "pista": pista,
            "pista_nova": pista_nova
        }

    def obter_pistas_diario(self):
        return self.diario.listar_pistas()

    def quantidade_pistas(self):
        return self.diario.quantidade_pistas()

    def conversa_encerrada(self):
        return self.sistema_dialogo.esta_encerrado()
