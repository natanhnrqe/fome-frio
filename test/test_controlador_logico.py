
from data.carregador import carregar_personagens

from system.gerador_caso import GeradorCaso
from system.gerador_pistas import GeradorPistas
from system.diario import DiarioDeBordo
from system.motor_logico import MotorLogico
from system.controlador_logico import ControladorLogico


personagens = carregar_personagens()

# Gera um caso aleatório.
caso = GeradorCaso().gerar(personagens)

gerador = GeradorPistas()

pistas = gerador.gerar(caso, personagens)
conclusoes = gerador.obter_conclusoes(caso, personagens)

# Simula a descoberta de todas as pistas.
diario = DiarioDeBordo()

for pista in pistas:
    diario.registrar_pista(pista)

# Inicializa os sistemas.
motor = MotorLogico()

controlador = ControladorLogico(
    motor_logico=motor,
    diario=diario
)

# Confirma que todas as pistas chegaram ao motor.
premissas = controlador.obter_premissas_disponiveis()

assert len(premissas) == len(pistas)

# Cadeia lógica do assassinato.
etapas = [
    ("P >> Q", "P"),
    ("Q >> R", "Q"),
    ("R >> S", "R")
]

for implicacao, fato in etapas:
    resultado = controlador.aplicar_regra(
        "modus_ponens",
        implicacao,
        fato
    )

    assert resultado is not None
    print("Dedução:", controlador.formatar_expressao(resultado))

# Cadeia lógica da morte secundária.
resultado = controlador.aplicar_regra(
    "modus_ponens",
    "T >> U",
    "T"
)

assert resultado is not None
print("Dedução:", controlador.formatar_expressao(resultado))

# Verifica as duas conclusões.
resultado_caso = controlador.verificar_caso(conclusoes)

assert resultado_caso["assassinato"] is True
assert resultado_caso["morte_secundaria"] is True

# Verifica se o jogador não consegue usar uma premissa desconhecida.
try:
    controlador.aplicar_regra(
        "modus_ponens",
        "X >> Y",
        "X"
    )
    raise AssertionError("O sistema aceitou premissas desconhecidas.")

except ValueError:
    print("Premissas desconhecidas foram bloqueadas.")

print("\nRESULTADO FINAL")
print("Assassino:", personagens[caso.assassino_id].nome)

for nome, dados in conclusoes.items():
    print(f"{nome}: {dados['texto']}")

print("\nTodas as validações passaram!")
