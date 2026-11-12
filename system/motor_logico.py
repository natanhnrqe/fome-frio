
import ast

from sympy import Symbol
from sympy.logic.boolalg import And, Or, Not, Implies


class MotorLogico:

    def __init__(self):
        self.variaveis = {}

    def obter_variavel(self, nome: str):
        if nome not in self.variaveis:
            self.variaveis[nome] = Symbol(nome)

        return self.variaveis[nome]

    def interpretar(self, expressao: str):
        """
        Converte uma expressão textual em uma expressão lógica SymPy.
        """

        try:
            arvore = ast.parse(expressao, mode="eval")
            return self._interpretar_no(arvore.body)

        except (SyntaxError, TypeError) as erro:
            raise ValueError(
                f"Expressão lógica inválida: {expressao}"
            ) from erro

    def _interpretar_no(self, no):

        if isinstance(no, ast.Name):
            return self.obter_variavel(no.id)

        if isinstance(no, ast.UnaryOp) and isinstance(no.op, ast.Invert):
            return Not(self._interpretar_no(no.operand))

        if isinstance(no, ast.BinOp):

            esquerda = self._interpretar_no(no.left)
            direita = self._interpretar_no(no.right)

            if isinstance(no.op, ast.BitAnd):
                return And(esquerda, direita)

            if isinstance(no.op, ast.BitOr):
                return Or(esquerda, direita)

            if isinstance(no.op, ast.RShift):
                return Implies(esquerda, direita)

        raise ValueError("Operação lógica não permitida.")

    def converter_premissa(self, premissa):
        """
        Aceita tanto uma expressão textual quanto um objeto Pista.
        """

        if hasattr(premissa, "expressao"):
            premissa = premissa.expressao

        if not isinstance(premissa, str):
            raise TypeError("A premissa deve ser uma string ou uma Pista.")

        return self.interpretar(premissa)

    def modus_ponens(self, premissa1, premissa2):
        """
        P, P -> Q  =>  Q
        """

        p1 = self.converter_premissa(premissa1)
        p2 = self.converter_premissa(premissa2)

        if p1.func == Implies and p1.args[0] == p2:
            return p1.args[1]

        if p2.func == Implies and p2.args[0] == p1:
            return p2.args[1]

        return None

    def silogismo_disjuntivo(self, premissa1, premissa2):
        """
        P v Q, ~P  =>  Q
        """

        p1 = self.converter_premissa(premissa1)
        p2 = self.converter_premissa(premissa2)

        if p1.func == Or and p2.func == Not:
            if p2.args[0] in p1.args:
                return next(
                    item for item in p1.args
                    if item != p2.args[0]
                )

        if p2.func == Or and p1.func == Not:
            if p1.args[0] in p2.args:
                return next(
                    item for item in p2.args
                    if item != p1.args[0]
                )

        return None

    def conjuncao(self, premissa1, premissa2):
        """
        P, Q  =>  P & Q
        """

        p1 = self.converter_premissa(premissa1)
        p2 = self.converter_premissa(premissa2)

        return And(p1, p2)

    def aplicar_regra(self, regra: str, premissa1, premissa2):
        """
        Executa a regra de inferência solicitada.
        """

        regras = {
            "modus_ponens": self.modus_ponens,
            "silogismo_disjuntivo": self.silogismo_disjuntivo,
            "conjuncao": self.conjuncao
        }

        if regra not in regras:
            raise ValueError(f"Regra desconhecida: {regra}")

        return regras[regra](premissa1, premissa2)

    def formatar_expressao(self, expressao):
        return str(expressao)
