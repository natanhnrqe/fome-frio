"""Diário de investigação em modal, com lista de pistas e detalhe."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao


class Diario:
    PAINEL = pygame.Rect(140, 60, 1000, 600)

    def __init__(self, jogo):
        self.jogo = jogo
        self.aberto = False
        self.pistas = []
        self.pista_selecionada = None

        self.botoes_pistas: list[tuple[Botao, object]] = []
        self.botao_fechar = None
        self._ids_anteriores = []

    # ------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------

    def abrir(self):
        if self.aberto:
            return

        self.aberto = True
        self.pistas = self.jogo.partida.obter_pistas_diario()
        self.pista_selecionada = None
        self._montar_interface()

    def fechar(self):
        if not self.aberto:
            return

        self.aberto = False
        self.pista_selecionada = None
        self.botoes_pistas = []
        self.botao_fechar = None

    def atualizar(self):
        if not self.aberto:
            return

        pistas_atualizadas = self.jogo.partida.obter_pistas_diario()
        ids = [pista.id for pista in pistas_atualizadas]

        if ids != self._ids_anteriores:
            self.fechar()
            self.abrir()

    # ------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------

    def _montar_interface(self):
        self.botoes_pistas = []
        self._ids_anteriores = [pista.id for pista in self.pistas]

        total = len(self.pistas)
        area_lista = pygame.Rect(self.PAINEL.x + 32, self.PAINEL.y + 108,
                                 420, 398)
        espacamento = 6

        if total:
            altura_linha = min(44, max(30, (area_lista.h - espacamento * (total - 1)) // total))
        else:
            altura_linha = 44

        for indice, pista in enumerate(self.pistas):
            botao = Botao(
                (area_lista.x, area_lista.y + indice * (altura_linha + espacamento),
                 area_lista.w, altura_linha),
                estilo.formatar_logica(pista.simbolo),
                variacao="opcao",
                tamanho_fonte=13,
                fonte_nome="logica",
                alinhamento="esquerda",
                padding=(38, 4),
                max_linhas=2,
                prefixo=f"{indice + 1:02d}",
                raio=6,
            )
            self.botoes_pistas.append((botao, pista))

        self.botao_fechar = Botao(
            (self.PAINEL.right - 210, self.PAINEL.bottom - 68, 170, 40),
            "FECHAR DIÁRIO",
            variacao="secundario",
            tamanho_fonte=14,
            uma_linha=True,
        )

    def selecionar_pista(self, pista):
        self.pista_selecionada = pista
        for botao, pista_botao in self.botoes_pistas:
            botao.set_selecionado(pista_botao is pista)

    # ------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------

    def processar_evento(self, evento) -> bool:
        if not self.aberto:
            return False

        if self.botao_fechar is not None and self.botao_fechar.processar_evento(evento):
            self.fechar()
            return True

        for botao, pista in self.botoes_pistas:
            if botao.processar_evento(evento):
                self.selecionar_pista(pista)
                return True

        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return True

        return False

    def atualizar_hover(self, pos_mouse=None):
        if not self.aberto:
            return
        if self.botao_fechar is not None:
            self.botao_fechar.atualizar(pos_mouse)
        for botao, _ in self.botoes_pistas:
            botao.atualizar(pos_mouse)

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
            "Arquivo de pistas",
            estilo.fonte("ui", 11, True),
            estilo.TEXTO_FRACO,
            (self.PAINEL.x + 32, self.PAINEL.y + 22),
        )
        estilo.desenhar_texto(
            superficie,
            "DIÁRIO DE INVESTIGAÇÃO",
            estilo.fonte("titulo", 30, True),
            estilo.TEXTO,
            (self.PAINEL.x + 32, self.PAINEL.y + 40),
        )

        contador = f"{len(self.pistas):02d} PISTA" + ("S" if len(self.pistas) != 1 else "")
        etiqueta = pygame.Rect(self.PAINEL.right - 166, self.PAINEL.y + 34, 134, 28)
        estilo.desenhar_etiqueta(superficie, etiqueta, contador,
                                 cor=estilo.DOURADO, alpha=245)

        estilo.desenhar_divisoria(
            superficie,
            self.PAINEL.x + 32,
            self.PAINEL.right - 32,
            self.PAINEL.y + 88,
            estilo.BORDA,
            160,
        )

        self._desenhar_lista(superficie)
        self._desenhar_detalhe(superficie)

        if self.botao_fechar is not None:
            self.botao_fechar.desenhar(superficie)

    def _desenhar_lista(self, superficie):
        area = pygame.Rect(self.PAINEL.x + 32, self.PAINEL.y + 108, 420, 398)

        estilo.desenhar_texto_espacado(
            superficie,
            "Pistas coletadas",
            estilo.fonte("ui", 11, True),
            estilo.TEXTO_FRACO,
            (area.x, area.y - 20),
        )

        if not self.pistas:
            estilo.desenhar_painel(
                superficie,
                area,
                cor=(13, 21, 29),
                borda=estilo.BORDA,
                raio=8,
                alpha=180,
                sombra=False,
            )
            estilo.desenhar_paragrafo(
                superficie,
                "Nenhuma pista registrada. Investigue os locais e converse com os sobreviventes.",
                estilo.fonte("corpo", 17),
                estilo.TEXTO_SUAVE,
                area.inflate(-48, -48),
                espacamento=6,
            )
            return

        recorte_anterior = superficie.get_clip()
        superficie.set_clip(area)
        for botao, _ in self.botoes_pistas:
            botao.desenhar(superficie)
        superficie.set_clip(recorte_anterior)

    def _desenhar_detalhe(self, superficie):
        area = pygame.Rect(self.PAINEL.x + 480, self.PAINEL.y + 108, 488, 398)
        estilo.desenhar_painel(
            superficie,
            area,
            cor=(12, 21, 29),
            borda=estilo.BORDA,
            raio=8,
            alpha=210,
            sombra=False,
        )

        if self.pista_selecionada is None:
            fonte = estilo.fonte("corpo", 19)
            linhas = estilo.quebrar_texto(
                "Selecione uma pista à esquerda para consultar a descrição e o significado lógico.",
                fonte,
                area.w - 64,
            )
            y = area.centery - len(linhas) * 15
            for linha in linhas:
                imagem = fonte.render(linha, True, estilo.TEXTO_FRACO)
                superficie.blit(imagem, imagem.get_rect(center=(area.centerx, y)))
                y += 30
            return

        pista = self.pista_selecionada
        interno = area.inflate(-40, -32)
        x = interno.x
        y = interno.y

        estilo.desenhar_texto_espacado(
            superficie,
            "Pista selecionada",
            estilo.fonte("ui", 10, True),
            estilo.DOURADO,
            (x, y),
        )
        y += 20

        simbolo = estilo.formatar_logica(pista.simbolo)
        fonte_simbolo = estilo.fonte("logica", 23, True)
        linhas_simbolo = estilo.quebrar_texto(simbolo, fonte_simbolo, interno.w)
        for linha in linhas_simbolo[:2]:
            imagem = fonte_simbolo.render(linha, True, estilo.DOURADO_CLARO)
            superficie.blit(imagem, (x, y))
            y += fonte_simbolo.get_linesize() + 1

        y += 10
        estilo.desenhar_divisoria(superficie, x, interno.right, y, estilo.BORDA, 120)
        y += 14

        estilo.desenhar_texto_espacado(
            superficie,
            "Descrição",
            estilo.fonte("ui", 10, True),
            estilo.TEXTO_FRACO,
            (x, y),
        )
        y += 20

        fonte_texto = estilo.fonte("corpo", 15)
        linhas = estilo.quebrar_texto(str(pista.descricao), fonte_texto, interno.w)
        for linha in linhas[:5]:
            if y > interno.bottom - 108:
                break
            imagem = fonte_texto.render(linha, True, estilo.TEXTO)
            superficie.blit(imagem, (x, y))
            y += fonte_texto.get_linesize() + 3

        y += 16
        if y < interno.bottom - 90:
            estilo.desenhar_texto_espacado(
                superficie,
                "Significado lógico",
                estilo.fonte("ui", 10, True),
                estilo.TEXTO_FRACO,
                (x, y),
            )
            y += 20

        significados = estilo.quebrar_texto(str(pista.significado), fonte_texto, interno.w)
        for linha in significados[:3]:
            if y > interno.bottom - 6:
                break
            imagem = fonte_texto.render(linha, True, estilo.TEXTO_SUAVE)
            superficie.blit(imagem, (x, y))
            y += fonte_texto.get_linesize() + 3
