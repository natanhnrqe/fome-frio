"""Botão desenhado pela própria interface.

Um único componente concentra estados, tipografia e áreas clicáveis para que
nenhuma tela invente dimensões ou estilos diferentes.
"""

from __future__ import annotations

import pygame

from interface import estilo


class Botao:
    def __init__(
        self,
        rect,
        texto,
        variacao="secundario",
        tamanho_fonte=17,
        fonte_nome="ui",
        alinhamento="centro",
        padding=(16, 8),
        max_linhas=2,
        uma_linha=False,
        selecionado=False,
        habilitado=True,
        prefixo=None,
        raio=estilo.RAIO_PEQUENO,
    ):
        self.rect = pygame.Rect(rect)
        self.texto = str(texto)
        self.variacao = variacao
        self.tamanho_fonte = int(tamanho_fonte)
        self.fonte_nome = fonte_nome
        self.alinhamento = alinhamento
        self.padding = padding
        self.max_linhas = max_linhas
        self.uma_linha = uma_linha
        self.selecionado = bool(selecionado)
        self.habilitado = bool(habilitado)
        self.prefixo = str(prefixo) if prefixo is not None else None
        self.raio = raio

        self.hover = False
        self.pressionado = False
        self._linhas: list[str] = []
        self._fonte = estilo.fonte(fonte_nome, tamanho_fonte)
        self._preparar_texto()

    # ------------------------------------------------------------
    # Geometria e texto
    # ------------------------------------------------------------

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)
        self._preparar_texto()

    def set_text(self, texto):
        self.texto = str(texto)
        self._preparar_texto()

    def set_selecionado(self, selecionado):
        self.selecionado = bool(selecionado)

    def set_habilitado(self, habilitado):
        self.habilitado = bool(habilitado)
        if not self.habilitado:
            self.pressionado = False
            self.hover = False

    @property
    def largura_texto(self):
        largura = self.rect.w - self.padding[0] * 2
        if self.prefixo is not None:
            largura -= 38
        if self.variacao == "opcao":
            largura -= 26
        return max(1, largura)

    def _preparar_texto(self):
        tamanho = self.tamanho_fonte
        largura_disponivel = self.largura_texto

        while tamanho > 11:
            fonte_usada = estilo.fonte(self.fonte_nome, tamanho)
            if self.uma_linha:
                linhas = [self.texto]
                cabe = fonte_usada.size(self.texto)[0] <= largura_disponivel
            else:
                linhas = estilo.quebrar_texto(self.texto, fonte_usada, largura_disponivel)
                cabe = len(linhas) <= self.max_linhas

            if cabe:
                break

            tamanho -= 1

        fonte_usada = estilo.fonte(self.fonte_nome, tamanho)

        if self.uma_linha:
            linhas = [self.texto]
            if fonte_usada.size(self.texto)[0] > largura_disponivel:
                linhas = [self._encurtar(self.texto, fonte_usada, largura_disponivel)]
        else:
            linhas = estilo.quebrar_texto(self.texto, fonte_usada, largura_disponivel)
            if len(linhas) > self.max_linhas:
                linhas = linhas[: self.max_linhas]
                ultima = linhas[-1]
                linhas[-1] = self._encurtar(ultima + "…", fonte_usada, largura_disponivel)

        self._fonte = fonte_usada
        self._linhas = linhas

    @staticmethod
    def _encurtar(texto, fonte_usada, largura):
        resultado = texto
        while resultado and fonte_usada.size(resultado)[0] > largura:
            resultado = resultado[:-1]
        return resultado or "…"

    # ------------------------------------------------------------
    # Interação
    # ------------------------------------------------------------

    def contem(self, pos) -> bool:
        return self.habilitado and self.rect.collidepoint(pos)

    def atualizar(self, pos_mouse=None):
        if not self.habilitado:
            self.hover = False
            self.pressionado = False
            return

        if pos_mouse is None:
            pos_mouse = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(pos_mouse)

        if not self.hover:
            self.pressionado = False

    def processar_evento(self, evento) -> bool:
        """Retorna True no clique completo (pressionar e soltar dentro)."""
        if not self.habilitado:
            return False

        if evento.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(evento.pos)
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.pressionado = True
                self.hover = True
            else:
                self.pressionado = False
            return False

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            clicado = self.pressionado and self.rect.collidepoint(evento.pos)
            self.pressionado = False
            self.hover = self.rect.collidepoint(evento.pos)
            return clicado

        return False

    # ------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------

    def _paleta(self):
        if not self.habilitado:
            return (32, 38, 42), (62, 70, 75), (112, 119, 122)

        if self.variacao == "primario":
            if self.pressionado:
                return (158, 117, 55), (225, 186, 117), estilo.TEXTO_ESCURO
            if self.hover:
                return (221, 173, 98), (242, 210, 148), estilo.TEXTO_ESCURO
            return (193, 145, 75), (229, 191, 123), estilo.TEXTO_ESCURO

        if self.variacao == "perigo":
            if self.pressionado:
                return (51, 27, 25), (180, 98, 84), estilo.PERIGO_CLARO
            if self.hover:
                return (67, 34, 31), (209, 124, 107), (246, 201, 189)
            return (39, 25, 24), (143, 82, 70), estilo.PERIGO_CLARO

        if self.variacao == "fantasma":
            if self.pressionado:
                return (14, 22, 30), (135, 108, 62), estilo.DOURADO_CLARO
            if self.hover:
                return (24, 37, 48), (174, 139, 79), estilo.DOURADO_CLARO
            return (11, 18, 25), (56, 75, 89), estilo.TEXTO_SUAVE

        if self.variacao == "opcao":
            if self.pressionado:
                return (15, 25, 34), (207, 163, 91), estilo.DOURADO_CLARO
            if self.hover or self.selecionado:
                return (29, 45, 57), (207, 163, 91), estilo.TEXTO
            return (20, 33, 44), (58, 80, 96), (224, 219, 208)

        # secundário (padrão)
        if self.pressionado:
            return (14, 24, 32), (150, 128, 86), estilo.DOURADO_CLARO
        if self.hover:
            return (29, 46, 60), (150, 179, 196), estilo.TEXTO
        return (19, 31, 42), (57, 79, 95), estilo.TEXTO

    def desenhar(self, superficie):
        fundo_cor, borda_cor, texto_cor = self._paleta()
        rect = self.rect.copy()

        if self.pressionado:
            rect.y += 1

        camada = pygame.Surface(rect.size, pygame.SRCALPHA)
        raio = self.raio
        pygame.draw.rect(camada, (*fundo_cor, 246 if self.habilitado else 190),
                         camada.get_rect(), border_radius=raio)
        pygame.draw.rect(camada, (*borda_cor, 255), camada.get_rect(), 1,
                         border_radius=raio)

        if self.variacao == "primario" and self.habilitado:
            pygame.draw.line(camada, (255, 239, 204, 110),
                             (raio, 2), (rect.w - raio, 2))

        if (self.selecionado or (self.hover and self.variacao == "opcao")) and self.habilitado:
            pygame.draw.rect(camada, (*estilo.DOURADO, 255),
                             pygame.Rect(0, 0, 4, rect.h), border_radius=2)

        superficie.blit(camada, rect.topleft)

        if not self._linhas:
            return

        x_texto = rect.x + self.padding[0]
        largura_texto = self.largura_texto

        if self.prefixo is not None:
            fonte_prefixo = estilo.fonte("mono", max(10, self._fonte.get_height() - 3), True)
            prefixo_img = fonte_prefixo.render(self.prefixo, True,
                                               estilo.DOURADO if self.habilitado else estilo.TEXTO_FRACO)
            badge = pygame.Rect(rect.x + 9, rect.centery - 10, 28, 20)
            pygame.draw.rect(superficie, (9, 15, 21), badge, border_radius=4)
            pygame.draw.rect(superficie, (*estilo.BORDA, 200), badge, 1, border_radius=4)
            superficie.blit(prefixo_img, prefixo_img.get_rect(center=badge.center))
            x_texto += 36

        if self.variacao == "opcao":
            seta = estilo.fonte("ui", max(13, self._fonte.get_height() - 2), True).render(
                "›", True, estilo.DOURADO if self.habilitado else estilo.TEXTO_FRACO
            )
            superficie.blit(seta, (rect.x + 12, rect.centery - seta.get_height() // 2))

        altura_linha = self._fonte.get_linesize()
        espacamento = 2
        total = len(self._linhas) * altura_linha + max(0, len(self._linhas) - 1) * espacamento
        y = rect.centery - total // 2

        for linha in self._linhas:
            imagem = self._fonte.render(linha, True, texto_cor)
            if self.alinhamento == "esquerda":
                x = x_texto
            elif self.alinhamento == "direita":
                x = rect.right - self.padding[0] - imagem.get_width()
            else:
                x = x_texto + (largura_texto - imagem.get_width()) // 2

            superficie.blit(imagem, (x, y))
            y += altura_linha + espacamento
