
from system.controlador_partida import ControladorPartida


partida = ControladorPartida()

print("\n=== CASO GERADO ===")

print(
    "Assassino real:",
    partida.personagens[partida.caso.assassino_id].nome
)

print(
    "Vítimas:",
    [
        partida.personagens[id].nome
        for id in partida.caso.vitimas_ids
    ]
)

# Exploração de todos os locais e conversas.
print("\n=== INVESTIGAÇÃO ===")

for local in partida.locais:

    partida.acessar_local(local.id)

    resultado = partida.investigar_local()

    print(
        f"\n{local.nome}: "
        f"{len(resultado['pistas_novas'])} pista(s) encontrada(s)"
    )

    for personagem_id in local.personagens:

        if personagem_id in partida.caso.vitimas_ids:
            continue

        partida.iniciar_conversa(personagem_id)

        partida.selecionar_escolha(0)

        resposta = partida.selecionar_escolha(0)

        if resposta["pista_nova"]:
            print(
                partida.personagens[personagem_id].nome,
                "revelou:",
                resposta["pista"].simbolo
            )

# Todas as pistas devem ter sido descobertas.
assert len(partida.obter_pistas_diario()) == len(partida.pistas)

print("\nTotal de pistas:", len(partida.obter_pistas_diario()))

# Inicia com a hipótese de que um dos seis sobreviventes é culpado.
hipotese = partida.pistas["hipoteses_assassino"].expressao

print("\n=== ELIMINAÇÃO DE SUSPEITOS ===")
print("Hipótese inicial:", hipotese)

# Aplica o silogismo disjuntivo com os cinco álibis.
for pista in partida.pistas.values():

    if not pista.id.startswith("alibi_"):
        continue

    hipotese = partida.aplicar_regra(
        "silogismo_disjuntivo",
        hipotese,
        pista.expressao
    )

    assert hipotese is not None

    print(
        "Evidência:",
        pista.simbolo,
        "| Possibilidades restantes:",
        hipotese
    )

# Confere se restou exatamente o assassino.
conclusao_assassinato = partida.conclusoes[
    "assassinato"
]["expressao"]

assert hipotese == partida.motor_logico.interpretar(
    conclusao_assassinato
)

print("\nAssassino identificado:", hipotese)

# Resolve a segunda morte.
print("\n=== SEGUNDA MORTE ===")

resultado_secundario = partida.aplicar_regra(
    "modus_ponens",
    "T >> U",
    "T"
)

assert resultado_secundario is not None

# Verifica as duas conclusões.
resultado = partida.tentar_resolver()

assert resultado["resolvido"] is True

print("\n=== CASO RESOLVIDO ===")
print(resultado["mensagem"])

for conclusao in partida.conclusoes.values():
    print(conclusao["texto"])

# Testa o reinício.
print("\n=== REINICIANDO PARTIDA ===")

mapa_antigo = partida.mapa
diario_antigo = partida.diario
motor_antigo = partida.motor_logico

partida.iniciar_nova_partida()

assert partida.mapa is not mapa_antigo
assert partida.diario is not diario_antigo
assert partida.motor_logico is not motor_antigo

assert partida.diario.quantidade_pistas() == 0
assert partida.motor_logico.listar_premissas() == []
assert len(partida.mapa.listar_locais_visitados()) == 0
assert not partida.sistema_resolucao.esta_resolvido()

print("Nova partida criada sem carregar o estado anterior.")

print("\nTESTE COMPLETO APROVADO!")
