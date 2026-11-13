
import pygame
import pygame_gui

from interface.componentes.painel_dialogo import PainelDialogo
from interface.componentes.diario import Diario
from interface.recursos import fundo


class TelaLocal:
    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.local = None
        self.painel_dialogo = PainelDialogo(jogo)
        self.diario = Diario(jogo)

        self.botoes_personagens = []
        self.botoes = []

    def entrar(self):
        self.limpar_botoes()

        self.painel_dialogo.fechar()
        self.diario.fechar()

        self.criar_botoes()
        self.criar_botoes_personagens()

    def criar_botoes(self):
        configuracoes = [
            ("INVESTIGAR LOCAL", (440, 470, 400, 55)),
            ("DIÁRIO", (1050, 20, 200, 50)),
            ("DEDUÇÕES", (1050, 80, 200, 50)),
            ("VOLTAR AO MAPA", (20, 20, 200, 50))
        ]

        for texto, posicao in configuracoes:
            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(*posicao),
                text=texto,
                manager=self.manager
            )

            self.botoes.append(botao)

        (
            self.botao_investigar,
            self.botao_diario,
            self.botao_deducao,
            self.botao_voltar
        ) = self.botoes

    def criar_botoes_personagens(self):
        self.botoes_personagens.clear()

        if self.local is None:
            return

        personagens_ids = (
            self.jogo.partida.mapa.listar_personagens_no_local()
        )

        for indice, personagem_id in enumerate(personagens_ids):
            personagem = self.jogo.partida.personagens.get(
                personagem_id
            )

            if personagem is None:
                continue

            coluna = indice % 4

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    140 + coluna * 250,
                    330,
                    220,
                    55
                ),
                text=personagem.nome,
                manager=self.manager
            )

            self.botoes_personagens.append(
                (botao, personagem_id)
            )

    def processar_evento(self, evento):
        self.painel_dialogo.processar_evento(evento)
        self.diario.processar_evento(evento)

        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if evento.ui_element == self.botao_voltar:
            self.jogo.voltar_mapa()
            return

        if evento.ui_element == self.botao_diario:
            self.diario.abrir()
            return

        if evento.ui_element == self.botao_deducao:
            self.jogo.abrir_deducoes()
            return

        if evento.ui_element == self.botao_investigar:
            resultado = self.jogo.partida.investigar_local()

            if resultado:
                novas = resultado.get("pistas_novas", [])
                total = len(resultado.get("pistas_encontradas", []))
                if novas:
                    self.jogo.notificar(f"{len(novas)} nova(s) pista(s) encontrada(s). Consulte o diário.")
                else:
                    self.jogo.notificar(f"Você examinou o local. {total} pista(s) já conhecida(s); nenhuma novidade.")

            return

        for botao, personagem_id in self.botoes_personagens:
            if evento.ui_element == botao:
                self.painel_dialogo.abrir(personagem_id)
                return

    def atualizar(self, delta):
        self.diario.atualizar()

    def desenhar(self, superficie):
        nome_local = getattr(self.local, "id", "ilha")
        fundos = {"cozinha": "cozinha.png", "sala_capitao": "conves.png",
                  "caldeira": "caldeira.png", "enfermaria": "enfermaria.png",
                  "passadico": "passadico_navegante.png", "alojamentos": "comodos_tripulacao.png",
                  "farol": "ilha.png", "caverna": "ilha.png", "casa_abandonada": "deposito.png"}
        fundo(superficie, fundos.get(nome_local, "ilha.png"), 135)

        if self.local is None:
            return

        fonte_titulo = pygame.font.SysFont(
            "arial", 38, bold=True
        )

        fonte_texto = pygame.font.SysFont(
            "arial", 22
        )

        titulo = fonte_titulo.render(
            self.local.nome.upper(),
            True,
            (240, 240, 240)
        )

        superficie.blit(
            titulo,
            titulo.get_rect(center=(640, 150))
        )

        texto = fonte_texto.render(
            "Explore o local e converse com os sobreviventes.",
            True,
            (190, 195, 200)
        )

        superficie.blit(
            texto,
            texto.get_rect(center=(640, 220))
        )
        self.painel_dialogo.desenhar(superficie)

    def limpar_botoes(self):
        for botao in self.botoes:
            botao.kill()

        for botao, _ in self.botoes_personagens:
            botao.kill()

        self.botoes.clear()
        self.botoes_personagens.clear()

    def sair(self):
        self.limpar_botoes()
        self.painel_dialogo.fechar()
        self.diario.fechar()
