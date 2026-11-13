
import pygame
import pygame_gui
from interface.recursos import fundo


class TelaMapa:

    LOCAIS = [
        ("cozinha", "COZINHA"),
        ("sala_capitao", "SALA DO CAPITÃO"),
        ("caldeira", "CALDEIRA"),
        ("enfermaria", "ENFERMARIA"),
        ("passadico", "PASSADIÇO"),
        ("alojamentos", "ALOJAMENTOS"),
        ("farol", "FAROL ABANDONADO"),
        ("caverna", "CAVERNA"),
        ("casa_abandonada", "CASA ABANDONADA")
    ]

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface
        self.botoes_locais = {}

    def entrar(self):
        self.botoes_locais = {}

        largura = 330
        altura = 75
        espacamento_x = 35
        espacamento_y = 25

        inicio_x = 100
        inicio_y = 170

        for indice, (local_id, nome) in enumerate(self.LOCAIS):

            coluna = indice % 3
            linha = indice // 3

            x = inicio_x + coluna * (largura + espacamento_x)
            y = inicio_y + linha * (altura + espacamento_y)

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    x, y, largura, altura
                ),
                text=nome,
                manager=self.manager
            )

            self.botoes_locais[botao] = local_id

    def sair(self):
        for botao in self.botoes_locais:
            botao.kill()

        self.botoes_locais.clear()

    def processar_evento(self, evento):

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:

            local_id = self.botoes_locais.get(
                evento.ui_element
            )

            if local_id is not None:
                self.jogo.acessar_local(local_id)

    def atualizar(self, delta):
        pass

    def desenhar(self, superficie):
        fundo(superficie, "ilha.png", 125)

        fonte_titulo = pygame.font.Font(None, 65)
        fonte_descricao = pygame.font.Font(None, 30)

        titulo = fonte_titulo.render(
            "MAPA DA ILHA",
            True,
            (230, 230, 230)
        )

        descricao = fonte_descricao.render(
            "Selecione um local para investigar",
            True,
            (170, 185, 200)
        )

        superficie.blit(
            titulo,
            titulo.get_rect(center=(640, 75))
        )

        superficie.blit(
            descricao,
            descricao.get_rect(center=(640, 125))
        )
