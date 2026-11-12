
from data.carregador import carregar_personagens

from system.gerador_caso import GeradorCaso
from system.gerador_pistas import GeradorPistas
from system.diario import DiarioDeBordo
from system.motor_logico import MotorLogico
from system.controlador_logico import ControladorLogico
from system.sistema_resolucao import SistemaResolucao


personagens = carregar_personagens()

caso = GeradorCaso().gerar(personagens)

gerador = GeradorPistas()

pistas = gerador.gerar(caso, personagens)
conclusoes = gerador.obter_conclusoes(caso, personagens)

diario = DiarioDeBordo()

for pista in pistas:
    diario.registrar_pista(pista)

motor = MotorLogico()

controlador = ControladorLogico(
    motor_logico=motor,
    diario=diario
)

sistema = SistemaResolucao(
    controlador_logico=controlador,
    conclusoes=conclusoes
)

# SITUAÇÃO 1: nenhuma conclusão demonstrada.
resultado = sistema.verificar_solucao()

assert resultado["resolvido"] is False
assert len(resultado["pendencias"]) == 2

print("Teste 1:", resultado["mensagem"])

# SITUAÇÃO 2: somente o assassinato demonstrado.
etapas_assassinato = [
    ("P >> Q", "P"),
    ("Q >> R", "Q"),
    ("R >> S", "R")
]

for implicacao, fato in etapas_assassinato:
    resultado_deducao = controlador.aplicar_regra(
        "modus_ponens",
        implicacao,
        fato
    )
    assert resultado_deducao is not None

resultado = sistema.verificar_solucao()

assert resultado["resolvido"] is False
assert resultado["pendencias"] == ["morte_secundaria"]

print("Teste 2:", resultado["mensagem"])
print("Pendência:", resultado["pendencias"])

# SITUAÇÃO 3: segunda morte também demonstrada.
resultado_deducao = controlador.aplicar_regra(
    "modus_ponens",
    "T >> U",
    "T"
)

assert resultado_deducao is not None

resultado = sistema.verificar_solucao()

assert resultado["resolvido"] is True
assert sistema.esta_resolvido() is True

print("Teste 3:", resultado["mensagem"])

# Não deve perder o estado de resolução.
resultado_repetido = sistema.verificar_solucao()

assert resultado_repetido["resolvido"] is True

print("\nTodos os testes passaram!")
