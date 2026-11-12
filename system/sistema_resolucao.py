
class SistemaResolucao:

    def __init__(self, controlador_logico, conclusoes):
        self.controlador_logico = controlador_logico
        self.conclusoes = conclusoes
        self.resolvido = False

    def verificar_solucao(self):
        if self.resolvido:
            return {
                "resolvido": True,
                "pendencias": [],
                "mensagem": "Este caso já foi resolvido."
            }

        resultados = self.controlador_logico.verificar_caso(
            self.conclusoes
        )

        pendencias = [
            nome
            for nome, confirmado in resultados.items()
            if not confirmado
        ]

        if pendencias:
            return {
                "resolvido": False,
                "pendencias": pendencias,
                "mensagem": (
                    "Ainda existem conclusões que precisam "
                    "ser demonstradas."
                )
            }

        self.resolvido = True

        return {
            "resolvido": True,
            "pendencias": [],
            "mensagem": "Investigação concluída! Caso resolvido."
        }

    def esta_resolvido(self):
        return self.resolvido

    def obter_conclusoes(self):
        return self.conclusoes
