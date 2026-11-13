
import pygame
import pygame_gui


class PainelDeducao:

    REGRAS = [
        ("modus_ponens", "MODUS PONENS"),
        ("silogismo_disjuntivo", "SILOGISMO DISJUNTIVO"),
        ("conjuncao", "CONJUNÇÃO")
    ]

    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.premissas = []
        self.selecionadas = []
        self.botoes = []

        self.pagina = 0
        self.itens_por_pagina = 8
        self.regra_indice = 0

        self.status = "Selecione duas premissas."
        self.texto_status = None

    def entrar(self):
        self.premissas = self.jogo.partida.obter_premissas()
        self.selecionadas.clear()
        self.pagina = 0

        self.botao_regra = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(300, 550, 250, 50),
            text=self.REGRAS[self.regra_indice][1],
            manager=self.manager
        )

        self.botao_aplicar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(570, 550, 220, 50),
            text="APLICAR REGRA",
            manager=self.manager
        )

        self.botao_resolver = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(810, 550, 250, 50),
            text="TENTAR RESOLVER",
            manager=self.manager
        )

        self.botao_anterior = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(300, 620, 110, 40),
            text="ANTERIOR",
            manager=self.manager
        )

        self.botao_proxima = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(430, 620, 110, 40),
            text="PRÓXIMA",
            manager=self.manager
        )

        self.texto_status = pygame_gui.elements.UITextBox(
            html_text=self.status,
            relative_rect=pygame.Rect(570, 610, 500, 55),
            manager=self.manager
        )

        self.atualizar_botoes()

    def sair(self):
        self.limpar_botoes()

        self.botao_regra.kill()
        self.botao_aplicar.kill()
        self.botao_resolver.kill()
        self.botao_anterior.kill()
        self.botao_proxima.kill()
        self.texto_status.kill()

    def limpar_botoes(self):
        for botao in self.botoes:
            botao.kill()

        self.botoes.clear()

    def atualizar_botoes(self):
        self.limpar_botoes()

        inicio = self.pagina * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina

        for indice, premissa in enumerate(self.premissas[inicio:fim]):
            indice_real = inicio + indice
            coluna = indice % 2
            linha = indice // 2

            texto = str(premissa)

            if indice_real in self.selecionadas:
                texto = "[SELECIONADA] " + texto

            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    100 + coluna * 550,
                    170 + linha * 85,
                    500,
                    65
                ),
                text=texto,
                manager=self.manager
            )

            self.botoes.append((botao, indice_real))

    def atualizar_premissas(self):
        self.premissas = self.jogo.partida.obter_premissas()
        self.selecionadas.clear()

        total_paginas = max(
            1,
            (len(self.premissas) + self.itens_por_pagina - 1)
            // self.itens_por_pagina
        )

        self.pagina = min(self.pagina, total_paginas - 1)
        self.atualizar_botoes()

    def atualizar_status(self, mensagem):
        self.status = mensagem
        self.texto_status.kill()

        self.texto_status = pygame_gui.elements.UITextBox(
            html_text=mensagem,
            relative_rect=pygame.Rect(570, 610, 500, 55),
            manager=self.manager
        )

    def aplicar_regra(self):
        if len(self.selecionadas) != 2:
            self.atualizar_status(
                "Selecione exatamente duas premissas."
            )
            return

        premissa1 = self.premissas[self.selecionadas[0]]
        premissa2 = self.premissas[self.selecionadas[1]]
        regra = self.REGRAS[self.regra_indice][0]

        try:
            resultado = self.jogo.partida.aplicar_regra(
                regra,
                premissa1,
                premissa2
            )

            if resultado is None:
                self.atualizar_status(
                    "Não foi possível aplicar essa regra."
                )
                return

            self.atualizar_status(f"Dedução: {resultado}")
            self.atualizar_premissas()

        except (ValueError, TypeError) as erro:
            self.atualizar_status(str(erro))

    def tentar_resolver(self):
        try:
            resultado = self.jogo.partida.tentar_resolver()

            if resultado["resolvido"]:
                mensagem = resultado["mensagem"]
            else:
                mensagem = (
                        resultado["mensagem"]
                        + "\nPendências: "
                        + ", ".join(resultado["pendencias"])
                )

        except (ValueError, TypeError) as erro:
            self.atualizar_status(str(erro))

    def processar_evento(self, evento):
        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        for botao, indice in self.botoes:
            if evento.ui_element == botao:

                if indice in self.selecionadas:
                    self.selecionadas.remove(indice)

                elif len(self.selecionadas) < 2:
                    self.selecionadas.append(indice)

                self.atualizar_botoes()
                return

        if evento.ui_element == self.botao_regra:
            self.regra_indice = (
                self.regra_indice + 1
            ) % len(self.REGRAS)

            self.botao_regra.set_text(
                self.REGRAS[self.regra_indice][1]
            )

        elif evento.ui_element == self.botao_aplicar:
            self.aplicar_regra()

        elif evento.ui_element == self.botao_resolver:
            self.tentar_resolver()

        elif evento.ui_element == self.botao_anterior:
            if self.pagina > 0:
                self.pagina -= 1
                self.atualizar_botoes()

        elif evento.ui_element == self.botao_proxima:
            total = (
                len(self.premissas) + self.itens_por_pagina - 1
            ) // self.itens_por_pagina

            if self.pagina + 1 < total:
                self.pagina += 1
                self.atualizar_botoes()

    def desenhar(self, superficie):
        fonte = pygame.font.Font(None, 60)

        titulo = fonte.render(
            "MESA DE DEDUÇÃO",
            True,
            (230, 230, 230)
        )

        superficie.blit(
            titulo,
            titulo.get_rect(center=(640, 75))
        )

        fonte_instrucao = pygame.font.Font(None, 28)

        instrucao = fonte_instrucao.render(
            "Selecione duas premissas e escolha uma regra lógica.",
            True,
            (190, 200, 210)
        )

        superficie.blit(instrucao, (250, 120))
