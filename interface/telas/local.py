"""Cena de local: cenário, personagens e caixa de diálogo."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao
from interface.componentes.diario import Diario
from interface.componentes.painel_dialogo import PainelDialogo
from interface.componentes.personagem import PersonagemCena
from interface.recursos import fundo


class TelaLocal:
    FUNDOS = {
        "cozinha": "cozinha.png",
        "sala_capitao": "conves.png",
        "caldeira": "caldeira.png",
        "enfermaria": "enfermaria.png",
        "passadico": "passadico_navegante.png",
        "alojamentos": "comodos_tripulacao.png",
        "farol": "ilha.png",
        "caverna": "ilha.png",
        "casa_abandonada": "deposito.png",
    }

    def __init__(self, jogo):
        self.jogo = jogo
        self.local = None
        self.painel_dialogo = PainelDialogo(jogo)
        self.diario = Diario(jogo)

        self.personagens_cena: list[PersonagemCena] = []
        self.botoes = []
        self.botao_investigar = None
        self.botao_diario = None
        self.botao_deducao = None
        self.botao_voltar = None
        self._layout_atual = None

    # ------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------

    def entrar(self):
        self.limpar_botoes()
        self.painel_dialogo.fechar()
        self.diario.fechar()
        self._layout_atual = None

        self.criar_botoes()
        self.criar_personagens()
        self._aplicar_layout()

    def criar_botoes(self):
        self.botao_voltar = Botao(
            (estilo.MARGEM, estilo.TOPO_Y, 106, estilo.TOPO_ALTURA),
            "MAPA",
            variacao="fantasma",
            tamanho_fonte=12,
            uma_linha=True,
        )
        self.botao_diario = Botao(
            (estilo.LARGURA - estilo.MARGEM - 118, estilo.TOPO_Y, 118, estilo.TOPO_ALTURA),
            "DIÁRIO",
            variacao="secundario",
            tamanho_fonte=12,
            uma_linha=True,
        )
        self.botao_deducao = Botao(
            (estilo.LARGURA - estilo.MARGEM - 118 - 146, estilo.TOPO_Y, 136, estilo.TOPO_ALTURA),
            "DEDUÇÕES",
            variacao="secundario",
            tamanho_fonte=12,
            uma_linha=True,
        )
        self.botao_investigar = Botao(
            (1004, 646, 240, 46),
            "INVESTIGAR LOCAL",
            variacao="primario",
            tamanho_fonte=14,
            uma_linha=True,
        )

        self.botoes = [
            self.botao_voltar,
            self.botao_diario,
            self.botao_deducao,
            self.botao_investigar,
        ]

    def criar_personagens(self):
        self.personagens_cena = []

        if self.local is None or self.jogo.partida is None:
            return

        for personagem_id in self.local.personagens:
            if personagem_id not in self.jogo.partida.personagens:
                continue
            self.personagens_cena.append(
                PersonagemCena(self.jogo, personagem_id, 300, 700, 560)
            )

    # ------------------------------------------------------------
    # Layout adaptativo
    # ------------------------------------------------------------

    def _aplicar_layout(self, forcar=False):
        aberto = self.painel_dialogo.aberto
        ativo = self.painel_dialogo.personagem_id if aberto else None
        estado = (aberto, len(self.personagens_cena), ativo)
        if not forcar and estado == self._layout_atual:
            return

        quantidade = len(self.personagens_cena)

        if aberto:
            # O falante permanece em altura cheia, apoiado no chão, à direita
            # da caixa de diálogo. A caixa não o empurra para cima.
            altura = estilo.ALTURA_PERSONAGEM_DIALOGO
            base_y = estilo.BASE_PERSONAGEM_DIALOGO
        else:
            altura = {1: 560, 2: 540}.get(quantidade, 430)
            base_y = 700

        # Dois personagens lado a lado precisam de espaço para não se
        # sobrepor. No diálogo, o falante fica à direita e o restante
        # permanece ao fundo, atrás da caixa, reduzido apenas por oclusão.
        if quantidade == 1:
            centros = [1050] if aberto else [300]
        elif quantidade == 2:
            centros = [300, 1050] if aberto else [250, 670]
        elif quantidade == 3:
            centros = [260, 470, 1050] if aberto else [160, 480, 800]
        else:
            espaco = 205 if aberto else 300
            inicio = 240 if aberto else 250
            centros = [inicio + indice * espaco for indice in range(quantidade - 1)]
            if aberto:
                centros.append(1050)
            else:
                centros = [inicio + indice * espaco for indice in range(quantidade)]

        personagens = list(self.personagens_cena)
        if aberto and ativo is not None:
            # O falante é o último da lista: fica à direita e é desenhado
            # por cima dos coadjuvantes.
            personagens.sort(key=lambda p: p.personagem_id == ativo)

        for personagem, centro in zip(personagens, centros):
            personagem.reposicionar(centro, base_y, altura)

        self._layout_atual = estado

    def _personagem_ativo(self):
        if self.painel_dialogo.aberto:
            return self.painel_dialogo.personagem_id
        return None

    # ------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------

    def processar_evento(self, evento):
        if self.diario.aberto:
            self.diario.processar_evento(evento)
            return

        if self.botao_voltar is not None and self.botao_voltar.processar_evento(evento):
            self.jogo.voltar_mapa()
            return

        if self.botao_diario is not None and self.botao_diario.processar_evento(evento):
            self.diario.abrir()
            return

        if self.botao_deducao is not None and self.botao_deducao.processar_evento(evento):
            self.jogo.abrir_deducoes()
            return

        if self.painel_dialogo.aberto:
            self.painel_dialogo.processar_evento(evento)
            return

        if self.botao_investigar is not None and self.botao_investigar.processar_evento(evento):
            self.investigar()
            return

        for personagem in self.personagens_cena:
            if personagem.processar_evento(evento):
                self.painel_dialogo.abrir(personagem.personagem_id)
                self._aplicar_layout()
                return

    def investigar(self):
        resultado = self.jogo.partida.investigar_local()

        if not resultado:
            return

        novas = resultado.get("pistas_novas", [])
        total = len(resultado.get("pistas_encontradas", []))
        if novas:
            self.jogo.notificar(
                f"{len(novas)} nova(s) pista(s) encontrada(s). Consulte o diário."
            )
        else:
            self.jogo.notificar(
                f"Você examinou o local. {total} pista(s) já conhecida(s); nenhuma novidade."
            )

    def tratar_escape(self) -> bool:
        if self.diario.aberto:
            self.diario.fechar()
            return True
        if self.painel_dialogo.aberto:
            self.painel_dialogo.fechar()
            self._aplicar_layout()
            return True
        return False

    # ------------------------------------------------------------
    # Atualização
    # ------------------------------------------------------------

    def atualizar(self, delta):
        self._aplicar_layout()
        self.diario.atualizar()

        pos = self.jogo.pos_mouse()

        if self.botao_voltar is not None:
            self.botao_voltar.atualizar(pos)
        if self.botao_diario is not None:
            self.botao_diario.atualizar(pos)
        if self.botao_deducao is not None:
            self.botao_deducao.atualizar(pos)
        if self.botao_investigar is not None:
            self.botao_investigar.atualizar(pos)

        self.painel_dialogo.atualizar_hover(pos)
        self.diario.atualizar_hover(pos)

        interativo = not self.painel_dialogo.aberto and not self.diario.aberto
        for personagem in self.personagens_cena:
            personagem.atualizar(pos, interativo)

    # ------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------

    def desenhar(self, superficie):
        nome_local = getattr(self.local, "id", "ilha") if self.local else "ilha"
        fundo(superficie, self.FUNDOS.get(nome_local, "ilha.png"), 124)
        estilo.aplicar_vinheta(superficie)

        if self.local is not None:
            self._desenhar_cabecalho(superficie)

        self._desenhar_personagens(superficie)

        if self.botao_voltar is not None:
            self.botao_voltar.desenhar(superficie)
        if self.botao_diario is not None:
            self.botao_diario.desenhar(superficie)
        if self.botao_deducao is not None:
            self.botao_deducao.desenhar(superficie)

        if not self.painel_dialogo.aberto and self.botao_investigar is not None:
            self.botao_investigar.desenhar(superficie)

        if not self.personagens_cena and not self.painel_dialogo.aberto:
            self._desenhar_local_vazio(superficie)

        self.painel_dialogo.desenhar(superficie)
        self.diario.desenhar(superficie)

    def _desenhar_cabecalho(self, superficie):
        estilo.desenhar_texto_espacado(
            superficie,
            "Cena do local",
            estilo.fonte("ui", 10, True),
            estilo.GELO,
            (160, 24),
        )
        estilo.desenhar_texto(
            superficie,
            self.local.nome.upper(),
            estilo.fonte("titulo", 30, True),
            estilo.TEXTO,
            (158, 38),
        )
        estilo.desenhar_texto(
            superficie,
            self.local.descricao,
            estilo.fonte("corpo", 14),
            estilo.TEXTO_SUAVE,
            (160, 76),
        )

    def _desenhar_personagens(self, superficie):
        ativo = self._personagem_ativo()
        aberto = self.painel_dialogo.aberto

        personagens = list(self.personagens_cena)
        if aberto and ativo is not None:
            # Desenha o falante por último para mantê-lo à frente.
            personagens.sort(key=lambda p: p.personagem_id == ativo)

        for personagem in personagens:
            falando = personagem.personagem_id == ativo
            dim = aberto and not falando
            personagem.desenhar(
                superficie,
                falando=falando,
                dim=dim,
                mostrar_placa=not aberto,
            )

    def _desenhar_local_vazio(self, superficie):
        rect = pygame.Rect(390, 298, 500, 118)
        estilo.desenhar_painel(
            superficie,
            rect,
            cor=(14, 24, 34),
            borda=estilo.BORDA,
            alpha=220,
            sombra=False,
        )
        estilo.desenhar_texto_espacado(
            superficie,
            "Cena silenciosa",
            estilo.fonte("ui", 10, True),
            estilo.DOURADO,
            (rect.x + 24, rect.y + 18),
        )
        estilo.desenhar_paragrafo(
            superficie,
            "Nenhum sobrevivente está neste local. Examine o ambiente em busca de pistas.",
            estilo.fonte("corpo", 17),
            estilo.TEXTO,
            (rect.x + 24, rect.y + 42, rect.w - 48, 62),
            espacamento=4,
        )

    def limpar_botoes(self):
        self.botoes = []
        self.botao_investigar = None
        self.botao_diario = None
        self.botao_deducao = None
        self.botao_voltar = None
        self.personagens_cena = []

    def sair(self):
        self.limpar_botoes()
        self.painel_dialogo.fechar()
        self.diario.fechar()
        self._layout_atual = None
