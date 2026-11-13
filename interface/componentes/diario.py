
import pygame
import pygame_gui


class Diario:
    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.aberto = False
        self.pistas = []
        self.pista_selecionada = None

        self.painel = None
        self.botoes_pistas = []
        self.texto_detalhe = None
        self.botao_fechar = None
        self.texto_contador = None

    def abrir(self):
        if self.aberto:
            return

        self.aberto = True
        self.pistas = self.jogo.partida.obter_pistas_diario()
        self.pista_selecionada = None

        self.criar_interface()

    def criar_interface(self):
        self.painel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(140, 70, 1000, 580),
            manager=self.manager
        )

        titulo = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 10, 940, 45),
            text="DIÁRIO DE INVESTIGAÇÃO",
            manager=self.manager,
            container=self.painel
        )

        self.texto_contador = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 55, 430, 35),
            text=f"PISTAS ENCONTRADAS: {len(self.pistas)}",
            manager=self.manager,
            container=self.painel
        )

        self.criar_lista_pistas()

        self.texto_detalhe = pygame_gui.elements.UITextBox(
            html_text="Selecione uma pista para consultar seus detalhes.",
            relative_rect=pygame.Rect(470, 100, 490, 390),
            manager=self.manager,
            container=self.painel
        )

        self.botao_fechar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(750, 510, 200, 45),
            text="FECHAR DIÁRIO",
            manager=self.manager,
            container=self.painel
        )

    def criar_lista_pistas(self):
        if not self.pistas:
            return

        for indice, pista in enumerate(self.pistas):
            simbolo = str(pista.simbolo)

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    20,
                    100 + indice * 48,
                    420,
                    42
                ),
                text=f"PISTA {indice + 1}: {simbolo}",
                manager=self.manager,
                container=self.painel
            )

            self.botoes_pistas.append((botao, pista))

    def selecionar_pista(self, pista):
        self.pista_selecionada = pista

        simbolo = str(pista.simbolo)
        descricao = str(pista.descricao)
        significado = str(pista.significado)

        texto = (
            f"<b>PISTA</b><br>"
            f"{simbolo}<br><br>"
            f"<b>DESCRIÇÃO</b><br>"
            f"{descricao}<br><br>"
            f"<b>SIGNIFICADO LÓGICO</b><br>"
            f"{significado}"
        )

        self.texto_detalhe.set_text(texto)

    def processar_evento(self, evento):
        if not self.aberto:
            return

        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if evento.ui_element == self.botao_fechar:
            self.fechar()
            return

        for botao, pista in self.botoes_pistas:
            if evento.ui_element == botao:
                self.selecionar_pista(pista)
                return

    def atualizar(self):
        if not self.aberto:
            return

        pistas_atualizadas = (
            self.jogo.partida.obter_pistas_diario()
        )

        if len(pistas_atualizadas) != len(self.pistas):
            self.fechar()
            self.abrir()

    def fechar(self):
        if not self.aberto:
            return

        self.aberto = False

        if self.painel is not None:
            self.painel.kill()

        self.painel = None
        self.botoes_pistas.clear()
        self.texto_detalhe = None
        self.botao_fechar = None
        self.texto_contador = None
        self.pista_selecionada = None
