
import ast

from sympy import Symbol
from sympy.logic.boolalg import And, Or, Not, Implies


class MotorLogico:
    def __init__(self):
        self.variaveis = {}
        self.premissas = []
        self.historico = []

    # --------------------------------------------------
    # INTERPRETAÇÃO DAS EXPRESSÕES
    # --------------------------------------------------

    def obter_variavel(self, nome: str):
        if nome not in self.variaveis:
            self.variaveis[nome] = Symbol(nome)

        return self.variaveis[nome]

    def interpretar(self, expressao: str):
        if not isinstance(expressao, str):
            raise TypeError("A expressão deve ser uma string.")

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

    # --------------------------------------------------
    # CONVERSÃO E CADASTRO DE PREMISSAS
    # --------------------------------------------------

    def converter_premissa(self, premissa):
        # Já é uma expressão lógica do SymPy.
        if isinstance(premissa, (Symbol, And, Or, Not, Implies)):
            return premissa

        # É um objeto Pista.
        if hasattr(premissa, "expressao"):
            premissa = premissa.expressao

        if not isinstance(premissa, str):
            raise TypeError(
                "A premissa deve ser uma string, "
                "uma Pista ou uma expressão lógica do SymPy."
            )

        return self.interpretar(premissa)

    def adicionar_premissa(self, premissa, origem="Premissa"):
        expressao = self.converter_premissa(premissa)

        if expressao not in self.premissas:
            self.premissas.append(expressao)

            self.historico.append({
                "tipo": "premissa",
                "origem": origem,
                "expressao": expressao
            })

            return True

        return False

    # --------------------------------------------------
    # REGRAS DE INFERÊNCIA
    # --------------------------------------------------

    def modus_ponens(self, premissa1, premissa2):
        p1 = self.converter_premissa(premissa1)
        p2 = self.converter_premissa(premissa2)

        if isinstance(p1, Implies) and p1.args[0] == p2:
            return p1.args[1]

        if isinstance(p2, Implies) and p2.args[0] == p1:
            return p2.args[1]

        return None


    def silogismo_disjuntivo(self, premissa1, premissa2):
        p1 = self.converter_premissa(premissa1)
        p2 = self.converter_premissa(premissa2)

        if isinstance(p1, Or) and isinstance(p2, Not):
            disjuncao = p1
            negacao = p2

        elif isinstance(p2, Or) and isinstance(p1, Not):
            disjuncao = p2
            negacao = p1

        else:
            return None

        alternativas = list(disjuncao.args)
        alternativa_negada = negacao.args[0]

        if alternativa_negada not in alternativas:
            return None

        restantes = [
            alternativa
            for alternativa in alternativas
            if alternativa != alternativa_negada
        ]

        if len(restantes) == 0:
            return None

        if len(restantes) == 1:
            return restantes[0]

        return Or(*restantes)


    def conjuncao(self, premissa1, premissa2):
        p1 = self.converter_premissa(premissa1)
        p2 = self.converter_premissa(premissa2)

        return And(p1, p2)

    # --------------------------------------------------
    # APLICAÇÃO E REGISTRO DAS REGRAS
    # --------------------------------------------------

    def aplicar_regra(
        self,
        regra: str,
        premissa1,
        premissa2
    ):
        regras = {
            "modus_ponens": self.modus_ponens,
            "silogismo_disjuntivo": self.silogismo_disjuntivo,
            "conjuncao": self.conjuncao
        }

        if regra not in regras:
            raise ValueError(f"Regra desconhecida: {regra}")

        resultado = regras[regra](premissa1, premissa2)

        if resultado is None:
            return None

        self.historico.append({
            "tipo": "deducao",
            "regra": regra,
            "premissas": [
                self.converter_premissa(premissa1),
                self.converter_premissa(premissa2)
            ],
            "resultado": resultado
        })

        return resultado

    def registrar_deducao(self, expressao):
        resultado = self.converter_premissa(expressao)

        if resultado in self.premissas:
            return False

        self.premissas.append(resultado)

        self.historico.append({
            "tipo": "deducao_registrada",
            "resultado": resultado
        })

        return True

    # --------------------------------------------------
    # CONSULTAS
    # --------------------------------------------------

    def verificar_conclusao(self, conclusao) -> bool:
        expressao = self.converter_premissa(conclusao)
        return expressao in self.premissas

    def listar_premissas(self):
        return list(self.premissas)

    def obter_historico(self):
        return list(self.historico)

    def limpar(self):
        self.premissas.clear()
        self.historico.clear()
        self.variaveis.clear()

    def formatar_expressao(self, expressao):
        return str(expressao)
