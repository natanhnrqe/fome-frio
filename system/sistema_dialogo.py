
class SistemaDialogo:
    def __init__(self, dialogos: dict):
        self.dialogos = dialogos
        self.dialogo_atual_id = None
        self.encerrado = True

    def iniciar(self, dialogo_inicial_id: str):
        if dialogo_inicial_id not in self.dialogos:
            raise ValueError(
                f"Diálogo inicial '{dialogo_inicial_id}' não encontrado."
            )

        self.dialogo_atual_id = dialogo_inicial_id
        self.encerrado = False

    def obter_dialogo_atual(self):
        if self.encerrado:
            return None

        return self.dialogos[self.dialogo_atual_id]

    def obter_escolhas(self):
        dialogo = self.obter_dialogo_atual()

        if dialogo is None:
            return []

        return dialogo.escolhas

    def selecionar_escolha(self, indice: int):
        dialogo = self.obter_dialogo_atual()

        if dialogo is None:
            raise RuntimeError("Não existe uma conversa ativa.")

        if indice < 0 or indice >= len(dialogo.escolhas):
            raise IndexError("Escolha inválida.")

        escolha = dialogo.escolhas[indice]
        proxima_etapa = escolha.proxima_etapa

        if proxima_etapa is None:
            self.dialogo_atual_id = None
            self.encerrado = True

        else:
            if proxima_etapa not in self.dialogos:
                raise ValueError(
                    f"Próxima etapa '{proxima_etapa}' não encontrada."
                )

            self.dialogo_atual_id = proxima_etapa

        return escolha

    def reiniciar(self, dialogo_inicial_id: str):
        self.iniciar(dialogo_inicial_id)

    def esta_encerrado(self) -> bool:
        return self.encerrado
