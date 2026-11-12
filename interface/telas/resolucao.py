
import pygame
import pygame_gui


class TelaResolucao:

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface
        self.botoes = []

    def entrar(self):
        self.botoes = []

        personagens = self.jogo.partida.personagens

        for indice, personagem in enumerate(personagens.values()):
            coluna = indice % 4
            linha = indice // 4

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    80 + coluna * 290,
                    220 + linha * 130,
                    250,
                    75
                ),
                text=personagem.nome,
                manager=self.manager
            )

            self.botoes.append((botao, personagem.id))

        self.botao_confirmar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(440, 550, 400, 60),
            text="CONFIRMAR ACUSAÇÃO",
            manager=self.manager
        )

        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 20, 200, 50),
            text="VOLTAR",
            manager=self.manager
        )

        self.suspeito_selecionado = None

        self.status = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(400, 140, 480, 50),
            text="Selecione quem você acredita ser o assassino.",
            manager=self.manager
        )

    def sair(self):
        for botao, _ in self.botoes:
            botao.kill()

        self.botoes.clear()
        self.botao_confirmar.kill()
        self.botao_voltar.kill()
        self.status.kill()

    def processar_evento(self, evento):
        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        for botao, personagem_id in self.botoes:
            if evento.ui_element == botao:
                self.suspeito_selecionado = personagem_id
                self.status.set_text(
                    f"Suspeito selecionado: {self.jogo.partida.personagens[personagem_id].nome}"
                )
                return

        if evento.ui_element == self.botao_voltar:
            self.jogo.gerenciador_telas.mudar_tela("investigacao")

        elif evento.ui_element == self.botao_confirmar:
            self.confirmar_acusacao()

    def confirmar_acusacao(self):
        if self.suspeito_selecionado is None:
            self.status.set_text("Selecione um suspeito primeiro.")
            return

        caso = self.jogo.partida.caso

        if self.suspeito_selecionado == caso.assassino_id:
            mensagem = "ACERTOU! Você identificou o assassino."
        else:
            mensagem = "ACUSAÇÃO INCORRETA! O assassino escapou."

        self.status.set_text(mensagem)

    def atualizar(self, delta):
        pass

    def desenhar(self, superficie):
        superficie.fill((18, 27, 38))

        fonte = pygame.font.Font(None, 65)

        titulo = fonte.render(
            "RESOLUÇÃO DO CASO",
            True,
            (230, 230, 230)
        )

        superficie.blit(
            titulo,
            titulo.get_rect(center=(640, 75))
        )
