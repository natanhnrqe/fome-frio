
class GerenciadorTelas:

    def __init__(self):
        self.telas = {}
        self.tela_atual = None

    def adicionar_tela(self, nome, tela):
        self.telas[nome] = tela

    def mudar_tela(self, nome):
        if nome not in self.telas:
            raise ValueError(f"Tela '{nome}' não encontrada.")

        if self.tela_atual is not None:
            self.telas[self.tela_atual].sair()

        self.tela_atual = nome
        self.telas[self.tela_atual].entrar()

    def processar_evento(self, evento):
        if self.tela_atual is not None:
            self.telas[self.tela_atual].processar_evento(evento)

    def atualizar(self, delta):
        if self.tela_atual is not None:
            self.telas[self.tela_atual].atualizar(delta)

    def desenhar(self, superficie):
        if self.tela_atual is not None:
            self.telas[self.tela_atual].desenhar(superficie)
