
import pygame
import pygame_gui

from interface.componentes.painel_deducao import PainelDeducao
from interface.componentes.painel_historico import PainelHistorico


class TelaInvestigacao:

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.painel = PainelDeducao(jogo)
        self.historico = PainelHistorico(jogo)

    def entrar(self):
        self.painel.entrar()

        self.status = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(350, 620, 580, 40),
            text="Demonstre todas as conclusões para resolver o caso.",
            manager=self.manager
        )

        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 20, 200, 50),
            text="VOLTAR AO LOCAL",
            manager=self.manager
        )

        self.botao_historico = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(1050, 20, 200, 50),
            text="HISTÓRICO",
            manager=self.manager
        )

        self.botao_resolver = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(1050, 80, 200, 50),
            text="RESOLVER CASO",
            manager=self.manager
        )

    def sair(self):
        self.painel.sair()
        self.historico.fechar()


        self.botao_voltar.kill()
        self.botao_historico.kill()
        self.botao_resolver.kill()

    def processar_evento(self, evento):
        self.historico.processar_evento(evento)

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:

            if evento.ui_element == self.botao_voltar:
                self.jogo.gerenciador_telas.mudar_tela("local")
                return

            if evento.ui_element == self.botao_historico:
                self.historico.abrir()
                return

            if evento.ui_element == self.botao_resolver:
                self.tentar_abrir_resolucao()
                return

        if not self.historico.aberto:
            self.painel.processar_evento(evento)

    def atualizar(self, delta):
        pass

    def desenhar(self, superficie):
        superficie.fill((18, 27, 38))
        self.painel.desenhar(superficie)

    def tentar_abrir_resolucao(self):
        resultado = self.jogo.partida.tentar_resolver()

        if resultado["resolvido"]:
            self.jogo.gerenciador_telas.mudar_tela("resolucao")
        else:
            pendencias = ", ".join(resultado["pendencias"])

            self.status.set_text(
                f"Conclusões pendentes: {pendencias}"
            )