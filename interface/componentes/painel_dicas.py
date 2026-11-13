"""Painel de dicas da mesa de dedução.

Mostra as frases das pistas coletadas para o jogador reconhecer o que cada
premissa representa, além de uma orientação para a regra ativa.
"""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao


class PainelDicas:
    PAINEL = pygame.Rect(150, 60, 980, 600)
    AREA = pygame.Rect(182, 278, 916, 376)

    DICAS_REGRA = {
        "modus_ponens": (
            "Procure uma premissa que afirme um fato (A) e outra que diga que "
            "esse fato leva a outro (A → B)."
        ),
        "silogismo_disjuntivo": (
            "Procure uma premissa com duas alternativas (A ∨ B) e a negação "
            "de uma delas (¬A ou ¬B)."
        ),
        "conjuncao": (
            "Escolha duas premissas verdadeiras quaisquer para uni-las em uma "
            "única conjunção (A ∧ B)."
        ),
    }

    def __init__(self, jogo):
        self.jogo = jogo
        self.aberto = False
        self.pistas = []
        self.regra = ("modus_ponens", "MODUS PONENS", "")
        self.rolagem = 0
        self.botao_fechar = None

    # ------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------

    def abrir(self, regra=None):
        self.aberto = True
        self.rolagem = 0
        if regra is not None:
            self.regra = regra

        self.pistas = self.jogo.partida.obter_pistas_diario()
        self.botao_fechar = Botao(
            (self.PAINEL.right - 170, self.PAINEL.y + 26, 138, 38),
            "FECHAR DICAS",
            variacao="secundario",
            tamanho_fonte=12,
            uma_linha=True,
        )

    def fechar(self):
        self.aberto = False
        self.pistas = []
        self.rolagem = 0
        self.botao_fechar = None

    # ------------------------------------------------------------
    # Conteúdo
    # ------------------------------------------------------------

    def _origem(self, pista):
        partes = []
        mapa = getattr(self.jogo.partida, "mapa", None)
        if mapa is not None and getattr(pista, "local_id", None):
            local = mapa.locais.get(pista.local_id)
            if local is not None:
                partes.append(local.nome)

        personagem_id = getattr(pista, "personagem_id", None)
        if personagem_id:
            personagem = self.jogo.partida.personagens.get(personagem_id)
            if personagem is not None:
                partes.append(personagem.nome)

        return "  ·  ".join(partes)

    def _altura_total(self):
        linhas = (len(self.pistas) + 1) // 2
        if linhas <= 0:
            return 0
        return linhas * 88 + (linhas - 1) * 8

    def _limite_rolagem(self):
        return max(0, self._altura_total() - self.AREA.h)

    # ------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------

    def processar_evento(self, evento) -> bool:
        if not self.aberto:
            return False

        if evento.type == pygame.MOUSEWHEEL:
            self.rolagem = min(
                self._limite_rolagem(),
                max(0, self.rolagem - evento.y * 44),
            )
            return True

        if self.botao_fechar is not None and self.botao_fechar.processar_evento(evento):
            self.fechar()
            return True

        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return True

        return False

    def atualizar_hover(self, pos_mouse=None):
        if not self.aberto:
            return
        if self.botao_fechar is not None:
            self.botao_fechar.atualizar(pos_mouse)

    # ------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------

    def desenhar(self, superficie):
        if not self.aberto:
            return

        superficie.blit(estilo.overlay(superficie.get_size(), (3, 6, 10), 176), (0, 0))
        estilo.desenhar_painel(
            superficie,
            self.PAINEL,
            cor=(16, 26, 36),
            borda=estilo.BORDA_CLARA,
            raio=12,
            alpha=249,
        )
        pygame.draw.line(
            superficie,
            estilo.DOURADO,
            (self.PAINEL.x + 24, self.PAINEL.y + 1),
            (self.PAINEL.right - 24, self.PAINEL.y + 1),
            2,
        )

        estilo.desenhar_texto_espacado(
            superficie,
            "Apoio à dedução",
            estilo.fonte("ui", 11, True),
            estilo.TEXTO_FRACO,
            (self.PAINEL.x + 32, self.PAINEL.y + 22),
        )
        estilo.desenhar_texto(
            superficie,
            "DICAS DE DEDUÇÃO",
            estilo.fonte("titulo", 30, True),
            estilo.TEXTO,
            (self.PAINEL.x + 32, self.PAINEL.y + 40),
        )

        self._desenhar_regra(superficie)

        estilo.desenhar_texto_espacado(
            superficie,
            "Frases das pistas coletadas",
            estilo.fonte("ui", 10, True),
            estilo.DOURADO,
            (self.PAINEL.x + 32, self.AREA.y - 20),
        )
        if self._limite_rolagem() > 0:
            estilo.desenhar_texto(
                superficie,
                "roda do mouse para ver mais",
                estilo.fonte("ui", 10),
                estilo.TEXTO_FRACO,
                (self.PAINEL.right - 32, self.AREA.y - 20),
                alinhamento="direita",
            )

        if not self.pistas:
            estilo.desenhar_texto(
                superficie,
                "Nenhuma pista coletada ainda. Investigue os locais e converse com os sobreviventes.",
                estilo.fonte("corpo", 17),
                estilo.TEXTO_SUAVE,
                (self.PAINEL.centerx, self.AREA.centery),
                alinhamento="centro",
            )
        else:
            self._desenhar_cartoes(superficie)

        if self.botao_fechar is not None:
            self.botao_fechar.desenhar(superficie)

    def _desenhar_regra(self, superficie):
        chave, rotulo, _descricao = self.regra
        rect = pygame.Rect(self.PAINEL.x + 32, self.PAINEL.y + 102,
                           self.PAINEL.w - 64, 92)
        estilo.desenhar_painel(
            superficie,
            rect,
            cor=(22, 35, 46),
            borda=estilo.BORDA,
            raio=8,
            alpha=242,
            sombra=False,
        )

        estilo.desenhar_texto_espacado(
            superficie,
            f"Regra ativa  ·  {rotulo}",
            estilo.fonte("ui", 10, True),
            estilo.DOURADO_CLARO,
            (rect.x + 18, rect.y + 12),
        )
        estilo.desenhar_paragrafo(
            superficie,
            self.DICAS_REGRA.get(chave, _descricao),
            estilo.fonte("logica", 15),
            estilo.TEXTO,
            (rect.x + 18, rect.y + 34, rect.w - 36, 46),
            espacamento=3,
            limite_linhas=2,
        )

    def _desenhar_cartoes(self, superficie):
        recorte_anterior = superficie.get_clip()
        superficie.set_clip(self.AREA)

        largura = (self.AREA.w - 16) // 2
        y = self.AREA.y - self.rolagem

        for indice, pista in enumerate(self.pistas):
            coluna = indice % 2
            linha = indice // 2
            rect = pygame.Rect(
                self.AREA.x + coluna * (largura + 16),
                y + linha * 96,
                largura,
                88,
            )
            if rect.bottom >= self.AREA.y and rect.y <= self.AREA.bottom:
                self._desenhar_cartao(superficie, rect, pista)

        superficie.set_clip(recorte_anterior)

    def _desenhar_cartao(self, superficie, rect, pista):
        estilo.desenhar_painel(
            superficie,
            rect,
            cor=(21, 34, 45),
            borda=estilo.BORDA,
            raio=7,
            alpha=244,
            sombra=False,
            brilho_superior=False,
        )
        pygame.draw.rect(
            superficie,
            estilo.DOURADO_ESCURO,
            pygame.Rect(rect.x, rect.y + 8, 3, rect.h - 16),
            border_radius=2,
        )

        simbolo = estilo.formatar_logica(pista.simbolo)
        fonte_simbolo = self._ajustar_simbolo(simbolo, rect.w - 24)
        estilo.desenhar_texto(
            superficie,
            simbolo,
            fonte_simbolo,
            estilo.DOURADO_CLARO,
            (rect.x + 12, rect.y + 6),
        )
        estilo.desenhar_paragrafo(
            superficie,
            str(pista.descricao),
            estilo.fonte("corpo", 12),
            estilo.TEXTO,
            (rect.x + 12, rect.y + 26, rect.w - 24, 47),
            espacamento=1,
            limite_linhas=3,
        )

        origem = self._origem(pista)
        if origem:
            estilo.desenhar_texto(
                superficie,
                origem,
                estilo.fonte("ui", 9),
                estilo.TEXTO_FRACO,
                (rect.x + 12, rect.y + 72),
            )

    @staticmethod
    def _ajustar_simbolo(simbolo, largura):
        tamanho = 15
        while tamanho > 10:
            fonte = estilo.fonte("logica", tamanho, True)
            if fonte.size(simbolo)[0] <= largura:
                return fonte
            tamanho -= 1
        return estilo.fonte("logica", tamanho, True)
