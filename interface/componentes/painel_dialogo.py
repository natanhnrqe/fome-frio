
import pygame
import pygame_gui


class PainelDialogo:

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.dialogo = None
        self.botoes = []
        self.texto_resposta = None

    def abrir(self, personagem_id):
        resultado = self.jogo.partida.iniciar_conversa(
            personagem_id
        )

        if not resultado:
            return

        self.atualizar_dialogo()

    def atualizar_dialogo(self):
        self.limpar_componentes()

        self.dialogo = (
            self.jogo.partida.obter_dialogo_atual()
        )

        if self.dialogo is None:
            return

        self.texto_resposta = pygame_gui.elements.UITextBox(
            html_text=self.dialogo.fala,
            relative_rect=pygame.Rect(260, 400, 760, 130),
            manager=self.manager
        )

        escolhas = (
            self.jogo.partida.obter_escolhas_dialogo()
        )

        for indice, escolha in enumerate(escolhas):

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    300,
                    550 + indice * 55,
                    680,
                    45
                ),
                text=escolha.texto,
                manager=self.manager
            )

            self.botoes.append(botao)

    def processar_evento(self, evento):

        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if evento.ui_element not in self.botoes:
            return

        indice = self.botoes.index(evento.ui_element)

        self.jogo.partida.selecionar_escolha(indice)

        self.atualizar_dialogo()

    def limpar_componentes(self):
        for botao in self.botoes:
            botao.kill()

        self.botoes.clear()

        if self.texto_resposta:
            self.texto_resposta.kill()
            self.texto_resposta = None

    def fechar(self):
        self.limpar_componentes()
        self.dialogo = None
