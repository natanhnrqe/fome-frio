"""Seleção de locais com composição de visual novel, não em grade de painel."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao
from interface.recursos import fundo


class TelaMapa:
    LOCAIS = [
        ("cozinha", "COZINHA"),
        ("sala_capitao", "SALA DO CAPITÃO"),
        ("caldeira", "CALDEIRA"),
        ("enfermaria", "ENFERMARIA"),
        ("passadico", "PASSADIÇO"),
        ("alojamentos", "ALOJAMENTOS"),
        ("farol", "FAROL ABANDONADO"),
        ("caverna", "CAVERNA"),
        ("casa_abandonada", "CASA ABANDONADA"),
    ]

    PAINEL_LISTA = pygame.Rect(48, 140, 430, 520)
    PAINEL_PREVIA = pygame.Rect(824, 466, 408, 176)

    def __init__(self, jogo):
        self.jogo = jogo
        self.botoes_locais = []
        self.botao_menu = None
        self.local_foco = None

    def entrar(self):
        self.botoes_locais = []
        self.local_foco = None

        self.botao_menu = Botao(
            (estilo.LARGURA - estilo.MARGEM - 108, estilo.TOPO_Y, 108, estilo.TOPO_ALTURA),
            "MENU",
            variacao="fantasma",
            tamanho_fonte=12,
            uma_linha=True,
        )

        for indice, (local_id, nome) in enumerate(self.LOCAIS):
            botao = Botao(
                (
                    self.PAINEL_LISTA.x + 20,
                    self.PAINEL_LISTA.y + 52 + indice * 49,
                    self.PAINEL_LISTA.w - 40,
                    42,
                ),
                nome,
                variacao="opcao",
                tamanho_fonte=14,
                alinhamento="esquerda",
                padding=(38, 6),
                prefixo=f"{indice + 1:02d}",
                raio=6,
                uma_linha=True,
            )
            self.botoes_locais.append((botao, local_id))

    def sair(self):
        self.botoes_locais = []
        self.botao_menu = None
        self.local_foco = None

    def processar_evento(self, evento):
        if self.botao_menu is not None and self.botao_menu.processar_evento(evento):
            self.jogo.voltar_menu()
            return

        for botao, local_id in self.botoes_locais:
            if botao.processar_evento(evento):
                if not self.jogo.acessar_local(local_id):
                    self.jogo.notificar("Este local ainda não está disponível.")
                return

    def atualizar(self, delta):
        pos = self.jogo.pos_mouse()
        if self.botao_menu is not None:
            self.botao_menu.atualizar(pos)

        foco = None
        for botao, local_id in self.botoes_locais:
            botao.atualizar(pos)
            if botao.hover:
                foco = local_id

        if foco is not None:
            self.local_foco = foco

    def desenhar(self, superficie):
        fundo(superficie, "ilha.png", 122)
        estilo.aplicar_vinheta(superficie)

        estilo.desenhar_texto_espacado(
            superficie,
            "Arquipélago congelado",
            estilo.fonte("ui", 11, True),
            estilo.GELO,
            (56, 30),
        )
        estilo.desenhar_texto(
            superficie,
            "MAPA DA ILHA",
            estilo.fonte("titulo", 38, True),
            estilo.TEXTO,
            (54, 44),
        )
        estilo.desenhar_texto(
            superficie,
            "Escolha um local para investigar",
            estilo.fonte("corpo", 16),
            estilo.TEXTO_SUAVE,
            (56, 94),
        )

        if self.botao_menu is not None:
            self.botao_menu.desenhar(superficie)

        self._desenhar_lista(superficie)
        self._desenhar_previa(superficie)

    def _desenhar_lista(self, superficie):
        painel = self.PAINEL_LISTA
        estilo.desenhar_painel(
            superficie,
            painel,
            cor=(14, 24, 34),
            borda=estilo.BORDA,
            alpha=232,
        )

        estilo.desenhar_texto_espacado(
            superficie,
            "Locais da ilha",
            estilo.fonte("ui", 10, True),
            estilo.TEXTO_FRACO,
            (painel.x + 20, painel.y + 16),
        )
        estilo.desenhar_texto(
            superficie,
            f"{len(self.botoes_locais):02d}",
            estilo.fonte("mono", 12, True),
            estilo.TEXTO_FRACO,
            (painel.right - 20, painel.y + 15),
            alinhamento="direita",
        )
        estilo.desenhar_divisoria(
            superficie,
            painel.x + 20,
            painel.right - 20,
            painel.y + 40,
            estilo.BORDA,
            140,
        )

        locais = self.jogo.partida.mapa.locais if self.jogo.partida else {}

        for botao, local_id in self.botoes_locais:
            botao.desenhar(superficie)

            local = locais.get(local_id)
            if local is not None and local.visitado:
                pygame.draw.circle(
                    superficie,
                    estilo.DOURADO,
                    (botao.rect.right - 14, botao.rect.centery),
                    3,
                )

        estilo.desenhar_texto(
            superficie,
            "Um ponto dourado indica locais já visitados.",
            estilo.fonte("ui", 10),
            estilo.TEXTO_FRACO,
            (painel.x + 20, painel.bottom - 24),
        )

    def _desenhar_previa(self, superficie):
        painel = self.PAINEL_PREVIA
        estilo.desenhar_painel(
            superficie,
            painel,
            cor=(13, 23, 32),
            borda=estilo.BORDA,
            alpha=226,
            sombra=False,
        )

        local = None
        if self.jogo.partida is not None and self.local_foco is not None:
            local = self.jogo.partida.mapa.locais.get(self.local_foco)

        estilo.desenhar_texto_espacado(
            superficie,
            "Local em destaque" if local else "Seleção de local",
            estilo.fonte("ui", 10, True),
            estilo.DOURADO if local else estilo.TEXTO_FRACO,
            (painel.x + 22, painel.y + 18),
        )

        if local is None:
            estilo.desenhar_paragrafo(
                superficie,
                "Passe o cursor sobre um local para ver detalhes. Clique para entrar na cena.",
                estilo.fonte("corpo", 16),
                estilo.TEXTO_SUAVE,
                (painel.x + 22, painel.y + 48, painel.w - 44, 90),
                espacamento=4,
            )
            return

        estilo.desenhar_texto(
            superficie,
            local.nome,
            estilo.fonte("titulo", 23, True),
            estilo.TEXTO,
            (painel.x + 22, painel.y + 40),
        )
        estilo.desenhar_paragrafo(
            superficie,
            local.descricao,
            estilo.fonte("corpo", 14),
            estilo.TEXTO_SUAVE,
            (painel.x + 22, painel.y + 74, painel.w - 44, 54),
            espacamento=3,
            limite_linhas=3,
        )

        rodape = "JÁ VISITADO" if local.visitado else "AINDA NÃO VISITADO"
        estilo.desenhar_texto(
            superficie,
            f"{rodape}   ·   {len(local.personagens)} PRESENÇA(S)",
            estilo.fonte("ui", 10, True),
            estilo.DOURADO_CLARO if local.visitado else estilo.TEXTO_FRACO,
            (painel.x + 22, painel.bottom - 26),
        )
