
from system.motor_logico import MotorLogico


motor = MotorLogico()

# Premissa inicial: uma das quatro possibilidades é verdadeira.
motor.adicionar_premissa("A | B | C | D")

# Eliminamos A.
resultado = motor.aplicar_regra(
    "silogismo_disjuntivo",
    "A | B | C | D",
    "~A"
)

assert resultado == motor.interpretar("B | C | D")
print("Após eliminar A:", resultado)

# Eliminamos B.
resultado = motor.aplicar_regra(
    "silogismo_disjuntivo",
    resultado,
    "~B"
)

assert resultado == motor.interpretar("C | D")
print("Após eliminar B:", resultado)

# Eliminamos C.
resultado = motor.aplicar_regra(
    "silogismo_disjuntivo",
    resultado,
    "~C"
)

assert resultado == motor.interpretar("D")
print("Após eliminar C:", resultado)

print("\nSILOGISMO DISJUNTIVO APROVADO!")
