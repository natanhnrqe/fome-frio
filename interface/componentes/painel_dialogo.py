import pygame
import pygame_gui
from interface.recursos import retrato

class PainelDialogo:
    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface
        self.aberto = False
        self.componentes = []
        self.botoes_escolhas = []
        self.painel = None
        self.aviso = None

    def _criar(self, classe, rect, **kwargs):
        item = classe(relative_rect=pygame.Rect(rect), manager=self.manager,
                      container=self.painel, **kwargs)
        self.componentes.append(item)
        return item

    def abrir(self, personagem_id):
        self.fechar()
        try:
            # iniciar_conversa inicia o estado e retorna None por contrato.
            self.jogo.partida.iniciar_conversa(personagem_id)
            dialogo = self.jogo.partida.obter_dialogo_atual()
            if dialogo is None:
                self.jogo.notificar("Este personagem não possui falas disponíveis.")
                return
        except (ValueError, RuntimeError, KeyError) as erro:
            self.jogo.notificar(str(erro))
            return
        self.personagem_id = personagem_id
        self.aberto = True
        self.painel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(330, 260, 870, 430), manager=self.manager)
        self.retrato = retrato(personagem_id, (220, 290))
        self.falante = self._criar(pygame_gui.elements.UILabel,
                                   (20, 12, 825, 42), text="")
        self.fala = self._criar(pygame_gui.elements.UITextBox,
                                (20, 60, 825, 115), html_text="")
        self.status = self._criar(pygame_gui.elements.UITextBox,
                                  (20, 180, 825, 55), html_text="")
        self.fechar_botao = self._criar(pygame_gui.elements.UIButton,
                                        (635, 350, 210, 48), text="ENCERRAR CONVERSA")
        self.atualizar()

    def atualizar(self, aviso=""):
        self._limpar_escolhas()
        dialogo = self.jogo.partida.obter_dialogo_atual()
        escolhas = self.jogo.partida.obter_escolhas_dialogo() or []
        if dialogo is None:
            self.falante.set_text("CONVERSA ENCERRADA")
            self.fala.set_text("Você já esgotou as perguntas disponíveis.")
            self.status.set_text(aviso)
            return
        self.falante.set_text(dialogo.falante)
        self.fala.set_text(dialogo.fala)
        self.status.set_text(aviso)
        for indice, escolha in enumerate(escolhas[:3]):
            botao = self._criar(pygame_gui.elements.UIButton,
                                (20, 245 + indice * 48, 825, 42),
                                text=escolha.texto)
            self.botoes_escolhas.append((botao, indice))

    def processar_evento(self, evento):
        if not self.aberto or evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return
        if evento.ui_element == self.fechar_botao:
            self.fechar(); return
        for botao, indice in self.botoes_escolhas:
            if evento.ui_element == botao:
                try:
                    resultado = self.jogo.partida.selecionar_escolha(indice)
                    escolha = resultado.get("escolha")
                    aviso = escolha.resposta if escolha else ""
                    pista = resultado.get("pista")
                    if resultado.get("pista_nova") and pista:
                        aviso += f"  |  NOVA PISTA: {pista.simbolo}"
                    elif pista:
                        aviso += "  |  Esta pista já consta no diário."
                    self.atualizar(aviso)
                except (ValueError, IndexError, KeyError, RuntimeError) as erro:
                    self.status.set_text(str(erro))
                return

    def desenhar(self, superficie):
        if self.aberto and self.retrato:
            superficie.blit(self.retrato, (65, 310))

    def _limpar_escolhas(self):
        for botao, _ in self.botoes_escolhas:
            botao.kill()
        self.botoes_escolhas = []

    def fechar(self):
        self.aberto = False
        self._limpar_escolhas()
        for item in self.componentes:
            item.kill()
        self.componentes = []
        if self.painel:
            self.painel.kill()
        self.painel = None
        self.retrato = None
        self.aviso = None
