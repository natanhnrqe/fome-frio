
from system.controlador_partida import ControladorPartida


QUANTIDADE_PARTIDAS = 1000

partida = ControladorPartida()

print(f"\nIniciando teste de {QUANTIDADE_PARTIDAS} partidas...\n")

for numero in range(1, QUANTIDADE_PARTIDAS + 1):

    if numero > 1:
        partida.iniciar_nova_partida()

    # 1. Verifica a composição do caso.
    sobreviventes = [
        personagem_id
        for personagem_id in partida.personagens
        if personagem_id not in partida.caso.vitimas_ids
    ]

    assert len(sobreviventes) == 6
    assert len(partida.caso.vitimas_ids) == 2
    assert partida.caso.assassino_id in sobreviventes

    # 2. Verifica as cinco pistas de álibi.
    alibis = [
        pista
        for pista in partida.pistas.values()
        if pista.id.startswith("alibi_")
    ]

    assert len(alibis) == 5

    suspeitos_inocentes = {
        personagem_id
        for personagem_id in sobreviventes
        if personagem_id != partida.caso.assassino_id
    }

    suspeitos_das_pistas = {
        pista.id.split("alibi_", 1)[1]
        for pista in alibis
    }

    testemunhas = {
        pista.personagem_id
        for pista in alibis
    }

    assert suspeitos_das_pistas == suspeitos_inocentes
    assert len(testemunhas) == 5
    assert testemunhas == suspeitos_inocentes

    for pista in alibis:
        suspeito_id = pista.id.split("alibi_", 1)[1]

        assert pista.personagem_id != suspeito_id
        assert pista.personagem_id in sobreviventes

    # 3. Explora todos os locais e conversa com os sobreviventes.
    for local in partida.locais:

        partida.acessar_local(local.id)
        partida.investigar_local()

        for personagem_id in local.personagens:

            if personagem_id in partida.caso.vitimas_ids:
                continue

            partida.iniciar_conversa(personagem_id)

            partida.selecionar_escolha(0)
            partida.selecionar_escolha(0)

    # 4. Verifica se todas as oito pistas foram descobertas.
    assert len(partida.obter_pistas_diario()) == 8

    # 5. Aplica o silogismo disjuntivo.
    hipotese = partida.pistas[
        "hipoteses_assassino"
    ].expressao

    for pista in alibis:

        resultado = partida.aplicar_regra(
            "silogismo_disjuntivo",
            hipotese,
            pista.expressao
        )

        assert resultado is not None
        hipotese = resultado

    # 6. Confere se o resultado corresponde ao assassino sorteado.
    conclusao_assassinato = partida.conclusoes[
        "assassinato"
    ]["expressao"]

    esperado = partida.motor_logico.interpretar(
        conclusao_assassinato
    )

    assert hipotese == esperado

    # 7. Resolve a segunda morte usando modus ponens.
    resultado_secundario = partida.aplicar_regra(
        "modus_ponens",
        "T >> U",
        "T"
    )

    assert resultado_secundario is not None

    # 8. Verifica a resolução completa.
    resultado_final = partida.tentar_resolver()

    assert resultado_final["resolvido"] is True

    if numero % 100 == 0:
        print(f"{numero}/{QUANTIDADE_PARTIDAS} partidas aprovadas.")

print("\n===================================")
print("TESTE DE ESTRESSE CONCLUÍDO!")
print(f"Partidas testadas: {QUANTIDADE_PARTIDAS}")
print("Falhas: 0")
print("===================================")
