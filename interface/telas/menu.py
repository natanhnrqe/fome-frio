"""Menu inicial atmosférico, com cenário em tela cheia."""

from __future__ import annotations

import random

import pygame

from interface import estilo
from interface.componentes.botao import Botao
from interface.recursos import fundo


class _Neve:
    def __init__(self, quantidade=58):
        sorteio = random.Random(17)
        self.flocos = [
            {
                "x": sorteio.uniform(0, estilo.LARGURA),
                "y": sorteio.uniform(0, estilo.ALTURA),
                "raio": sorteio.choice((1, 1, 1, 2)),
                "velocidade": sorteio.uniform(8, 26),
                "deriva": sorteio.uniform(4, 18),
                "alpha": sorteio.randint(34, 100),
            }
            for _ in range(quantidade)
        ]

    def atualizar(self, delta):
        for floco in self.flocos:
            floco["y"] += floco["velocidade"] * delta
            floco["x"] += floco["deriva"] * delta
            if floco["y"] > estilo.ALTURA + 4:
                floco["y"] = -4
                floco["x"] = random.uniform(0, estilo.LARGURA)
            if floco["x"] > estilo.LARGURA + 4:
                floco["x"] = -4

    def desenhar(self, superficie):
        camada = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
        for floco in self.flocos:
            pygame.draw.circle(
                camada,
                (224, 235, 242, floco["alpha"]),
                (round(floco["x"]), round(floco["y"])),
                floco["raio"],
            )
        superficie.blit(camada, (0, 0))


class TelaMenu:
    def __init__(self, jogo):
        self.jogo = jogo
        self.botao_nova = None
        self.botao_sair = None
        self.neve = _Neve()

    def entrar(self):
        self.botao_nova = Botao(
            (88, 414, 344, 56),
            "NOVA INVESTIGAÇÃO",
            variacao="primario",
            tamanho_fonte=16,
            uma_linha=True,
        )
        self.botao_sair = Botao(
            (88, 484, 344, 50),
            "SAIR",
            variacao="fantasma",
            tamanho_fonte=14,
            uma_linha=True,
        )

    def sair(self):
        self.botao_nova = None
        self.botao_sair = None

    def processar_evento(self, evento):
        if self.botao_nova is not None and self.botao_nova.processar_evento(evento):
            self.jogo.iniciar_partida()
            return

        if self.botao_sair is not None and self.botao_sair.processar_evento(evento):
            self.jogo.encerrar()

    def atualizar(self, delta):
        self.neve.atualizar(delta)
        pos = self.jogo.pos_mouse()
        if self.botao_nova is not None:
            self.botao_nova.atualizar(pos)
        if self.botao_sair is not None:
            self.botao_sair.atualizar(pos)

    def desenhar(self, superficie):
        fundo(superficie, "ilha.png", 92)

        # Escurece a esquerda para dar suporte ao bloco de título.
        superficie.blit(
            estilo.gradiente_horizontal(
                (760, estilo.ALTURA), (5, 10, 15), (5, 10, 15), 205, 0
            ),
            (0, 0),
        )
        self.neve.desenhar(superficie)
        estilo.aplicar_vinheta(superficie)

        estilo.desenhar_texto_espacado(
            superficie,
            "Uma investigação em uma ilha congelada",
            estilo.fonte("ui", 12, True),
            estilo.GELO,
            (88, 174),
            espacamento=2,
        )

        sombra = estilo.fonte("titulo", 82, True).render("FOME E FRIO", True, (0, 0, 0))
        superficie.blit(sombra, (92, 206))
        estilo.desenhar_texto(
            superficie,
            "FOME E FRIO",
            estilo.fonte("titulo", 82, True),
            estilo.TEXTO,
            (88, 202),
        )

        pygame.draw.line(superficie, estilo.DOURADO, (90, 318), (210, 318), 2)
        estilo.desenhar_texto(
            superficie,
            "Dois corpos. Seis sobreviventes. Uma verdade sob o gelo.",
            estilo.fonte("corpo", 20),
            estilo.TEXTO_SUAVE,
            (90, 338),
        )

        if self.botao_nova is not None:
            self.botao_nova.desenhar(superficie)
        if self.botao_sair is not None:
            self.botao_sair.desenhar(superficie)

        estilo.desenhar_texto(
            superficie,
            "Uma visual novel de investigação",
            estilo.fonte("ui", 11),
            estilo.TEXTO_FRACO,
            (90, 574),
        )
        estilo.desenhar_texto(
            superficie,
            "ESC  SAIR",
            estilo.fonte("mono", 10, True),
            estilo.TEXTO_FRACO,
            (estilo.LARGURA - 90, 574),
            alinhamento="direita",
        )
