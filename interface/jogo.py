
import pygame

from system.controlador_partida import ControladorPartida

from interface import estilo
from interface.gerenciador_telas import GerenciadorTelas
from interface.telas.menu import TelaMenu
from interface.telas.mapa import TelaMapa
from interface.telas.local import TelaLocal
from interface.telas.investigacao import TelaInvestigacao
from interface.telas.resolucao import TelaResolucao


class Jogo:
    """Loop principal e composição responsiva em 1280x720.

    A interface sempre é desenhada em uma superfície lógica. A janela pode ser
    redimensionada livremente: o conteúdo é ampliado/reduzido com letterbox,
    sem distorcer cenários ou personagens.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Fome e Frio — Uma Investigação na Ilha Congelada")

        self.largura = estilo.LARGURA
        self.altura = estilo.ALTURA

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura),
            pygame.RESIZABLE,
        )
        self.superficie = pygame.Surface((self.largura, self.altura)).convert()
        self.viewport = pygame.Rect(0, 0, self.largura, self.altura)
        self._recalcular_viewport()

        self.relogio = pygame.time.Clock()
        self.executando = True

        self.partida = None
        self.local_atual = None
        self.mensagem = ""
        self.mensagem_expira = 0

        self.gerenciador_telas = GerenciadorTelas()

        self.gerenciador_telas.adicionar_tela("menu", TelaMenu(self))
        self.gerenciador_telas.adicionar_tela("mapa", TelaMapa(self))
        self.gerenciador_telas.adicionar_tela("local", TelaLocal(self))
        self.gerenciador_telas.adicionar_tela("investigacao", TelaInvestigacao(self))
        self.gerenciador_telas.adicionar_tela("resolucao", TelaResolucao(self))

        self.gerenciador_telas.mudar_tela("menu")

    # ------------------------------------------------------------
    # Escala e entrada
    # ------------------------------------------------------------

    def _recalcular_viewport(self):
        largura_janela, altura_janela = self.tela.get_size()
        escala = min(largura_janela / self.largura, altura_janela / self.altura)
        largura_vista = max(1, round(self.largura * escala))
        altura_vista = max(1, round(self.altura * escala))
        self.viewport = pygame.Rect(
            (largura_janela - largura_vista) // 2,
            (altura_janela - altura_vista) // 2,
            largura_vista,
            altura_vista,
        )

    def redimensionar(self, largura, altura):
        largura = max(800, int(largura))
        altura = max(450, int(altura))
        self.tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        self._recalcular_viewport()

    def pos_mouse(self):
        """Converte a posição real do cursor para a superfície lógica."""
        return self._pos_para_logico(pygame.mouse.get_pos())

    def _evento_logico(self, evento):
        if evento.type in (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
        ):
            dados = dict(evento.dict)
            dados["pos"] = self._pos_para_logico(evento.pos)
            return pygame.event.Event(evento.type, dados)
        return evento

    def _pos_para_logico(self, pos):
        x, y = pos
        if self.viewport.w <= 0 or self.viewport.h <= 0:
            return (0, 0)

        logico_x = (x - self.viewport.x) * self.largura / self.viewport.w
        logico_y = (y - self.viewport.y) * self.altura / self.viewport.h
        return (
            int(max(0, min(self.largura - 1, logico_x))),
            int(max(0, min(self.altura - 1, logico_y))),
        )

    # ------------------------------------------------------------
    # Fluxo de telas
    # ------------------------------------------------------------

    def iniciar_partida(self):
        try:
            self.partida = ControladorPartida()
            self.local_atual = None
            self._limpar_notificacao()
            self.gerenciador_telas.mudar_tela("mapa")
        except Exception as erro:
            self.notificar(f"Falha ao iniciar partida: {erro}")

    def acessar_local(self, local_id):
        sucesso = self.partida.acessar_local(local_id)

        if not sucesso:
            return False

        self.local_atual = self.partida.mapa.obter_local_atual()
        tela_local = self.gerenciador_telas.telas["local"]
        tela_local.local = self.local_atual
        self._limpar_notificacao()
        self.gerenciador_telas.mudar_tela("local")
        return True

    def voltar_mapa(self):
        if self.partida is not None:
            self.partida.voltar_ao_mapa()
        self._limpar_notificacao()
        self.gerenciador_telas.mudar_tela("mapa")

    def abrir_deducoes(self):
        self._limpar_notificacao()
        self.gerenciador_telas.mudar_tela("investigacao")

    def voltar_menu(self):
        self.partida = None
        self.local_atual = None
        self._limpar_notificacao()
        self.gerenciador_telas.mudar_tela("menu")

    def _limpar_notificacao(self):
        self.mensagem = ""
        self.mensagem_expira = 0

    def notificar(self, mensagem):
        self.mensagem = str(mensagem)
        self.mensagem_expira = pygame.time.get_ticks() + 5000

    def encerrar(self):
        self.executando = False

    # ------------------------------------------------------------
    # Loop
    # ------------------------------------------------------------

    def executar(self):
        while self.executando:
            delta = self.relogio.tick(60) / 1000.0

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.encerrar()
                    continue

                if evento.type == pygame.VIDEORESIZE:
                    self.redimensionar(evento.w, evento.h)
                    continue

                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    tela = self.gerenciador_telas.telas.get(self.gerenciador_telas.tela_atual)
                    if tela is not None and hasattr(tela, "tratar_escape") and tela.tratar_escape():
                        continue

                    if self.partida is not None:
                        if self.gerenciador_telas.tela_atual == "investigacao":
                            self.gerenciador_telas.mudar_tela("local")
                        elif self.gerenciador_telas.tela_atual == "local":
                            self.voltar_mapa()
                        else:
                            self.voltar_menu()
                    else:
                        self.encerrar()
                    continue

                self.gerenciador_telas.processar_evento(self._evento_logico(evento))

            self.gerenciador_telas.atualizar(delta)

            self.superficie.fill(estilo.TINTA)
            self.gerenciador_telas.desenhar(self.superficie)
            self._desenhar_notificacao(self.superficie)
            self._apresentar()

        pygame.quit()

    def _apresentar(self):
        largura_janela, altura_janela = self.tela.get_size()
        self.tela.fill((0, 0, 0))

        if self.viewport.size == (self.largura, self.altura):
            self.tela.blit(self.superficie, self.viewport.topleft)
        else:
            imagem = pygame.transform.smoothscale(self.superficie, self.viewport.size)
            self.tela.blit(imagem, self.viewport.topleft)

        pygame.display.flip()

    def _notificacao_bloqueada(self):
        """Evita que o aviso cubra modais e botões da tela atual."""
        if self.gerenciador_telas.tela_atual is None:
            return False

        tela = self.gerenciador_telas.telas.get(self.gerenciador_telas.tela_atual)
        if tela is None:
            return False

        for atributo in ("diario", "dicas", "painel_dialogo", "historico"):
            elemento = getattr(tela, atributo, None)
            if getattr(elemento, "aberto", False):
                return True

        return getattr(tela, "resultado", None) is not None

    def _desenhar_notificacao(self, superficie):
        if not self.mensagem:
            return

        agora = pygame.time.get_ticks()
        if self._notificacao_bloqueada():
            # Congela o prazo enquanto o modal está aberto. Ao fechar, o
            # jogador ainda tem tempo de ler o aviso.
            self.mensagem_expira = agora + 5000
            return

        if agora >= self.mensagem_expira:
            self.mensagem = ""
            return

        fonte = estilo.fonte("ui", 14)
        linhas = estilo.quebrar_texto(self.mensagem, fonte, 470)
        linhas = linhas[:3]

        largura_texto = max((fonte.size(linha)[0] for linha in linhas), default=0)
        largura = min(520, largura_texto + 52)
        altura = max(48, 18 + len(linhas) * 20)
        rect = pygame.Rect(
            self.largura - 36 - largura,
            self.altura - 86 - altura,
            largura,
            altura,
        )

        estilo.desenhar_painel(
            superficie,
            rect,
            cor=(13, 23, 32),
            borda=estilo.DOURADO_ESCURO,
            raio=8,
            alpha=244,
            sombra=True,
            brilho_superior=False,
        )
        pygame.draw.rect(
            superficie,
            estilo.DOURADO,
            pygame.Rect(rect.x, rect.y + 9, 3, rect.h - 18),
            border_radius=2,
        )

        y = rect.y + 12
        for linha in linhas:
            imagem = fonte.render(linha, True, estilo.TEXTO)
            superficie.blit(imagem, (rect.x + 18, y))
            y += 20
