
from data.carregador import carregar_personagens
from system.gerador_caso import GeradorCaso


personagens = carregar_personagens()
gerador = GeradorCaso()

for numero in range(10):
    caso = gerador.gerar(personagens)

    assert caso.assassino_id not in caso.vitimas_ids
    assert len(caso.vitimas_ids) == 2
    assert caso.vitima_assassinato_id in caso.vitimas_ids
    assert caso.vitima_secundaria_id in caso.vitimas_ids
    assert caso.vitima_assassinato_id != caso.vitima_secundaria_id

    print(f"\nCaso {numero + 1}")
    print(f"Assassino: {personagens[caso.assassino_id].nome}")
    print(
        "Vítima assassinada:",
        personagens[caso.vitima_assassinato_id].nome
    )
    print(
        "Vítima secundária:",
        personagens[caso.vitima_secundaria_id].nome
    )
    print("Causa secundária:", caso.causa_morte_secundaria)

print("\nTodos os testes passaram!")
