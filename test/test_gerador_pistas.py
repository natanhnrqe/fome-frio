
from data.carregador import carregar_personagens
from system.gerador_caso import GeradorCaso
from system.gerador_pistas import GeradorPistas
from system.motor_logico import MotorLogico


personagens = carregar_personagens()

gerador_caso = GeradorCaso()
gerador_pistas = GeradorPistas()

caso = gerador_caso.gerar(personagens)
pistas = gerador_pistas.gerar(caso, personagens)
conclusoes = gerador_pistas.obter_conclusoes(caso, personagens)

motor = MotorLogico()

# Adiciona todas as pistas como premissas.
for pista in pistas:
    motor.adicionar_premissa(pista)

# Cadeia do assassinato: P -> Q -> R -> S
etapas_assassinato = [
    ("P >> Q", "P"),
    ("Q >> R", "Q"),
    ("R >> S", "R")
]

for implicacao, fato in etapas_assassinato:
    resultado = motor.aplicar_regra(
        "modus_ponens",
        implicacao,
        fato
    )

    assert resultado is not None

    motor.registrar_deducao(resultado)

# Cadeia da morte secundária: T -> U
resultado = motor.aplicar_regra(
    "modus_ponens",
    "T >> U",
    "T"
)

assert resultado is not None
motor.registrar_deducao(resultado)

# Verifica as conclusões.
assert motor.verificar_conclusao(
    conclusoes["assassinato"]["expressao"]
)

assert motor.verificar_conclusao(
    conclusoes["morte_secundaria"]["expressao"]
)

print("\nCASO GERADO")
print("Assassino:", personagens[caso.assassino_id].nome)
print("Vítimas:", [
    personagens[id].nome for id in caso.vitimas_ids
])

print("\nCONCLUSÕES DEDUZIDAS")
print(conclusoes["assassinato"]["texto"])
print(conclusoes["morte_secundaria"]["texto"])

print("\nTodas as deduções foram validadas!")
