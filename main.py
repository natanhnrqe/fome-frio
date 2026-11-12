
from system.motor_logico import MotorLogico

motor = MotorLogico()

# MODUS PONENS
resultado = motor.modus_ponens("P", "P >> Q")

print("Modus Ponens:", resultado)
# Q


# SILOGISMO DISJUNTIVO
resultado = motor.silogismo_disjuntivo("T | S", "~T")

print("Silogismo Disjuntivo:", resultado)
# S


# CONJUNÇÃO
resultado = motor.conjuncao("R", "Q")

print("Conjunção:", resultado)
# Q & R


# TESTE DE INFERÊNCIA INVÁLIDA
resultado = motor.modus_ponens("P", "Q >> R")

print("Inferência inválida:", resultado)
# None


# CONCLUSÃO FINAL
resultado = motor.conjuncao("S", "I")

print("Conclusão:", resultado)
# I & S
