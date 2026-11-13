"""Personagem em cena: sprite proporcional e clicável.

O próprio personagem é o botão de conversa. A placa de nome aparece junto aos
pés, nunca sobre o rosto, e some quando a caixa de diálogo assume a interação.
"""

from __future__ import annotations

import pygame

from interface import estilo
from interface.recursos import retrato


class PersonagemCena:
    def __init__(self, jogo, personagem_id, centro_x, base_y, altura):
        self.jogo = jogo
        self.personagem_id = personagem_id
        self.personagem = jogo.partida.personagens.get(personagem_id)

        self.centro_x = int(centro_x)
        self.base_y = int(base_y)
        self.altura = int(altura)
        self.imagem = None
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.placa = pygame.Rect(0, 0, 1, 1)

        self.hover = False
        self.pressionado = False
        self._glow = None
        self._escuro = None

        self.reposicionar(centro_x, base_y, altura)

    # ------------------------------------------------------------
    # Geometria
    # ------------------------------------------------------------

    def reposicionar(self, centro_x, base_y, altura):
        self.centro_x = int(centro_x)
        self.base_y = int(base_y)
        self.altura = int(altura)

        self.imagem = retrato(self.personagem_id, self.altura)
        if self.imagem is None:
            self.rect = pygame.Rect(self.centro_x - 120, self.base_y - self.altura,
                                    240, self.altura)
        else:
            self.rect = self.imagem.get_rect(midbottom=(self.centro_x, self.base_y))

        self._atualizar_placa()
        self._preparar_silhuetas()

    def _atualizar_placa(self):
        nome = self.personagem.nome if self.personagem else self.personagem_id
        cargo = self.personagem.cargo if self.personagem else ""

        fonte_nome = estilo.fonte("titulo", 18, True)
        fonte_cargo = estilo.fonte("ui", 11)
        largura = max(fonte_nome.size(nome)[0], fonte_cargo.size(cargo)[0]) + 34
        largura = max(176, min(320, largura))

        self.placa = pygame.Rect(0, 0, largura, 48)
        self.placa.midbottom = (self.centro_x, self.base_y + 8)

    def _preparar_silhuetas(self):
        self._glow = None
        self._escuro = None
        if self.imagem is None:
            return

        mascara = pygame.mask.from_surface(self.imagem)
        self._glow = mascara.to_surface(
            setcolor=(*estilo.DOURADO_CLARO, 255),
            unsetcolor=(0, 0, 0, 0),
        )
        self._escuro = mascara.to_surface(
            setcolor=(4, 8, 12, 255),
            unsetcolor=(0, 0, 0, 0),
        )

    def contem(self, pos) -> bool:
        return self.rect.collidepoint(pos) or self.placa.collidepoint(pos)

    # ------------------------------------------------------------
    # Interação
    # ------------------------------------------------------------

    def atualizar(self, pos_mouse=None, interativo=True):
        if not interativo:
            self.hover = False
            self.pressionado = False
            return

        if pos_mouse is None:
            pos_mouse = pygame.mouse.get_pos()

        self.hover = self.contem(pos_mouse)
        if not self.hover:
            self.pressionado = False

    def processar_evento(self, evento, interativo=True) -> bool:
        if not interativo:
            return False

        if evento.type == pygame.MOUSEMOTION:
            self.hover = self.contem(evento.pos)
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.contem(evento.pos):
                self.pressionado = True
                self.hover = True
            else:
                self.pressionado = False
            return False

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            clicado = self.pressionado and self.contem(evento.pos)
            self.pressionado = False
            self.hover = self.contem(evento.pos)
            return clicado

        return False

    # ------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------

    def _desenhar_sombra(self, superficie):
        largura = max(70, round(self.rect.w * 0.68))
        altura = max(14, round(largura * 0.14))
        camada = pygame.Surface((largura + 8, altura + 8), pygame.SRCALPHA)
        pygame.draw.ellipse(
            camada,
            (0, 0, 0, 110),
            pygame.Rect(4, 4, largura, altura),
        )
        superficie.blit(
            camada,
            (self.rect.centerx - camada.get_width() // 2, self.base_y - altura // 2),
        )

    def _desenhar_brilho(self, superficie):
        if self._glow is None:
            return

        alpha = 46
        if self.hover:
            alpha = 78 + int(12 * abs(pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 22).x))

        self._glow.set_alpha(alpha)
        for deslocamento in ((-3, 0), (3, 0), (0, -3), (0, 3)):
            superficie.blit(self._glow, self.rect.move(deslocamento))

    def desenhar(self, superficie, falando=False, dim=False, mostrar_placa=True):
        if self.imagem is None:
            return

        self._desenhar_sombra(superficie)

        if self.hover or falando:
            self._desenhar_brilho(superficie)

        superficie.blit(self.imagem, self.rect)

        if dim:
            self._escuro.set_alpha(112)
            superficie.blit(self._escuro, self.rect)

        if mostrar_placa and not dim:
            self._desenhar_placa(superficie)

    def _desenhar_placa(self, superficie):
        rect = self.placa
        cor_borda = estilo.DOURADO if self.hover else estilo.BORDA
        camada = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(camada, (9, 16, 23, 232), camada.get_rect(), border_radius=6)
        pygame.draw.rect(camada, (*cor_borda, 255), camada.get_rect(), 1, border_radius=6)
        pygame.draw.rect(camada, (*estilo.DOURADO, 230), pygame.Rect(0, 8, 3, rect.h - 16),
                         border_radius=2)
        superficie.blit(camada, rect.topleft)

        nome = self.personagem.nome if self.personagem else self.personagem_id
        cargo = self.personagem.cargo if self.personagem else ""

        fonte_nome = estilo.fonte("titulo", 18, True)
        fonte_cargo = estilo.fonte("ui", 11)

        nome_img = fonte_nome.render(nome, True,
                                     estilo.DOURADO_CLARO if self.hover else estilo.TEXTO)
        cargo_img = fonte_cargo.render(cargo.upper(), True, estilo.TEXTO_FRACO)

        superficie.blit(nome_img, nome_img.get_rect(midtop=(rect.centerx, rect.y + 7)))
        superficie.blit(cargo_img, cargo_img.get_rect(midtop=(rect.centerx, rect.y + 29)))
