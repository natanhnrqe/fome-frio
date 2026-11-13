"""Histórico das premissas e deduções, em modal com rolagem."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao


class PainelHistorico:
    PAINEL = pygame.Rect(220, 80, 840, 560)
    AREA = pygame.Rect(252, 180, 776, 384)

    def __init__(self, jogo):
        self.jogo = jogo
        self.aberto = False
        self.entradas = []
        self.rolagem = 0
        self.botao_fechar = None

    def abrir(self):
        if self.aberto:
            return

        self.aberto = True
        self.rolagem = 0
        self.entradas = self._formatar_historico(
            self.jogo.partida.obter_historico_deducoes()
        )
        self.botao_fechar = Botao(
            (self.PAINEL.centerx - 80, self.PAINEL.bottom - 58, 160, 38),
            "FECHAR",
            variacao="secundario",
            tamanho_fonte=13,
            uma_linha=True,
        )

    def fechar(self):
        if not self.aberto:
            return
        self.aberto = False
        self.entradas = []
        self.rolagem = 0
        self.botao_fechar = None

    # ------------------------------------------------------------
    # Conteúdo
    # ------------------------------------------------------------

    def _formatar_historico(self, historico):
        entradas = []

        for item in historico or []:
            tipo = item.get("tipo")

            if tipo == "premissa":
                entradas.append({
                    "etiqueta": "PREMISSA",
                    "origem": str(item.get("origem", "")),
                    "expressao": estilo.formatar_logica(item.get("expressao", "")),
                    "cor": estilo.GELO,
                })
            elif tipo == "deducao":
                regra = str(item.get("regra", "")).replace("_", " ").upper()
                premissas = item.get("premissas", [])
                resultado = item.get("resultado", "")
                expressao = " · ".join(
                    estilo.formatar_logica(p) for p in premissas
                )
                if expressao:
                    expressao += f"  ⇒  {estilo.formatar_logica(resultado)}"
                else:
                    expressao = estilo.formatar_logica(resultado)
                entradas.append({
                    "etiqueta": f"DEDUÇÃO · {regra}",
                    "origem": "Regra aplicada",
                    "expressao": expressao,
                    "cor": estilo.DOURADO_CLARO,
                })
            elif tipo == "deducao_registrada":
                entradas.append({
                    "etiqueta": "DEDUÇÃO REGISTRADA",
                    "origem": "Nova premissa demonstrada",
                    "expressao": estilo.formatar_logica(item.get("resultado", "")),
                    "cor": estilo.SUCESSO,
                })

        return entradas

    def _altura_total(self):
        if not self.entradas:
            return 0
        return len(self.entradas) * 76 + (len(self.entradas) - 1) * 8

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
                max(0, self.rolagem - evento.y * 48),
            )
            return True

        if self.botao_fechar is not None and self.botao_fechar.processar_evento(evento):
            self.fechar()
            return True

        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return True

        return False

    def atualizar_hover(self, pos_mouse=None):
        if self.aberto and self.botao_fechar is not None:
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
            "Registro lógico",
            estilo.fonte("ui", 11, True),
            estilo.TEXTO_FRACO,
            (self.PAINEL.x + 32, self.PAINEL.y + 22),
        )
        estilo.desenhar_texto(
            superficie,
            "HISTÓRICO DE DEDUÇÕES",
            estilo.fonte("titulo", 30, True),
            estilo.TEXTO,
            (self.PAINEL.x + 32, self.PAINEL.y + 40),
        )
        estilo.desenhar_texto(
            superficie,
            f"{len(self.entradas):02d} REGISTROS",
            estilo.fonte("ui", 11, True),
            estilo.TEXTO_FRACO,
            (self.PAINEL.right - 32, self.PAINEL.y + 52),
            alinhamento="direita",
        )
        estilo.desenhar_divisoria(
            superficie,
            self.PAINEL.x + 32,
            self.PAINEL.right - 32,
            self.PAINEL.y + 88,
            estilo.BORDA,
            160,
        )

        self._desenhar_entradas(superficie)
        self._desenhar_barra_rolagem(superficie)

        if self.botao_fechar is not None:
            self.botao_fechar.desenhar(superficie)

    def _desenhar_entradas(self, superficie):
        if not self.entradas:
            fonte = estilo.fonte("corpo", 18)
            imagem = fonte.render("Nenhuma dedução registrada ainda.", True,
                                  estilo.TEXTO_FRACO)
            superficie.blit(imagem, imagem.get_rect(center=self.AREA.center))
            return

        recorte_anterior = superficie.get_clip()
        superficie.set_clip(self.AREA)

        y = self.AREA.y - self.rolagem
        for entrada in self.entradas:
            rect = pygame.Rect(self.AREA.x, y, self.AREA.w - 22, 76)
            if rect.bottom >= self.AREA.y and rect.y <= self.AREA.bottom:
                self._desenhar_entrada(superficie, rect, entrada)
            y += 84

        superficie.set_clip(recorte_anterior)

    def _desenhar_entrada(self, superficie, rect, entrada):
        estilo.desenhar_painel(
            superficie,
            rect,
            cor=(13, 22, 30),
            borda=estilo.BORDA,
            raio=7,
            alpha=210,
            sombra=False,
        )
        pygame.draw.rect(
            superficie,
            entrada["cor"],
            pygame.Rect(rect.x, rect.y + 10, 3, rect.h - 20),
            border_radius=2,
        )

        estilo.desenhar_texto(
            superficie,
            entrada["etiqueta"],
            estilo.fonte("ui", 10, True),
            entrada["cor"],
            (rect.x + 18, rect.y + 10),
        )
        estilo.desenhar_texto(
            superficie,
            entrada["origem"],
            estilo.fonte("ui", 9),
            estilo.TEXTO_FRACO,
            (rect.right - 14, rect.y + 11),
            alinhamento="direita",
        )

        fonte_expr = estilo.fonte("logica", 13, True)
        linhas = estilo.quebrar_texto(entrada["expressao"], fonte_expr, rect.w - 36)
        y = rect.y + 30
        for linha in linhas[:2]:
            imagem = fonte_expr.render(linha, True, estilo.TEXTO)
            superficie.blit(imagem, (rect.x + 18, y))
            y += 17

    def _desenhar_barra_rolagem(self, superficie):
        if self._limite_rolagem() <= 0:
            return

        trilho = pygame.Rect(self.AREA.right - 10, self.AREA.y, 4, self.AREA.h)
        pygame.draw.rect(superficie, (34, 48, 60), trilho, border_radius=2)

        proporcao = self.AREA.h / self._altura_total()
        altura = max(28, int(self.AREA.h * proporcao))
        deslocamento = int(
            (self.AREA.h - altura) * (self.rolagem / self._limite_rolagem())
        )
        polegar = pygame.Rect(trilho.x, trilho.y + deslocamento, trilho.w, altura)
        pygame.draw.rect(superficie, estilo.DOURADO_ESCURO, polegar, border_radius=2)
