
import pygame
import pygame_gui

from interface.componentes.painel_dialogo import PainelDialogo
from interface.componentes.diario import Diario


class TelaLocal:

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.local = None
        self.painel_dialogo = PainelDialogo(jogo)
        self.diario = Diario(jogo)
        self.botoes_personagens = []

    def entrar(self):
        self.botao_investigar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(440, 470, 400, 55),
            text="INVESTIGAR LOCAL",
            manager=self.manager
        )

        self.botao_diario = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(1050, 20, 200, 50),
            text="DIÁRIO",
            manager=self.manager
        )

        self.botao_deducao = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(1050, 80, 200, 50),
            text="DEDUÇÕES",
            manager=self.manager
        )

        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 20, 180, 50),
            text="VOLTAR AO MAPA",
            manager=self.manager
        )

        self.criar_botoes_personagens()

    def criar_botoes_personagens(self):
        if self.local is None:
            return

        personagens = (
            self.jogo.partida.mapa.listar_personagens_no_local()
        )

        for indice, personagem_id in enumerate(personagens):
            personagem = self.jogo.partida.personagens[personagem_id]

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    350 + indice * 200,
                    330,
                    180,
                    50
                ),
                text=personagem.nome,
                manager=self.manager
            )

            self.botoes_personagens.append(
                (botao, personagem_id)
            )

    def sair(self):
        self.botao_investigar.kill()
        self.botao_diario.kill()
        self.botao_deducao.kill()
        self.botao_voltar.kill()

        for botao, _ in self.botoes_personagens:
            botao.kill()

        self.botoes_personagens.clear()
        self.painel_dialogo.fechar()
        self.diario.fechar()

    def processar_evento(self, evento):
        self.painel_dialogo.processar_evento(evento)
        self.diario.processar_evento(evento)

        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if evento.ui_element == self.botao_voltar:
            self.jogo.voltar_mapa()

        elif evento.ui_element == self.botao_diario:
            if self.diario.aberto:
                self.diario.fechar()
            else:
                self.diario.abrir()

        elif evento.ui_element == self.botao_deducao:
            self.jogo.abrir_deducoes()

        elif evento.ui_element == self.botao_investigar:
            self.jogo.partida.investigar_local()

        else:
            for botao, personagem_id in self.botoes_personagens:
                if evento.ui_element == botao:
                    self.painel_dialogo.abrir(personagem_id)
                    break

    def atualizar(self, delta):
        pass

    def desenhar(self, superficie):
        superficie.fill((18, 27, 38))

        if self.local is None:
            return

        fonte = pygame.font.Font(None, 65)

        titulo = fonte.render(
            self.local.nome.upper(),
            True,
            (230, 230, 230)
        )

        superficie.blit(
            titulo,
            titulo.get_rect(center=(640, 150))
        )
