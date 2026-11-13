"""Caixa de diálogo no padrão de visual novel."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao
from interface.estilo import PAINEL_DIALOGO


class PainelDialogo:
    def __init__(self, jogo):
        self.jogo = jogo
        self.aberto = False
        self.personagem_id = None
        self.falante = ""
        self.cargo = ""
        self.fala = ""
        self.resposta = ""
        self.aviso = ""

        self.botoes_escolhas: list[tuple[Botao, int]] = []
        self.botao_fechar = None
        self.botao_encerrar = None
        self.retrato = None

    # ------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------

    def abrir(self, personagem_id):
        self.fechar()

        try:
            # iniciar_conversa prepara o estado e retorna None por contrato.
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
        self.aviso = ""
        self.atualizar()

    def fechar(self):
        self.aberto = False
        self.personagem_id = None
        self.falante = ""
        self.cargo = ""
        self.fala = ""
        self.resposta = ""
        self.aviso = ""
        self.botoes_escolhas = []
        self.botao_fechar = None
        self.botao_encerrar = None
        self.retrato = None

    # ------------------------------------------------------------
    # Conteúdo
    # ------------------------------------------------------------

    def _nome_do_falante(self, dialogo):
        personagem = self.jogo.partida.personagens.get(self.personagem_id)
        if personagem is not None:
            return personagem.nome, personagem.cargo
        if dialogo is not None and dialogo.falante not in ("npc", ""):
            return dialogo.falante, ""
        return "DESCONHECIDO", ""

    def atualizar(self, resposta=None, aviso=""):
        base = PAINEL_DIALOGO
        self.botoes_escolhas = []
        self.botao_encerrar = None
        self.resposta = resposta or ""
        self.aviso = aviso
        self.botao_fechar = Botao(
            (base.right - 104, base.y + 12, 88, 28),
            "FECHAR",
            variacao="fantasma",
            tamanho_fonte=11,
            padding=(8, 4),
            uma_linha=True,
        )

        dialogo = self.jogo.partida.obter_dialogo_atual()
        escolhas = self.jogo.partida.obter_escolhas_dialogo() or []

        if dialogo is None:
            nome, cargo = self._nome_do_falante(None)
            self.falante = nome
            self.cargo = cargo
            if self.resposta:
                self.fala = self.resposta
                self.aviso = aviso or "As perguntas disponíveis para este personagem foram esgotadas."
            else:
                self.falante = "CONVERSA ENCERRADA"
                self.cargo = ""
                self.fala = "As perguntas disponíveis para este personagem foram esgotadas."
            self._criar_fechamento()
            return

        nome, cargo = self._nome_do_falante(dialogo)
        self.falante = nome
        self.cargo = cargo
        # A resposta escolhida é a fala principal deste compasso. A pergunta
        # seguinte continua disponível nas opções, sem texto minúsculo.
        self.fala = self.resposta or dialogo.fala

        base = PAINEL_DIALOGO
        for indice, escolha in enumerate(escolhas[:3]):
            botao = Botao(
                (base.x + 452, base.y + 70 + indice * 56, 320, 50),
                escolha.texto,
                variacao="opcao",
                tamanho_fonte=15,
                alinhamento="esquerda",
                padding=(34, 6),
                max_linhas=2,
            )
            self.botoes_escolhas.append((botao, indice))

        if not self.botoes_escolhas:
            self._criar_fechamento()

    def _criar_fechamento(self):
        base = PAINEL_DIALOGO
        self.botao_encerrar = Botao(
            (base.x + 452, base.bottom - 56, 320, 44),
            "ENCERRAR CONVERSA",
            variacao="primario",
            tamanho_fonte=15,
        )

    # ------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------

    def processar_evento(self, evento) -> bool:
        if not self.aberto:
            return False

        if evento.type == pygame.KEYDOWN and pygame.K_1 <= evento.key <= pygame.K_3:
            indice = evento.key - pygame.K_1
            if indice < len(self.botoes_escolhas):
                self._selecionar(indice)
                return True

        if self.botao_fechar is not None and self.botao_fechar.processar_evento(evento):
            self.fechar()
            return True

        if self.botao_encerrar is not None and self.botao_encerrar.processar_evento(evento):
            self.fechar()
            return True

        for botao, indice in self.botoes_escolhas:
            if botao.processar_evento(evento):
                self._selecionar(indice)
                return True

        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return PAINEL_DIALOGO.collidepoint(evento.pos)

        return False

    def _selecionar(self, indice):
        try:
            resultado = self.jogo.partida.selecionar_escolha(indice)
            escolha = resultado.get("escolha")
            resposta = escolha.resposta if escolha else ""
            pista = resultado.get("pista")
            aviso = ""

            if resultado.get("pista_nova") and pista:
                aviso = "NOVA PISTA  ·  " + estilo.formatar_logica(pista.simbolo)
            elif pista:
                aviso = "Pista já registrada no diário."

            self.atualizar(resposta=resposta, aviso=aviso)
        except (ValueError, IndexError, KeyError, RuntimeError) as erro:
            self.aviso = str(erro)

    # ------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------

    def desenhar(self, superficie):
        if not self.aberto:
            return

        base = PAINEL_DIALOGO
        estilo.desenhar_painel(
            superficie,
            base,
            cor=(15, 24, 33),
            borda=estilo.BORDA_CLARA,
            raio=12,
            alpha=242,
            sombra=True,
        )

        # Filete dourado superior da caixa.
        pygame.draw.line(
            superficie,
            estilo.DOURADO,
            (base.x + 22, base.y + 1),
            (base.right - 22, base.y + 1),
            2,
        )

        self._desenhar_nome(superficie)

        corpo = pygame.Rect(base.x + 32, base.y + 66, 390, 140)
        pygame.draw.line(
            superficie,
            estilo.DOURADO_ESCURO,
            (corpo.x - 12, corpo.y + 2),
            (corpo.x - 12, corpo.y + corpo.h - 4),
            2,
        )

        tamanho_corpo = 20
        fonte_corpo = estilo.fonte("corpo", tamanho_corpo)
        linhas = estilo.quebrar_texto(self.fala, fonte_corpo, corpo.w)
        while (
            len(linhas) * fonte_corpo.get_linesize() + max(0, len(linhas) - 1) * 4 > corpo.h
            and tamanho_corpo > 15
        ):
            tamanho_corpo -= 1
            fonte_corpo = estilo.fonte("corpo", tamanho_corpo)
            linhas = estilo.quebrar_texto(self.fala, fonte_corpo, corpo.w)

        estilo.desenhar_paragrafo(
            superficie,
            self.fala,
            fonte_corpo,
            estilo.TEXTO,
            corpo,
            espacamento=4,
            limite_linhas=len(linhas),
        )

        if self.aviso:
            fonte_aviso = estilo.fonte("logica", 12)
            estilo.desenhar_texto(
                superficie,
                self.aviso,
                fonte_aviso,
                estilo.DOURADO_CLARO,
                (base.x + 32, base.bottom - 31),
            )

        for botao, _ in self.botoes_escolhas:
            botao.desenhar(superficie)

        if self.botao_encerrar is not None:
            self.botao_encerrar.desenhar(superficie)

        if self.botao_fechar is not None:
            self.botao_fechar.desenhar(superficie)

    def _desenhar_nome(self, superficie):
        base = PAINEL_DIALOGO
        nome = self.falante or "—"
        fonte_nome = estilo.fonte("titulo", 21, negrito=True)
        largura = max(218, min(380, fonte_nome.size(nome)[0] + 44))
        rect = pygame.Rect(base.x + 26, base.y + 10, largura, 44)

        estilo.desenhar_painel(
            superficie,
            rect,
            cor=(25, 36, 46),
            borda=estilo.DOURADO_ESCURO,
            raio=6,
            alpha=252,
            sombra=False,
            brilho_superior=False,
        )
        pygame.draw.rect(
            superficie,
            estilo.DOURADO,
            pygame.Rect(rect.x, rect.y + 7, 3, rect.h - 14),
            border_radius=2,
        )

        nome_img = fonte_nome.render(nome, True, estilo.DOURADO_CLARO)
        superficie.blit(nome_img, (rect.x + 16, rect.y + 4))

        cargo = getattr(self, "cargo", "")
        if cargo:
            cargo_img = estilo.fonte("ui", 10).render(cargo.upper(), True, estilo.TEXTO_FRACO)
            superficie.blit(cargo_img, (rect.x + 16, rect.y + 28))

    def atualizar_hover(self, pos_mouse=None):
        if not self.aberto:
            return
        if self.botao_fechar is not None:
            self.botao_fechar.atualizar(pos_mouse)
        if self.botao_encerrar is not None:
            self.botao_encerrar.atualizar(pos_mouse)
        for botao, _ in self.botoes_escolhas:
            botao.atualizar(pos_mouse)
