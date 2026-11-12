
from system.motor_logico import MotorLogico


motor = MotorLogico()

# Premissas iniciais
motor.adicionar_premissa("P", origem="Premissa 1")
motor.adicionar_premissa("P >> Q", origem="Premissa 2")

# Modus Ponens:
# P
# P -> Q
# Portanto, Q

resultado = motor.aplicar_regra(
    "modus_ponens",
    "P",
    "P >> Q"
)

assert resultado == motor.interpretar("Q")
print("Modus Ponens:", motor.formatar_expressao(resultado))

motor.registrar_deducao(resultado)

assert motor.verificar_conclusao("Q")


# Silogismo Disjuntivo:
# R ou S
# Não R
# Portanto, S

resultado = motor.aplicar_regra(
    "silogismo_disjuntivo",
    "R | S",
    "~R"
)

assert resultado == motor.interpretar("S")
print("Silogismo Disjuntivo:", motor.formatar_expressao(resultado))

motor.registrar_deducao(resultado)


# Conjunção:
# A
# B
# Portanto, A e B

resultado = motor.aplicar_regra(
    "conjuncao",
    "A",
    "B"
)

assert resultado == motor.interpretar("A & B")
print("Conjunção:", motor.formatar_expressao(resultado))


# Histórico
print("\n===== HISTÓRICO =====")

for etapa in motor.obter_historico():
    print(etapa)

print("\nTodos os testes passaram!")
