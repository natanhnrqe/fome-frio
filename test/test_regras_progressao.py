
from system.controlador_partida import ControladorPartida


partida = ControladorPartida()

print("\n=== TESTE DE PROGRESSO DA INVESTIGAÇÃO ===")

# 1. Não deve resolver um caso sem nenhuma dedução.
resultado = partida.tentar_resolver()

assert resultado["resolvido"] is False
assert len(resultado["pendencias"]) == 2

print("[OK] Não permite resolver sem deduções.")

# 2. Não deve utilizar premissas ainda não descobertas.
try:
    partida.aplicar_regra(
        "modus_ponens",
        "T >> U",
        "T"
    )
    raise AssertionError(
        "O sistema aceitou premissas não descobertas."
    )
except ValueError:
    print("[OK] Bloqueia premissas não descobertas.")

# 3. Testa o diário e a duplicação de pistas.
partida.acessar_local("sala_capitao")

primeira_investigacao = partida.investigar_local()

assert len(primeira_investigacao["pistas_novas"]) == 1

quantidade_antes = partida.diario.quantidade_pistas()

segunda_investigacao = partida.investigar_local()

assert len(segunda_investigacao["pistas_novas"]) == 0
assert partida.diario.quantidade_pistas() == quantidade_antes

print("[OK] O diário não duplica pistas.")

# 4. Explora todos os locais e conversa com os sobreviventes.
for local in partida.locais:

    partida.acessar_local(local.id)
    partida.investigar_local()

    for personagem_id in local.personagens:

        if personagem_id in partida.caso.vitimas_ids:
            continue

        partida.iniciar_conversa(personagem_id)
        partida.selecionar_escolha(0)
        partida.selecionar_escolha(0)

assert partida.diario.quantidade_pistas() == 8

print("[OK] Todas as pistas foram descobertas.")

# 5. Deduz a identidade do assassino.
alibis = [
    pista
    for pista in partida.pistas.values()
    if pista.id.startswith("alibi_")
]

hipotese = partida.pistas[
    "hipoteses_assassino"
].expressao

for pista in alibis:

    hipotese = partida.aplicar_regra(
        "silogismo_disjuntivo",
        hipotese,
        pista.expressao
    )

    assert hipotese is not None

# 6. A resolução ainda deve estar incompleta.
resultado = partida.tentar_resolver()

assert resultado["resolvido"] is False
assert resultado["pendencias"] == ["morte_secundaria"]

print("[OK] Exige também a conclusão da segunda morte.")

# 7. Deduz a segunda morte.
partida.aplicar_regra(
    "modus_ponens",
    "T >> U",
    "T"
)

resultado = partida.tentar_resolver()

assert resultado["resolvido"] is True

print("[OK] Permite resolver após demonstrar as duas conclusões.")

# 8. Não permite continuar alterando a partida resolvida.
try:
    partida.aplicar_regra(
        "modus_ponens",
        "T >> U",
        "T"
    )
    raise AssertionError(
        "O sistema permitiu deduzir após encerrar o caso."
    )
except RuntimeError:
    print("[OK] Bloqueia alterações após a resolução.")

print("\nTODOS OS TESTES DE PROGRESSO APROVADOS!")
