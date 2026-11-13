"""Acusação final: cartões de suspeitos e painel de veredito."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao
from interface.recursos import fundo, recorte_rosto


class _CartaoSuspeito:
    def __init__(self, jogo, personagem_id, personagem, rect):
        self.jogo = jogo
        self.personagem_id = personagem_id
        self.personagem = personagem
        self.rect = pygame.Rect(rect)
        self.retrato = recorte_rosto(personagem_id, (66, 86))
        self.hover = False
        self.pressionado = False
        self.selecionado = False
        self.habilitado = True

    def contem(self, pos):
        return self.habilitado and self.rect.collidepoint(pos)

    def atualizar(self, pos_mouse=None):
        if pos_mouse is None:
            pos_mouse = pygame.mouse.get_pos()
        self.hover = self.contem(pos_mouse)
        if not self.hover:
            self.pressionado = False

    def processar_evento(self, evento):
        if not self.habilitado:
            return False

        if evento.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(evento.pos)
            return False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.pressionado = True
                self.hover = True
            return False

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            clicado = self.pressionado and self.rect.collidepoint(evento.pos)
            self.pressionado = False
            return clicado

        return False

    def desenhar(self, superficie, dim=False):
        rect = self.rect
        borda = estilo.DOURADO if (self.selecionado or self.hover) else estilo.BORDA
        cor = (27, 43, 55) if (self.selecionado or self.hover) else (17, 28, 38)

        estilo.desenhar_painel(
            superficie,
            rect,
            cor=cor,
            borda=borda,
            raio=8,
            alpha=236 if not dim else 150,
            sombra=False,
            brilho_superior=False,
        )

        if self.selecionado:
            pygame.draw.rect(
                superficie,
                estilo.DOURADO,
                pygame.Rect(rect.x, rect.y + 10, 3, rect.h - 20),
                border_radius=2,
            )

        if self.retrato is not None:
            superficie.blit(self.retrato, (rect.x + 12, rect.y + 20))

        nome = self.personagem.nome
        fonte_nome = estilo.fonte("titulo", 17, True)
        linhas = estilo.quebrar_texto(nome, fonte_nome, rect.w - 98)
        y = rect.y + 28
        for linha in linhas[:2]:
            imagem = fonte_nome.render(linha, True, estilo.TEXTO if not dim else estilo.TEXTO_FRACO)
            superficie.blit(imagem, (rect.x + 90, y))
            y += fonte_nome.get_linesize()

        cargo = self.personagem.cargo.upper()
        cargo_img = estilo.fonte("ui", 9, True).render(
            cargo, True, estilo.TEXTO_FRACO
        )
        superficie.blit(cargo_img, (rect.x + 90, rect.y + 74))

        if self.selecionado:
            marcador = estilo.fonte("ui", 10, True).render(
                "SELECIONADO", True, estilo.DOURADO_CLARO
            )
            superficie.blit(marcador, (rect.x + 90, rect.y + 94))

        if dim:
            superficie.blit(
                estilo.overlay(rect.size, (6, 10, 14), 92),
                rect.topleft,
            )


class TelaResolucao:
    CAUSAS = {
        "ataque_de_urso": "Ataque de urso",
        "hipotermia": "Hipotermia fatal",
        "fome": "Inanição",
        "acidente": "Acidente",
    }

    def __init__(self, jogo):
        self.jogo = jogo
        self.suspeito_selecionado = None
        self.resultado = None
        self.status = "Selecione um suspeito."
        self.cartoes = []
        self.botao_confirmar = None
        self.botao_voltar = None
        self.botao_nova = None
        self.botao_menu = None
        self.verdade = None

    # ------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------

    def entrar(self):
        self.suspeito_selecionado = None
        self.resultado = None
        self.status = "Selecione um suspeito."
        self.cartoes = []
        self.verdade = None

        self.botao_voltar = Botao(
            (estilo.MARGEM, estilo.TOPO_Y, 118, estilo.TOPO_ALTURA),
            "VOLTAR",
            variacao="fantasma",
            tamanho_fonte=12,
            uma_linha=True,
        )
        self.botao_confirmar = Botao(
            (440, 502, 400, 52),
            "CONFIRMAR ACUSAÇÃO",
            variacao="primario",
            tamanho_fonte=15,
            uma_linha=True,
        )
        self.botao_nova = None
        self.botao_menu = None

        personagens = list(self.jogo.partida.personagens.items())
        for indice, (personagem_id, personagem) in enumerate(personagens[:8]):
            coluna = indice % 4
            linha = indice // 4
            rect = pygame.Rect(73 + coluna * 288, 158 + linha * 140, 270, 126)
            self.cartoes.append(
                _CartaoSuspeito(self.jogo, personagem_id, personagem, rect)
            )

    def sair(self):
        self.cartoes = []
        self.botao_confirmar = None
        self.botao_voltar = None
        self.botao_nova = None
        self.botao_menu = None
        self.suspeito_selecionado = None
        self.resultado = None
        self.verdade = None

    # ------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------

    def processar_evento(self, evento):
        if self.resultado is not None:
            if self.botao_nova is not None and self.botao_nova.processar_evento(evento):
                self.jogo.iniciar_partida()
                return
            if self.botao_menu is not None and self.botao_menu.processar_evento(evento):
                self.jogo.voltar_menu()
                return
            return

        if self.botao_voltar is not None and self.botao_voltar.processar_evento(evento):
            self.jogo.gerenciador_telas.mudar_tela("investigacao")
            return

        for cartao in self.cartoes:
            if cartao.processar_evento(evento):
                self.suspeito_selecionado = cartao.personagem_id
                for outro in self.cartoes:
                    outro.selecionado = outro is cartao
                self.status = f"Suspeito selecionado: {cartao.personagem.nome}"
                return

        if self.botao_confirmar is not None and self.botao_confirmar.processar_evento(evento):
            self.confirmar_acusacao()

    def atualizar(self, delta):
        pos = self.jogo.pos_mouse()
        if self.botao_voltar is not None:
            self.botao_voltar.atualizar(pos)
        if self.botao_confirmar is not None:
            self.botao_confirmar.atualizar(pos)
        if self.botao_nova is not None:
            self.botao_nova.atualizar(pos)
        if self.botao_menu is not None:
            self.botao_menu.atualizar(pos)

        for cartao in self.cartoes:
            cartao.atualizar(pos)

    # ------------------------------------------------------------
    # Acusação
    # ------------------------------------------------------------

    def confirmar_acusacao(self):
        if self.suspeito_selecionado is None:
            self.status = "Selecione um suspeito primeiro."
            return

        validacao = self.jogo.partida.tentar_resolver()
        if not validacao["resolvido"]:
            self.status = "Ainda existem conclusões pendentes."
            self.jogo.gerenciador_telas.mudar_tela("investigacao")
            return

        caso = self.jogo.partida.caso
        personagens = self.jogo.partida.personagens

        def obter_nome(personagem_id):
            personagem = personagens.get(personagem_id)
            return personagem.nome if personagem is not None else personagem_id

        self.resultado = self.suspeito_selecionado == caso.assassino_id
        self.status = (
            "VOCÊ RESOLVEU O CASO!" if self.resultado
            else "SUA ACUSAÇÃO ESTAVA INCORRETA."
        )
        self.verdade = {
            "assassino": obter_nome(caso.assassino_id),
            "vitima_assassinato": obter_nome(caso.vitima_assassinato_id),
            "vitima_secundaria": obter_nome(caso.vitima_secundaria_id),
            "causa": self.CAUSAS.get(caso.causa_morte_secundaria,
                                     caso.causa_morte_secundaria.replace("_", " ").capitalize()),
        }

        for cartao in self.cartoes:
            cartao.habilitado = False

        self.botao_confirmar.set_habilitado(False)
        self.botao_voltar.set_habilitado(False)

        self.botao_nova = Botao(
            (440, 548, 190, 46),
            "NOVA PARTIDA",
            variacao="primario",
            tamanho_fonte=13,
            uma_linha=True,
        )
        self.botao_menu = Botao(
            (650, 548, 190, 46),
            "MENU",
            variacao="secundario",
            tamanho_fonte=13,
            uma_linha=True,
        )

    # ------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------

    def desenhar(self, superficie):
        fundo(superficie, "conves.png", 158)
        estilo.aplicar_vinheta(superficie)

        estilo.desenhar_texto_espacado(
            superficie,
            "A verdade sob o gelo",
            estilo.fonte("ui", 10, True),
            estilo.GELO,
            (estilo.LARGURA // 2, 24),
        )
        estilo.desenhar_texto(
            superficie,
            "ACUSAÇÃO FINAL",
            estilo.fonte("titulo", 38, True),
            estilo.TEXTO,
            (estilo.LARGURA // 2, 40),
            alinhamento="centro",
        )
        estilo.desenhar_texto(
            superficie,
            "Quem você acredita ser o assassino?",
            estilo.fonte("corpo", 16),
            estilo.TEXTO_SUAVE,
            (estilo.LARGURA // 2, 92),
            alinhamento="centro",
        )

        if self.botao_voltar is not None:
            self.botao_voltar.desenhar(superficie)

        for cartao in self.cartoes:
            cartao.desenhar(superficie, dim=self.resultado is not None)

        if self.resultado is None:
            self._desenhar_status(superficie)
            self.botao_confirmar.desenhar(superficie)

        if self.resultado is not None:
            self._desenhar_resultado(superficie)

    def _desenhar_status(self, superficie):
        rect = pygame.Rect(340, 438, 600, 44)
        estilo.desenhar_painel(
            superficie,
            rect,
            cor=(13, 23, 32),
            borda=estilo.BORDA,
            raio=6,
            alpha=225,
            sombra=False,
        )
        cor = estilo.DOURADO_CLARO if self.suspeito_selecionado else estilo.TEXTO_SUAVE
        estilo.desenhar_texto(
            superficie,
            self.status,
            estilo.fonte("ui", 14),
            cor,
            (rect.centerx, rect.y + 11),
            alinhamento="centro",
        )

    def _desenhar_resultado(self, superficie):
        superficie.blit(estilo.overlay(superficie.get_size(), (3, 6, 10), 158), (0, 0))

        painel = pygame.Rect(240, 86, 800, 552)
        estilo.desenhar_painel(
            superficie,
            painel,
            cor=(16, 27, 37),
            borda=estilo.BORDA_CLARA,
            raio=12,
            alpha=252,
        )
        pygame.draw.line(
            superficie,
            estilo.DOURADO,
            (painel.x + 26, painel.y + 1),
            (painel.right - 26, painel.y + 1),
            2,
        )

        cor_veredito = estilo.SUCESSO if self.resultado else estilo.PERIGO_CLARO
        estilo.desenhar_texto_espacado(
            superficie,
            "Veredito da investigação",
            estilo.fonte("ui", 10, True),
            cor_veredito,
            (painel.centerx, painel.y + 30),
        )

        titulo = "VOCÊ RESOLVEU O CASO" if self.resultado else "A ACUSAÇÃO ESTAVA INCORRETA"
        estilo.desenhar_texto(
            superficie,
            titulo,
            estilo.fonte("titulo", 35, True),
            cor_veredito,
            (painel.centerx, painel.y + 52),
            alinhamento="centro",
        )

        subtitulo = (
            "A verdade veio à tona sob o gelo."
            if self.resultado else
            "O caso foi encerrado, mas não pela mão que você apontou."
        )
        estilo.desenhar_texto(
            superficie,
            subtitulo,
            estilo.fonte("corpo", 15),
            estilo.TEXTO_SUAVE,
            (painel.centerx, painel.y + 104),
            alinhamento="centro",
        )

        estilo.desenhar_divisoria(superficie, painel.x + 50, painel.right - 50,
                                 painel.y + 138, estilo.BORDA, 140)

        estilo.desenhar_texto_espacado(
            superficie,
            "O verdadeiro assassino",
            estilo.fonte("ui", 10, True),
            estilo.DOURADO,
            (painel.x + 50, painel.y + 158),
        )
        estilo.desenhar_texto(
            superficie,
            self.verdade["assassino"],
            estilo.fonte("titulo", 30, True),
            estilo.DOURADO_CLARO,
            (painel.x + 50, painel.y + 176),
        )

        coluna_y = painel.y + 238
        self._bloco_revelacao(
            superficie, painel.x + 50, coluna_y, 330,
            "Vítima do assassinato", self.verdade["vitima_assassinato"]
        )
        self._bloco_revelacao(
            superficie, painel.x + 420, coluna_y, 330,
            "Segunda vítima", self.verdade["vitima_secundaria"]
        )

        estilo.desenhar_texto_espacado(
            superficie,
            "Causa da segunda morte",
            estilo.fonte("ui", 10, True),
            estilo.TEXTO_FRACO,
            (painel.x + 50, painel.y + 316),
        )
        estilo.desenhar_texto(
            superficie,
            self.verdade["causa"],
            estilo.fonte("corpo", 22),
            estilo.TEXTO,
            (painel.x + 50, painel.y + 334),
        )

        pygame.draw.line(
            superficie,
            estilo.DOURADO_ESCURO,
            (painel.x + 50, painel.y + 384),
            (painel.right - 50, painel.y + 384),
            1,
        )

        if self.botao_nova is not None:
            self.botao_nova.desenhar(superficie)
        if self.botao_menu is not None:
            self.botao_menu.desenhar(superficie)

    def _bloco_revelacao(self, superficie, x, y, largura, rotulo, valor):
        estilo.desenhar_texto_espacado(
            superficie,
            rotulo,
            estilo.fonte("ui", 10, True),
            estilo.TEXTO_FRACO,
            (x, y),
        )
        linhas = estilo.quebrar_texto(valor, estilo.fonte("corpo", 20), largura)
        yy = y + 20
        for linha in linhas[:2]:
            imagem = estilo.fonte("corpo", 20).render(linha, True, estilo.TEXTO)
            superficie.blit(imagem, (x, yy))
            yy += 26

    def tratar_escape(self) -> bool:
        return False
