
from data.carregador import carregar_personagens
from data.locais import carregar_locais

from scenes.mapa import Mapa

from system.gerador_caso import GeradorCaso
from system.gerador_pistas import GeradorPistas
from system.distribuidor_pistas import DistribuidorPistas
from system.gerador_dialogos import GeradorDialogos

from system.diario import DiarioDeBordo
from system.sistema_dialogo import SistemaDialogo
from system.sistema_investigacao import SistemaInvestigacao
from system.controlador_investigacao import ControladorInvestigacao

from system.motor_logico import MotorLogico
from system.controlador_logico import ControladorLogico
from system.sistema_resolucao import SistemaResolucao


class ControladorPartida:

    def __init__(self):
        self.iniciar_nova_partida()

    def iniciar_nova_partida(self):
        # Dados novos para evitar reaproveitar estados anteriores.
        self.personagens = carregar_personagens()
        self.locais = carregar_locais()

        # Geração do caso.
        gerador_caso = GeradorCaso()
        self.caso = gerador_caso.gerar(self.personagens)

        # Geração das pistas e das conclusões esperadas.
        gerador_pistas = GeradorPistas()

        pistas_lista = gerador_pistas.gerar(
            self.caso,
            self.personagens
        )

        self.pistas = {
            pista.id: pista
            for pista in pistas_lista
        }

        self.conclusoes = gerador_pistas.obter_conclusoes(
            self.caso,
            self.personagens
        )

        # Distribuição das pistas.
        DistribuidorPistas().distribuir(
            pistas_lista,
            self.caso,
            self.locais
        )

        # Geração dos diálogos.
        self.dialogos = GeradorDialogos().gerar(
            self.caso,
            self.personagens,
            self.pistas
        )

        # Mapa e diário.
        self.mapa = Mapa(self.locais)
        self.diario = DiarioDeBordo()

        # Sistema de diálogos.
        self.sistema_dialogo = SistemaDialogo(self.dialogos)

        self.controlador_investigacao = ControladorInvestigacao(
            self.sistema_dialogo,
            self.diario,
            self.pistas
        )

        # Sistema de investigação dos locais.
        self.sistema_investigacao = SistemaInvestigacao(
            self.mapa,
            self.diario,
            self.pistas
        )

        # Motor lógico.
        self.motor_logico = MotorLogico()

        self.controlador_logico = ControladorLogico(
            self.motor_logico,
            self.diario
        )

        # Resolução do caso.
        self.sistema_resolucao = SistemaResolucao(
            self.controlador_logico,
            self.conclusoes
        )

        return self

    def acessar_local(self, local_id):
        self._verificar_partida_ativa()
        return self.mapa.acessar_local(local_id)

    def voltar_ao_mapa(self):
        self._verificar_partida_ativa()
        self.mapa.voltar_ao_mapa()

    def investigar_local(self):
        self._verificar_partida_ativa()
        return self.sistema_investigacao.investigar_local()

    def iniciar_conversa(self, personagem_id):
        self._verificar_partida_ativa()

        if personagem_id not in self.personagens:
            raise ValueError("Personagem não encontrado.")

        if personagem_id in self.caso.vitimas_ids:
            raise ValueError("Não é possível conversar com uma vítima.")

        local_atual = self.mapa.obter_local_atual()

        if local_atual is None:
            raise RuntimeError(
                "É necessário acessar um local antes de conversar."
            )

        if personagem_id not in local_atual.personagens:
            raise ValueError(
                "Este personagem não está no local atual."
            )

        dialogo_id = f"{personagem_id}_inicio"

        if dialogo_id not in self.dialogos:
            raise ValueError(
                "Não existe diálogo disponível para este personagem."
            )

        self.controlador_investigacao.iniciar_conversa(dialogo_id)

    def selecionar_escolha(self, indice):
        self._verificar_partida_ativa()

        return self.controlador_investigacao.selecionar_escolha(
            indice
        )

    def aplicar_regra(self, regra, premissa1, premissa2):
        self._verificar_partida_ativa()

        return self.controlador_logico.aplicar_regra(
            regra,
            premissa1,
            premissa2
        )

    def tentar_resolver(self):
        return self.sistema_resolucao.verificar_solucao()

    def obter_pistas_diario(self):
        return self.diario.listar_pistas()

    def obter_dialogo_atual(self):
        return self.controlador_investigacao.obter_dialogo_atual()

    def obter_escolhas_dialogo(self):
        return self.controlador_investigacao.obter_escolhas()

    def obter_premissas(self):
        return self.controlador_logico.obter_premissas_disponiveis()

    def obter_historico_deducoes(self):
        return self.controlador_logico.obter_historico()

    def _verificar_partida_ativa(self):
        if self.sistema_resolucao.esta_resolvido():
            raise RuntimeError(
                "Esta partida já foi resolvida. Inicie uma nova partida."
            )
