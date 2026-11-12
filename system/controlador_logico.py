
class ControladorLogico:

    def __init__(self, motor_logico, diario):
        self.motor = motor_logico
        self.diario = diario

    def sincronizar_diario(self):
        """
        Transfere para o motor lógico as pistas descobertas.
        Não adiciona novamente premissas já registradas.
        """
        quantidade_adicionada = 0

        for pista in self.diario.listar_pistas():
            adicionada = self.motor.adicionar_premissa(
                pista,
                origem=f"Pista: {pista.id}"
            )

            if adicionada:
                quantidade_adicionada += 1

        return quantidade_adicionada

    def obter_premissas_disponiveis(self):
        self.sincronizar_diario()
        return self.motor.listar_premissas()

    def aplicar_regra(self, regra, premissa1, premissa2):
        self.sincronizar_diario()

        p1 = self.motor.converter_premissa(premissa1)
        p2 = self.motor.converter_premissa(premissa2)

        premissas_disponiveis = self.motor.listar_premissas()

        if p1 not in premissas_disponiveis:
            raise ValueError(
                "A primeira premissa não foi descoberta ou deduzida."
            )

        if p2 not in premissas_disponiveis:
            raise ValueError(
                "A segunda premissa não foi descoberta ou deduzida."
            )

        resultado = self.motor.aplicar_regra(
            regra,
            p1,
            p2
        )

        if resultado is None:
            return None

        self.motor.registrar_deducao(resultado)

        return resultado

    def verificar_conclusao(self, conclusao):
        self.sincronizar_diario()
        return self.motor.verificar_conclusao(conclusao)

    def verificar_caso(self, conclusoes):
        self.sincronizar_diario()

        resultados = {}

        for nome, dados in conclusoes.items():
            resultados[nome] = self.motor.verificar_conclusao(
                dados["expressao"]
            )

        return resultados

    def obter_historico(self):
        return self.motor.obter_historico()

    def formatar_expressao(self, expressao):
        return self.motor.formatar_expressao(expressao)
