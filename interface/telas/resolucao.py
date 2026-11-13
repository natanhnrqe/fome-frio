
import pygame
import pygame_gui


class TelaResolucao:
    def __init__(self, jogo):
        self.jogo = jogo
        self.manager = jogo.interface

        self.botoes_personagens = []
        self.suspeito_selecionado = None
        self.resultado = None

        self.elementos = []

    def entrar(self):
        self.suspeito_selecionado = None
        self.resultado = None
        self.botoes_personagens = []
        self.elementos = []

        self.criar_interface()

    def criar_elemento(self, classe, **kwargs):
        elemento = classe(manager=self.manager, **kwargs)
        self.elementos.append(elemento)
        return elemento

    def criar_interface(self):
        self.criar_elemento(
            pygame_gui.elements.UILabel,
            relative_rect=pygame.Rect(300, 45, 680, 60),
            text="ACUSAÇÃO FINAL"
        )

        self.criar_elemento(
            pygame_gui.elements.UILabel,
            relative_rect=pygame.Rect(250, 110, 780, 45),
            text="Quem você acredita ser o assassino?"
        )

        for indice, (personagem_id, personagem) in enumerate(
            self.jogo.partida.personagens.items()
        ):
            coluna = indice % 4
            linha = indice // 4

            botao = self.criar_elemento(
                pygame_gui.elements.UIButton,
                relative_rect=pygame.Rect(
                    65 + coluna * 300,
                    210 + linha * 115,
                    260,
                    75
                ),
                text=personagem.nome
            )

            self.botoes_personagens.append(
                (botao, personagem_id)
            )

        self.status = self.criar_elemento(
            pygame_gui.elements.UILabel,
            relative_rect=pygame.Rect(200, 455, 880, 45),
            text="Selecione um suspeito."
        )

        self.botao_confirmar = self.criar_elemento(
            pygame_gui.elements.UIButton,
            relative_rect=pygame.Rect(440, 520, 400, 55),
            text="CONFIRMAR ACUSAÇÃO"
        )

        self.botao_voltar = self.criar_elemento(
            pygame_gui.elements.UIButton,
            relative_rect=pygame.Rect(20, 20, 190, 45),
            text="VOLTAR"
        )

        self.botao_nova = None
        self.botao_menu = None
        self.texto_revelacao = None

    def processar_evento(self, evento):
        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        if self.resultado is not None:
            if evento.ui_element == self.botao_nova:
                self.jogo.iniciar_partida()
                return

            if evento.ui_element == self.botao_menu:
                self.jogo.voltar_menu()
                return

        for botao, personagem_id in self.botoes_personagens:
            if evento.ui_element == botao:
                self.suspeito_selecionado = personagem_id

                nome = self.jogo.partida.personagens[
                    personagem_id
                ].nome

                self.status.set_text(
                    f"Suspeito selecionado: {nome}"
                )
                return

        if evento.ui_element == self.botao_voltar:
            self.jogo.gerenciador_telas.mudar_tela(
                "investigacao"
            )
            return

        if evento.ui_element == self.botao_confirmar:
            self.confirmar_acusacao()

    def confirmar_acusacao(self):
        if self.suspeito_selecionado is None:
            self.status.set_text("Selecione um suspeito primeiro.")
            return

        validacao = self.jogo.partida.tentar_resolver()

        if not validacao["resolvido"]:
            self.status.set_text(
                "Ainda existem conclusões pendentes."
            )
            self.jogo.gerenciador_telas.mudar_tela("investigacao")
            return

        caso = self.jogo.partida.caso
        personagens = self.jogo.partida.personagens

        def obter_nome(personagem_id):
            personagem = personagens.get(personagem_id)

            if personagem is None:
                return personagem_id

            return personagem.nome

        assassino = obter_nome(caso.assassino_id)

        vitima_assassinato = obter_nome(
            caso.vitima_assassinato_id
        )

        vitima_secundaria = obter_nome(
            caso.vitima_secundaria_id
        )

        self.resultado = (
                self.suspeito_selecionado == caso.assassino_id
        )

        if self.resultado:
            mensagem = "VOCÊ RESOLVEU O CASO!"
        else:
            mensagem = "SUA ACUSAÇÃO ESTAVA INCORRETA."

        self.status.set_text(mensagem)

        texto_revelacao = (
            f"<b>O VERDADEIRO ASSASSINO:</b><br>"
            f"{assassino}<br><br>"
            f"<b>VÍTIMA DO ASSASSINATO:</b><br>"
            f"{vitima_assassinato}<br><br>"
            f"<b>SEGUNDA VÍTIMA:</b><br>"
            f"{vitima_secundaria}<br><br>"
            f"<b>CAUSA DA SEGUNDA MORTE:</b><br>"
            f"{caso.causa_morte_secundaria}"
        )

        self.texto_revelacao = self.criar_elemento(
            pygame_gui.elements.UITextBox,
            relative_rect=pygame.Rect(250, 495, 780, 125),
            html_text=texto_revelacao
        )

        self.botao_confirmar.disable()
        self.botao_voltar.disable()

        for botao, _ in self.botoes_personagens:
            botao.disable()

        self.botao_nova = self.criar_elemento(
            pygame_gui.elements.UIButton,
            relative_rect=pygame.Rect(440, 640, 190, 45),
            text="NOVA PARTIDA"
        )

        self.botao_menu = self.criar_elemento(
            pygame_gui.elements.UIButton,
            relative_rect=pygame.Rect(650, 640, 190, 45),
            text="MENU"
        )

    def sair(self):
        for elemento in self.elementos:
            elemento.kill()

        self.elementos.clear()
        self.botoes_personagens.clear()

        self.suspeito_selecionado = None
        self.resultado = None

    def atualizar(self, delta):
        pass

    def desenhar(self, superficie):
        superficie.fill((24, 29, 36))

        if self.resultado is True:
            texto = "INVESTIGAÇÃO CONCLUÍDA"
        elif self.resultado is False:
            texto = "INVESTIGAÇÃO FALHOU"
        else:
            texto = "A VERDADE ESTÁ ENTRE OS SUSPEITOS"

        fonte = pygame.font.SysFont(
            "arial", 28, bold=True
        )

        imagem = fonte.render(
            texto,
            True,
            (230, 230, 230)
        )

        superficie.blit(
            imagem,
            imagem.get_rect(center=(640, 160))
        )
