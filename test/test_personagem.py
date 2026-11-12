
from data.carregador import carregar_personagens


personagens = carregar_personagens()

for personagem in personagens.values():
    print(f"Nome: {personagem.nome}")
    print(f"Cargo: {personagem.cargo}")
    print(f"Nacionalidade: {personagem.nacionalidade}")
    print(f"Arma: {personagem.arma}")
    print("-" * 30)

print("Total de personagens:", len(personagens))
