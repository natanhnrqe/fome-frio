"""Carregamento e composição de imagens da interface.

Os cenários têm proporção retrato (414x466) e os retratos são 768x1024.
Por isso, nenhum asset é esticado: cenários usam recorte tipo "cover" com
ponto focal configurável e personagens são escalados apenas pela altura.
"""

from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

_CACHE: dict[tuple, pygame.Surface] = {}

# Ponto focal preserva o miolo importante de cada cenário durante o recorte.
FOCOS = {
    "ilha.png": (0.50, 0.48),
    "cozinha.png": (0.52, 0.52),
    "conves.png": (0.50, 0.50),
    "caldeira.png": (0.48, 0.50),
    "enfermaria.png": (0.50, 0.52),
    "passadico_navegante.png": (0.50, 0.52),
    "comodos_tripulacao.png": (0.50, 0.50),
    "deposito.png": (0.50, 0.50),
}

_NOMES_RETRATOS = {
    "alizandro": "alizandro_pelo",
    "armando": "armando_cazinha",
    "ciro": "ciro_longue",
    "cleber": "cleber_ber",
    "edi": "edi_ficio",
    "lee": "lee_maonada",
    "marco": "marco_polos",
    "pery": "pery_siga",
    "estevao": "estevao_firme",
}


def _original(caminho: str | Path) -> pygame.Surface | None:
    chave = ("original", str(caminho))
    if chave in _CACHE:
        return _CACHE[chave]

    arquivo = ASSETS / caminho
    if not arquivo.exists():
        return None

    imagem = pygame.image.load(str(arquivo)).convert_alpha()
    _CACHE[chave] = imagem
    return imagem


def imagem(caminho, tamanho=None):
    """Compatibilidade: carrega uma imagem, opcionalmente em um tamanho exato."""
    chave = (str(caminho), tuple(tamanho) if tamanho else None)
    if chave in _CACHE:
        return _CACHE[chave]

    base = _original(caminho)
    if base is None:
        return None

    if tamanho:
        imagem_final = pygame.transform.smoothscale(base, tamanho)
        _CACHE[chave] = imagem_final
        return imagem_final

    return base


def _cover(imagem_base: pygame.Surface, tamanho, foco) -> pygame.Surface:
    """Escala sem distorcer e recorta o excesso em torno do ponto focal."""
    largura, altura = int(tamanho[0]), int(tamanho[1])
    original_l, original_a = imagem_base.get_size()

    escala = max(largura / original_l, altura / original_a)
    nova_l = max(largura, round(original_l * escala))
    nova_a = max(altura, round(original_a * escala))

    escalada = pygame.transform.smoothscale(imagem_base, (nova_l, nova_a))
    resultado = pygame.Surface((largura, altura)).convert()

    deslocamento_x = round((nova_l - largura) * float(foco[0]))
    deslocamento_y = round((nova_a - altura) * float(foco[1]))

    resultado.blit(escalada, (-deslocamento_x, -deslocamento_y))
    return resultado


def imagem_fundo(caminho: str | Path, tamanho, foco=None) -> pygame.Surface | None:
    foco = tuple(foco) if foco is not None else FOCOS.get(Path(caminho).name, (0.5, 0.5))
    chave = ("fundo", str(caminho), tuple(tamanho), foco)
    if chave in _CACHE:
        return _CACHE[chave]

    base = _original(caminho)
    if base is None:
        return None

    resultado = _cover(base, tamanho, foco)
    _CACHE[chave] = resultado
    return resultado


_OVERLAYS: dict[tuple, pygame.Surface] = {}


def _overlay(tamanho, cor, alpha) -> pygame.Surface:
    chave = (tuple(tamanho), tuple(cor), int(alpha))
    if chave not in _OVERLAYS:
        camada = pygame.Surface(tuple(tamanho), pygame.SRCALPHA)
        camada.fill((*cor, int(alpha)))
        _OVERLAYS[chave] = camada
    return _OVERLAYS[chave]


def fundo(superficie, nome, escurecer=100, foco=None):
    """Desenha um cenário ocupando a tela inteira, sem esticar a arte."""
    tamanho = superficie.get_size()
    nome = Path(nome).name
    img = imagem_fundo(Path("backgrounds") / nome, tamanho, foco)

    if img is None:
        superficie.fill((22, 30, 39))
        return

    superficie.blit(img, (0, 0))
    if escurecer:
        superficie.blit(_overlay(tamanho, (7, 12, 18), escurecer), (0, 0))


def _caminho_retrato(personagem_id: str, estado: str) -> Path | None:
    pasta = _NOMES_RETRATOS.get(personagem_id)
    if not pasta:
        return None

    base = Path("portraits") / pasta
    arquivo = ASSETS / base / f"{estado}.png"
    if not arquivo.exists():
        arquivo = ASSETS / base / "neutro.png"
    if not arquivo.exists():
        return None

    return arquivo


def retrato(personagem_id, altura=520, estado="neutro", tamanho=None):
    """Retorna o retrato escalado somente pela altura, mantendo a proporção.

    O argumento ``tamanho`` existe apenas por compatibilidade com a interface
    antiga; quando informado, sua altura é usada e a largura é recalculada.
    """
    if tamanho:
        altura = int(tamanho[1])

    arquivo = _caminho_retrato(personagem_id, estado)
    if arquivo is None:
        return None

    chave = ("retrato", str(arquivo), int(altura))
    if chave in _CACHE:
        return _CACHE[chave]

    base = _original(arquivo)
    if base is None:
        return None

    largura_original, altura_original = base.get_size()
    nova_altura = max(1, int(altura))
    nova_largura = max(1, round(largura_original * nova_altura / altura_original))
    resultado = pygame.transform.smoothscale(base, (nova_largura, nova_altura))
    _CACHE[chave] = resultado
    return resultado


def recorte_rosto(personagem_id, tamanho, estado="neutro"):
    """Recorte de busto para cartões e listas de suspeitos."""
    arquivo = _caminho_retrato(personagem_id, estado)
    if arquivo is None:
        return None

    chave = ("rosto", str(arquivo), tuple(tamanho))
    if chave in _CACHE:
        return _CACHE[chave]

    base = _original(arquivo)
    if base is None:
        return None

    largura_original, altura_original = base.get_size()
    recorte = pygame.Rect(
        round(largura_original * 0.12),
        round(altura_original * 0.025),
        round(largura_original * 0.76),
        round(altura_original * 0.54),
    )
    busto = base.subsurface(recorte).copy()
    resultado = _cover(busto, tamanho, (0.5, 0.35))
    _CACHE[chave] = resultado
    return resultado
