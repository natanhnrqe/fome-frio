
import pygame
import pygame_gui
from interface.recursos import fundo


class TelaMenu:

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

    def entrar(self):
        self.botao_nova = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(440, 390, 400, 65),
            text="NOVA INVESTIGAÇÃO",
            manager=self.manager
        )

        self.botao_sair = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(440, 480, 400, 65),
            text="SAIR",
            manager=self.manager
        )

    def sair(self):
        self.botao_nova.kill()
        self.botao_sair.kill()

    def processar_evento(self, evento):
        if evento.type == pygame_gui.UI_BUTTON_PRESSED:

            if evento.ui_element == self.botao_nova:
                self.jogo.iniciar_partida()

            elif evento.ui_element == self.botao_sair:
                self.jogo.encerrar()

    def atualizar(self, delta):
        pass

    def desenhar(self, superficie):
        fundo(superficie, "ilha.png", 115)

        fonte = pygame.font.Font(None, 90)
        fonte_subtitulo = pygame.font.Font(None, 32)

        titulo = fonte.render(
            "FOME E FRIO",
            True,
            (230, 230, 230)
        )

        subtitulo = fonte_subtitulo.render(
            "Uma investigação em uma ilha congelada",
            True,
            (170, 185, 200)
        )

        superficie.blit(
            titulo,
            titulo.get_rect(center=(640, 230))
        )

        superficie.blit(
            subtitulo,
            subtitulo.get_rect(center=(640, 305))
        )
