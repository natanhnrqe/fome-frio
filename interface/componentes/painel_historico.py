
import pygame
import pygame_gui


class PainelHistorico:

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface
        self.aberto = False

    def abrir(self):
        if self.aberto:
            return

        self.aberto = True

        historico = self.jogo.partida.obter_historico_deducoes()

        if historico:
            conteudo = "<br><br>".join(
                str(item) for item in historico
            )
        else:
            conteudo = "Nenhuma dedução registrada ainda."

        self.painel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(220, 100, 840, 500),
            manager=self.manager
        )

        self.texto = pygame_gui.elements.UITextBox(
            html_text=conteudo,
            relative_rect=pygame.Rect(20, 20, 800, 390),
            manager=self.manager,
            container=self.painel
        )

        self.botao_fechar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(300, 430, 220, 45),
            text="FECHAR",
            manager=self.manager,
            container=self.painel
        )

    def processar_evento(self, evento):
        if (
            self.aberto
            and evento.type == pygame_gui.UI_BUTTON_PRESSED
            and evento.ui_element == self.botao_fechar
        ):
            self.fechar()

    def fechar(self):
        if not self.aberto:
            return

        self.painel.kill()
        self.aberto = False
