
import pygame
import pygame_gui

from system.controlador_partida import ControladorPartida

from interface.gerenciador_telas import GerenciadorTelas
from interface.telas.menu import TelaMenu
from interface.telas.mapa import TelaMapa
from interface.telas.local import TelaLocal
from interface.telas.investigacao import TelaInvestigacao
from interface.telas.resolucao import TelaResolucao


class Jogo:

    def __init__(self):
        pygame.init()

        self.largura = 1280
        self.altura = 720

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption("Fome e Frio")

        self.relogio = pygame.time.Clock()
        self.executando = True

        self.interface = pygame_gui.UIManager(
            (self.largura, self.altura)
        )

        self.partida = None
        self.local_atual = None
        self.mensagem = ""
        self.mensagem_expira = 0

        self.gerenciador_telas = GerenciadorTelas()

        self.gerenciador_telas.adicionar_tela(
            "menu", TelaMenu(self)
        )

        self.gerenciador_telas.adicionar_tela(
            "mapa", TelaMapa(self)
        )

        self.gerenciador_telas.adicionar_tela(
            "local", TelaLocal(self)
        )

        self.gerenciador_telas.adicionar_tela(
            "investigacao", TelaInvestigacao(self)
        )

        self.gerenciador_telas.adicionar_tela(
            "resolucao",
            TelaResolucao(self)
        )

        self.gerenciador_telas.mudar_tela("menu")

    def iniciar_partida(self):
        try:
            self.partida = ControladorPartida()
            self.local_atual = None
            self.gerenciador_telas.mudar_tela("mapa")
        except Exception as erro:
            self.notificar(f"Falha ao iniciar partida: {erro}")

    def acessar_local(self, local_id):
        sucesso = self.partida.acessar_local(local_id)

        if not sucesso:
            return

        self.local_atual = self.partida.mapa.obter_local_atual()

        tela_local = self.gerenciador_telas.telas["local"]
        tela_local.local = self.local_atual

        self.gerenciador_telas.mudar_tela("local")

    def voltar_mapa(self):
        self.partida.voltar_ao_mapa()
        self.gerenciador_telas.mudar_tela("mapa")

    def abrir_deducoes(self):
        self.gerenciador_telas.mudar_tela("investigacao")

    def voltar_menu(self):
        self.partida = None
        self.local_atual = None
        self.mensagem = ""
        self.mensagem_expira = 0

        self.gerenciador_telas.mudar_tela("menu")

    def notificar(self, mensagem):
        self.mensagem = str(mensagem)
        self.mensagem_expira = pygame.time.get_ticks() + 5000

    def encerrar(self):
        self.executando = False

    def executar(self):
        while self.executando:

            delta = self.relogio.tick(60) / 1000.0

            for evento in pygame.event.get():

                self.interface.process_events(evento)

                if evento.type == pygame.QUIT:
                    self.encerrar()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:

                        if self.partida is not None:
                            if self.gerenciador_telas.tela_atual == "investigacao":
                                self.gerenciador_telas.mudar_tela("local")
                            elif self.gerenciador_telas.tela_atual == "local":
                                self.voltar_mapa()
                            else:
                                self.voltar_menu()
                        else:
                            self.encerrar()

                self.gerenciador_telas.processar_evento(evento)

            self.interface.update(delta)

            self.gerenciador_telas.atualizar(delta)

            self.tela.fill((18, 27, 38))

            self.gerenciador_telas.desenhar(self.tela)

            self.interface.draw_ui(self.tela)

            if self.mensagem and pygame.time.get_ticks() < self.mensagem_expira:
                fonte = pygame.font.SysFont("arial", 19)
                texto = fonte.render(self.mensagem, True, (245, 235, 210))
                pygame.draw.rect(self.tela, (15, 20, 26), pygame.Rect(100, 675, 1080, 32))
                self.tela.blit(texto, (115, 681))
            elif self.mensagem:
                self.mensagem = ""

            pygame.display.flip()

        pygame.quit()
