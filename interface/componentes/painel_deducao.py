"""Mesa de dedução: premissas, regras lógicas e verificação."""

from __future__ import annotations

import pygame

from interface import estilo
from interface.componentes.botao import Botao


class PainelDeducao:
    REGRAS = [
        ("modus_ponens", "MODUS PONENS",
         "Se A implica B e A é verdadeiro, então B é verdadeiro."),
        ("silogismo_disjuntivo", "SILOGISMO DISJUNTIVO",
         "Se A ou B, e um dos dois é falso, então o outro é verdadeiro."),
        ("conjuncao", "CONJUNÇÃO",
         "Combine duas premissas verdadeiras em uma única conjunção."),
    ]

    PAINEL_ESQUERDO = pygame.Rect(56, 148, 760, 404)
    PAINEL_DIREITO = pygame.Rect(836, 148, 388, 404)
    BARRA_STATUS = pygame.Rect(56, 566, 1168, 88)

    def __init__(self, jogo):
        self.jogo = jogo

        self.premissas = []
        self.selecionadas = []
        self.botoes = []

        self.pagina = 0
        self.itens_por_pagina = 8
        self.regra_indice = 0

        self.status = "Selecione duas premissas e escolha uma regra lógica."
        self.botao_regra = None
        self.botao_aplicar = None
        self.botao_dica = None
        self.botao_verificar = None
        self.botao_anterior = None
        self.botao_proxima = None
        self.ao_dica = None

    # ------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------

    def entrar(self):
        self.premissas = self.jogo.partida.obter_premissas()
        self.selecionadas.clear()
        self.pagina = 0
        self.status = "Selecione duas premissas e escolha uma regra lógica."
        self.regra_indice = 0

        self.botao_regra = Botao(
            (self.PAINEL_DIREITO.x + 24, self.PAINEL_DIREITO.y + 234, 340, 40),
            self._texto_regra(),
            variacao="secundario",
            tamanho_fonte=13,
            uma_linha=True,
        )
        self.botao_aplicar = Botao(
            (self.PAINEL_DIREITO.x + 24, self.PAINEL_DIREITO.y + 294, 340, 48),
            "APLICAR REGRA",
            variacao="primario",
            tamanho_fonte=15,
        )
        self.botao_dica = Botao(
            (self.PAINEL_DIREITO.x + 24, self.PAINEL_DIREITO.y + 350, 340, 40),
            "DICA DE MONTAGEM",
            variacao="secundario",
            tamanho_fonte=12,
            uma_linha=True,
        )
        self.botao_verificar = Botao(
            (self.BARRA_STATUS.right - 246, self.BARRA_STATUS.y + 20, 226, 48),
            "VERIFICAR CONCLUSÕES",
            variacao="secundario",
            tamanho_fonte=13,
            uma_linha=True,
        )

        self.botao_anterior = Botao(
            (self.PAINEL_ESQUERDO.x + 20, self.PAINEL_ESQUERDO.bottom - 44, 96, 30),
            "ANTERIOR",
            variacao="fantasma",
            tamanho_fonte=11,
            padding=(8, 4),
            uma_linha=True,
        )
        self.botao_proxima = Botao(
            (self.PAINEL_ESQUERDO.right - 116, self.PAINEL_ESQUERDO.bottom - 44, 96, 30),
            "PRÓXIMA",
            variacao="fantasma",
            tamanho_fonte=11,
            padding=(8, 4),
            uma_linha=True,
        )

        self.atualizar_botoes()

    def sair(self):
        self.limpar_botoes()
        self.botao_regra = None
        self.botao_aplicar = None
        self.botao_dica = None
        self.botao_verificar = None
        self.botao_anterior = None
        self.botao_proxima = None

    # ------------------------------------------------------------
    # Estado e conteúdo
    # ------------------------------------------------------------

    def _texto_regra(self):
        return self.REGRAS[self.regra_indice][1]

    def _total_paginas(self):
        return max(1, (len(self.premissas) + self.itens_por_pagina - 1) // self.itens_por_pagina)

    def limpar_botoes(self):
        self.botoes = []

    def atualizar_botoes(self):
        self.limpar_botoes()

        inicio = self.pagina * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina

        for indice, premissa in enumerate(self.premissas[inicio:fim]):
            indice_real = inicio + indice
            coluna = indice % 2
            linha = indice // 2

            botao = Botao(
                (
                    self.PAINEL_ESQUERDO.x + 20 + coluna * 366,
                    self.PAINEL_ESQUERDO.y + 54 + linha * 76,
                    354,
                    68,
                ),
                estilo.formatar_logica(premissa),
                variacao="opcao",
                tamanho_fonte=14,
                fonte_nome="logica",
                alinhamento="esquerda",
                padding=(40, 6),
                max_linhas=2,
                prefixo=f"{indice_real + 1:02d}",
                selecionado=indice_real in self.selecionadas,
            )
            self.botoes.append((botao, indice_real))

    def atualizar_premissas(self):
        self.premissas = self.jogo.partida.obter_premissas()
        self.selecionadas.clear()

        total_paginas = self._total_paginas()
        self.pagina = min(self.pagina, total_paginas - 1)
        self.atualizar_botoes()

    def atualizar_status(self, mensagem):
        self.status = mensagem

    # ------------------------------------------------------------
    # Regras
    # ------------------------------------------------------------

    def aplicar_regra(self):
        if len(self.selecionadas) != 2:
            self.atualizar_status("Selecione exatamente duas premissas para aplicar a regra.")
            return

        premissa1 = self.premissas[self.selecionadas[0]]
        premissa2 = self.premissas[self.selecionadas[1]]
        regra = self.REGRAS[self.regra_indice][0]

        try:
            resultado = self.jogo.partida.aplicar_regra(regra, premissa1, premissa2)
            if resultado is None:
                self.atualizar_status("Essa regra não se aplica às premissas selecionadas.")
                return

            self.atualizar_status(
                f"Dedução registrada: {estilo.formatar_logica(resultado)}"
            )
            self.atualizar_premissas()
        except (ValueError, TypeError) as erro:
            self.atualizar_status(str(erro))

    def tentar_resolver(self):
        try:
            resultado = self.jogo.partida.tentar_resolver()
            if resultado["resolvido"]:
                self.atualizar_status(resultado["mensagem"])
            else:
                pendencias = ", ".join(resultado["pendencias"])
                self.atualizar_status(
                    f"{resultado['mensagem']} Pendências: {pendencias}"
                )
        except (ValueError, TypeError) as erro:
            self.atualizar_status(str(erro))

    # ------------------------------------------------------------
    # Eventos
    # ------------------------------------------------------------

    def processar_evento(self, evento) -> bool:
        botoes = [botao for botao, _ in self.botoes]
        botoes.extend([
            self.botao_regra, self.botao_aplicar, self.botao_dica,
            self.botao_verificar, self.botao_anterior, self.botao_proxima,
        ])

        if evento.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            for botao in botoes:
                if botao is not None:
                    botao.processar_evento(evento)
            return False

        if evento.type != pygame.MOUSEBUTTONUP or evento.button != 1:
            return False

        for botao, indice in self.botoes:
            if botao.processar_evento(evento):
                if indice in self.selecionadas:
                    self.selecionadas.remove(indice)
                elif len(self.selecionadas) < 2:
                    self.selecionadas.append(indice)
                self.atualizar_botoes()
                return True

        if self.botao_regra is not None and self.botao_regra.processar_evento(evento):
            self.regra_indice = (self.regra_indice + 1) % len(self.REGRAS)
            self.botao_regra.set_text(self._texto_regra())
            self.atualizar_status(
                f"Regra selecionada: {self._texto_regra()}."
            )
            return True

        if self.botao_aplicar is not None and self.botao_aplicar.processar_evento(evento):
            self.aplicar_regra()
            return True

        if self.botao_dica is not None and self.botao_dica.processar_evento(evento):
            if self.ao_dica is not None:
                self.ao_dica()
            return True

        if self.botao_verificar is not None and self.botao_verificar.processar_evento(evento):
            self.tentar_resolver()
            return True

        if self.botao_anterior is not None and self.botao_anterior.processar_evento(evento):
            if self.pagina > 0:
                self.pagina -= 1
                self.atualizar_botoes()
            return True

        if self.botao_proxima is not None and self.botao_proxima.processar_evento(evento):
            if self.pagina + 1 < self._total_paginas():
                self.pagina += 1
                self.atualizar_botoes()
            return True

        return False

    def atualizar_hover(self, pos_mouse=None):
        for botao, _ in self.botoes:
            botao.atualizar(pos_mouse)
        for botao in (self.botao_regra, self.botao_aplicar, self.botao_dica,
                      self.botao_verificar, self.botao_anterior, self.botao_proxima):
            if botao is not None:
                botao.atualizar(pos_mouse)

    # ------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------

    def desenhar(self, superficie):
        estilo.desenhar_texto(
            superficie,
            "MESA DE DEDUÇÃO",
            estilo.fonte("titulo", 38, True),
            estilo.TEXTO,
            (640, 46),
            alinhamento="centro",
        )
        estilo.desenhar_texto(
            superficie,
            "Combine premissas para demonstrar as conclusões do caso.",
            estilo.fonte("ui", 13),
            estilo.TEXTO_SUAVE,
            (640, 92),
            alinhamento="centro",
        )

        self._desenhar_premissas(superficie)
        self._desenhar_regra(superficie)
        self._desenhar_status(superficie)

    def _desenhar_premissas(self, superficie):
        painel = self.PAINEL_ESQUERDO
        estilo.desenhar_painel(superficie, painel, cor=(17, 28, 38),
                               borda=estilo.BORDA, alpha=238)

        estilo.desenhar_texto_espacado(
            superficie,
            "Premissas disponíveis",
            estilo.fonte("ui", 10, True),
            estilo.TEXTO_FRACO,
            (painel.x + 20, painel.y + 16),
        )
        estilo.desenhar_texto(
            superficie,
            f"PÁGINA {self.pagina + 1} / {self._total_paginas()}",
            estilo.fonte("ui", 11, True),
            estilo.TEXTO_FRACO,
            (painel.right - 20, painel.y + 16),
            alinhamento="direita",
        )
        estilo.desenhar_divisoria(superficie, painel.x + 20, painel.right - 20,
                                 painel.y + 38, estilo.BORDA, 140)

        if not self.botoes:
            estilo.desenhar_paragrafo(
                superficie,
                "Nenhuma premissa disponível. Colete pistas e volte à mesa de dedução.",
                estilo.fonte("corpo", 17),
                estilo.TEXTO_SUAVE,
                (painel.x + 40, painel.y + 78, painel.w - 80, 100),
                espacamento=5,
            )
        else:
            for botao, _ in self.botoes:
                botao.desenhar(superficie)

        self.botao_anterior.desenhar(superficie)
        self.botao_proxima.desenhar(superficie)

        fonte_pagina = estilo.fonte("mono", 12, True)
        pagina = fonte_pagina.render(f"{self.pagina + 1} / {self._total_paginas()}",
                                     True, estilo.TEXTO_FRACO)
        superficie.blit(pagina, pagina.get_rect(
            center=(painel.centerx - 4, painel.bottom - 29)
        ))

    def _desenhar_regra(self, superficie):
        painel = self.PAINEL_DIREITO
        estilo.desenhar_painel(superficie, painel, cor=(17, 28, 38),
                               borda=estilo.BORDA, alpha=238)

        estilo.desenhar_texto_espacado(
            superficie,
            "Regra de inferência",
            estilo.fonte("ui", 10, True),
            estilo.TEXTO_FRACO,
            (painel.x + 24, painel.y + 18),
        )

        _chave, rotulo, descricao = self.REGRAS[self.regra_indice]
        estilo.desenhar_texto(
            superficie,
            rotulo,
            estilo.fonte("titulo", 24, True),
            estilo.DOURADO_CLARO,
            (painel.x + 24, painel.y + 42),
        )

        estilo.desenhar_paragrafo(
            superficie,
            descricao,
            estilo.fonte("corpo", 15),
            estilo.TEXTO_SUAVE,
            (painel.x + 24, painel.y + 82, painel.w - 48, 112),
            espacamento=4,
        )

        estilo.desenhar_divisoria(superficie, painel.x + 24, painel.right - 24,
                                 painel.y + 206, estilo.BORDA, 120)

        estilo.desenhar_texto(
            superficie,
            "TROCA A REGRA ATIVA",
            estilo.fonte("ui", 9, True),
            estilo.TEXTO_FRACO,
            (painel.x + 24, painel.y + 218),
        )

        self.botao_regra.desenhar(superficie)
        self.botao_aplicar.desenhar(superficie)
        if self.botao_dica is not None:
            self.botao_dica.desenhar(superficie)

    def _desenhar_status(self, superficie):
        barra = self.BARRA_STATUS
        estilo.desenhar_painel(superficie, barra, cor=(14, 24, 33),
                               borda=estilo.BORDA, alpha=236, sombra=False)

        estilo.desenhar_texto_espacado(
            superficie,
            "Retorno da dedução",
            estilo.fonte("ui", 9, True),
            estilo.TEXTO_FRACO,
            (barra.x + 20, barra.y + 12),
        )
        estilo.desenhar_paragrafo(
            superficie,
            self.status,
            estilo.fonte("logica", 15),
            estilo.TEXTO,
            (barra.x + 20, barra.y + 30, 870, 48),
            espacamento=3,
            limite_linhas=2,
        )

        self.botao_verificar.desenhar(superficie)
