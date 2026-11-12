
import pygame
import pygame_gui


class Diario:

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.aberto = False
        self.botoes = []
        self.painel = None
        self.detalhe = None

    def abrir(self):
        if self.aberto:
            return

        self.aberto = True

        self.painel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(180, 80, 920, 560),
            manager=self.manager
        )

        self.detalhe = pygame_gui.elements.UITextBox(
            html_text="Selecione uma pista para consultar seu significado.",
            relative_rect=pygame.Rect(350, 420, 700, 100),
            manager=self.manager,
            container=self.painel
        )

        self.atualizar_pistas()

    def atualizar_pistas(self):
        for botao in self.botoes:
            botao.kill()

        self.botoes.clear()

        pistas = self.jogo.partida.obter_pistas_diario()

        for indice, pista in enumerate(pistas):

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    20,
                    20 + indice * 55,
                    250,
                    45
                ),
                text=pista.simbolo,
                manager=self.manager,
                container=self.painel
            )

            self.botoes.append((botao, pista))

    def processar_evento(self, evento):

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:

            for botao, pista in self.botoes:

                if evento.ui_element == botao:
                    self.detalhe.kill()

                    self.detalhe = pygame_gui.elements.UITextBox(
                        html_text=(
                            f"<b>{pista.simbolo}</b><br>"
                            f"{pista.descricao}<br><br>"
                            f"{pista.significado}"
                        ),
                        relative_rect=pygame.Rect(
                            350, 420, 700, 100
                        ),
                        manager=self.manager,
                        container=self.painel
                    )

    def fechar(self):
        if not self.aberto:
            return

        self.painel.kill()
        self.painel = None
        self.detalhe = None
        self.botoes.clear()
        self.aberto = False
