"""Tela de deduções sobre um cenário atmosférico."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao
from interface.componentes.diario import Diario
from interface.componentes.painel_deducao import PainelDeducao
from interface.componentes.painel_dicas import PainelDicas
from interface.componentes.painel_historico import PainelHistorico
from interface.recursos import fundo


class TelaInvestigacao:
    def __init__(self, jogo):
        self.jogo = jogo
        self.painel = PainelDeducao(jogo)
        self.dicas = PainelDicas(jogo)
        self.historico = PainelHistorico(jogo)
        self.diario = Diario(jogo)
        self.painel.ao_dica = self._abrir_dicas

        self.botao_voltar = None
        self.botao_diario = None
        self.botao_historico = None
        self.botao_resolver = None

    def entrar(self):
        self.painel.entrar()

        self.botao_voltar = Botao(
            (estilo.MARGEM, estilo.TOPO_Y, 150, estilo.TOPO_ALTURA),
            "VOLTAR AO LOCAL",
            variacao="fantasma",
            tamanho_fonte=11,
            uma_linha=True,
        )
        self.botao_diario = Botao(
            (estilo.LARGURA - estilo.MARGEM - 396, estilo.TOPO_Y, 110, estilo.TOPO_ALTURA),
            "DIÁRIO",
            variacao="secundario",
            tamanho_fonte=12,
            uma_linha=True,
        )
        self.botao_historico = Botao(
            (estilo.LARGURA - estilo.MARGEM - 278, estilo.TOPO_Y, 110, estilo.TOPO_ALTURA),
            "HISTÓRICO",
            variacao="secundario",
            tamanho_fonte=12,
            uma_linha=True,
        )
        self.botao_resolver = Botao(
            (estilo.LARGURA - estilo.MARGEM - 160, estilo.TOPO_Y, 160, estilo.TOPO_ALTURA),
            "RESOLVER CASO",
            variacao="primario",
            tamanho_fonte=12,
            uma_linha=True,
        )

    def sair(self):
        self.painel.sair()
        self.dicas.fechar()
        self.historico.fechar()
        self.diario.fechar()
        self.botao_voltar = None
        self.botao_diario = None
        self.botao_historico = None
        self.botao_resolver = None

    def _abrir_dicas(self):
        self.historico.fechar()
        self.diario.fechar()
        self.dicas.abrir(self.painel.REGRAS[self.painel.regra_indice])

    def _abrir_diario(self):
        self.historico.fechar()
        self.dicas.fechar()
        self.diario.abrir()

    def _abrir_historico(self):
        self.diario.fechar()
        self.dicas.fechar()
        self.historico.abrir()

    def processar_evento(self, evento):
        if self.dicas.aberto:
            self.dicas.processar_evento(evento)
            return

        if self.diario.aberto:
            self.diario.processar_evento(evento)
            return

        if self.historico.aberto:
            self.historico.processar_evento(evento)
            return

        if self.botao_voltar is not None and self.botao_voltar.processar_evento(evento):
            self.jogo.gerenciador_telas.mudar_tela("local")
            return

        if self.botao_diario is not None and self.botao_diario.processar_evento(evento):
            self._abrir_diario()
            return

        if self.botao_historico is not None and self.botao_historico.processar_evento(evento):
            self._abrir_historico()
            return

        if self.botao_resolver is not None and self.botao_resolver.processar_evento(evento):
            self.tentar_abrir_resolucao()
            return

        self.painel.processar_evento(evento)

    def atualizar(self, delta):
        pos = self.jogo.pos_mouse()

        if self.botao_voltar is not None:
            self.botao_voltar.atualizar(pos)
        if self.botao_diario is not None:
            self.botao_diario.atualizar(pos)
        if self.botao_historico is not None:
            self.botao_historico.atualizar(pos)
        if self.botao_resolver is not None:
            self.botao_resolver.atualizar(pos)

        self.diario.atualizar()
        self.dicas.atualizar_hover(pos)
        self.historico.atualizar_hover(pos)
        self.diario.atualizar_hover(pos)

        if not (self.dicas.aberto or self.diario.aberto or self.historico.aberto):
            self.painel.atualizar_hover(pos)

    def desenhar(self, superficie):
        fundo(superficie, "conves.png", 176)
        estilo.aplicar_vinheta(superficie)

        self.painel.desenhar(superficie)

        if self.botao_voltar is not None:
            self.botao_voltar.desenhar(superficie)
        if self.botao_diario is not None:
            self.botao_diario.desenhar(superficie)
        if self.botao_historico is not None:
            self.botao_historico.desenhar(superficie)
        if self.botao_resolver is not None:
            self.botao_resolver.desenhar(superficie)

        self.historico.desenhar(superficie)
        self.diario.desenhar(superficie)
        self.dicas.desenhar(superficie)

    def tentar_abrir_resolucao(self):
        resultado = self.jogo.partida.tentar_resolver()

        if resultado["resolvido"]:
            self.jogo.gerenciador_telas.mudar_tela("resolucao")
        else:
            pendencias = ", ".join(resultado["pendencias"])
            self.painel.atualizar_status(
                f"Conclusões pendentes: {pendencias}. Volte às premissas e demonstre cada uma."
            )

    def tratar_escape(self) -> bool:
        if self.dicas.aberto:
            self.dicas.fechar()
            return True
        if self.diario.aberto:
            self.diario.fechar()
            return True
        if self.historico.aberto:
            self.historico.fechar()
            return True
        return False
