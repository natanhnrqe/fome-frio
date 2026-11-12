
from data.carregador import carregar_pistas
from system.motor_logico import MotorLogico


pistas = carregar_pistas()
motor = MotorLogico()

print("Total de pistas:", len(pistas))
print("-" * 40)

for pista in pistas.values():
    expressao = motor.converter_premissa(pista)

    print(f"ID: {pista.id}")
    print(f"Símbolo: {pista.simbolo}")
    print(f"Descrição: {pista.descricao}")
    print(f"Expressão interpretada: {expressao}")
    print("-" * 40)
