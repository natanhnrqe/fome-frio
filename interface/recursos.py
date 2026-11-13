from pathlib import Path
import pygame

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

_CACHE = {}

def imagem(caminho, tamanho=None):
    chave = (str(caminho), tamanho)
    if chave not in _CACHE:
        arquivo = ASSETS / caminho
        if not arquivo.exists():
            return None
        img = pygame.image.load(str(arquivo)).convert()
        if tamanho:
            img = pygame.transform.smoothscale(img, tamanho)
        _CACHE[chave] = img
    return _CACHE[chave]

def fundo(superficie, nome, escurecer=100):
    img = imagem(Path("backgrounds") / nome, superficie.get_size())
    if img is None:
        superficie.fill((22, 30, 39))
        return
    superficie.blit(img, (0, 0))
    camada = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
    camada.fill((7, 13, 20, escurecer))
    superficie.blit(camada, (0, 0))

def retrato(personagem_id, tamanho=(250, 300), estado="neutro"):
    nomes = {
        "alizandro": "alizandro_pelo", "armando": "armando_cazinha",
        "ciro": "ciro_longue", "cleber": "cleber_ber",
        "edi": "edi_ficio", "lee": "lee_maonada",
        "marco": "marco_polos", "pery": "pery_siga"
    }
    pasta = nomes.get(personagem_id)
    if not pasta:
        return None
    base = Path("portraits") / pasta
    arquivo = ASSETS / base / f"{estado}.png"
    if not arquivo.exists():
        arquivo = ASSETS / base / "neutro.png"
    if not arquivo.exists():
        return None
    chave = (str(arquivo), tamanho)
    if chave not in _CACHE:
        img = pygame.image.load(str(arquivo)).convert_alpha()
        _CACHE[chave] = pygame.transform.smoothscale(img, tamanho)
    return _CACHE[chave]
