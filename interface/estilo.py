"""Identidade visual central de Fome e Frio.

Toda dimensão, cor e tipografia usada pela interface deve passar por aqui.
O jogo é composto em uma superfície lógica de 1280x720; o pygame escala essa
superfície para a janela real preservando a proporção da imagem.
"""

from __future__ import annotations

import re
from pathlib import Path

import pygame

LARGURA = 1280
ALTURA = 720

MARGEM = 36
RAIO = 10
RAIO_PEQUENO = 7

TOPO_Y = 26
TOPO_ALTURA = 40

# Caixa de diálogo à esquerda; o personagem ativo permanece em pé à direita,
# em altura cheia e apoiado no chão da cena.
PAINEL_DIALOGO = pygame.Rect(48, 454, 792, 240)
ALTURA_PERSONAGEM_DIALOGO = 540
BASE_PERSONAGEM_DIALOGO = 700

# ---------------------------------------------------------------
# Cores
# ---------------------------------------------------------------

TINTA = (9, 14, 20)
FUNDO = (13, 20, 28)
FUNDO_CLARO = (21, 33, 44)
PAINEL = (18, 29, 39)
PAINEL_ALTO = (25, 40, 52)
PAINEL_CLARO = (34, 52, 66)
BORDA = (56, 78, 94)
BORDA_CLARA = (92, 121, 139)
BORDA_FORTE = (126, 156, 174)

DOURADO = (205, 158, 83)
DOURADO_CLARO = (236, 199, 132)
DOURADO_ESCURO = (151, 111, 51)

GELO = (145, 178, 199)
GELO_CLARO = (196, 218, 231)

TEXTO = (233, 228, 216)
TEXTO_SUAVE = (174, 188, 198)
TEXTO_FRACO = (124, 141, 153)
TEXTO_ESCURO = (28, 21, 11)

SUCESSO = (143, 184, 137)
PERIGO = (201, 121, 104)
PERIGO_CLARO = (231, 168, 153)

SOMBRA = (2, 5, 8)


# ---------------------------------------------------------------
# Tipografia
# ---------------------------------------------------------------

_FAMILIAS = {
    "titulo": "georgia",
    "corpo": "georgia",
    "ui": "segoeui",
    "mono": "consolas",
    # Cambria cobre os conectivos lógicos (∨, ∧, →, ¬) que a Segoe UI
    # disponível no pygame não desenha em todas as versões do Windows.
    "logica": "cambria",
}

# A fonte de lógica é empacotada com o jogo: se a máquina não tiver Cambria,
# os conectivos não podem virar quadrados vazios. DejaVu Serif cobre todo o
# conjunto usado na interface (¬, ∧, ∨, →, ⇒).
_DIR_FONTES = Path(__file__).resolve().parent.parent / "assets" / "fonts"
_ARQUIVOS_LOGICA = {
    False: _DIR_FONTES / "DejaVuSerif-Regular.ttf",
    True: _DIR_FONTES / "DejaVuSerif-Bold.ttf",
}

_FONTES: dict[tuple[str, int, bool], pygame.font.Font] = {}


def fonte(nome: str = "corpo", tamanho: int = 20, negrito: bool = False) -> pygame.font.Font:
    """Retorna uma fonte em cache, com famílias consistentes no jogo inteiro."""
    chave = (nome, int(tamanho), bool(negrito))
    if chave not in _FONTES:
        if nome == "logica":
            arquivo = _ARQUIVOS_LOGICA[bool(negrito)]
            if arquivo.exists():
                _FONTES[chave] = pygame.font.Font(str(arquivo), int(tamanho))
                return _FONTES[chave]

        familia = _FAMILIAS.get(nome, _FAMILIAS["ui"])
        _FONTES[chave] = pygame.font.SysFont(familia, int(tamanho), bold=negrito)
    return _FONTES[chave]


def formatar_logica(texto) -> str:
    """Converte a notação interna do motor em notação legível na interface.

    O backend usa ``|``, ``&``, ``~`` e ``>>``. A apresentação usa os
    conectivos tipográficos correspondentes, sem alterar as expressões
    enviadas ao motor lógico.
    """
    formatado = re.sub(
        r"Implies\(([^,]+),\s*([^)]+)\)",
        r"\1 → \2",
        str(texto),
    )
    return (
        formatado
        .replace(">>", " → ")
        .replace("|", " ∨ ")
        .replace("&", " ∧ ")
        .replace("~", "¬")
        .replace("  ", " ")
        .strip()
    )


# ---------------------------------------------------------------
# Texto
# ---------------------------------------------------------------

def quebrar_texto(texto: str, fonte_usada: pygame.font.Font, largura: int) -> list[str]:
    """Quebra texto em linhas que caibam na largura informada."""
    largura = max(1, int(largura))
    linhas: list[str] = []

    for paragrafo in str(texto).split("\n"):
        if not paragrafo:
            linhas.append("")
            continue

        atual = ""
        for palavra in paragrafo.split():
            tentativa = palavra if not atual else f"{atual} {palavra}"

            if fonte_usada.size(tentativa)[0] <= largura:
                atual = tentativa
                continue

            if atual:
                linhas.append(atual)
                atual = ""

            # Palavras maiores que a linha são partidas para nunca vazar.
            if fonte_usada.size(palavra)[0] > largura:
                pedaco = ""
                for caractere in palavra:
                    tentativa_pedaco = pedaco + caractere
                    if pedaco and fonte_usada.size(tentativa_pedaco)[0] > largura:
                        linhas.append(pedaco)
                        pedaco = caractere
                    else:
                        pedaco = tentativa_pedaco
                atual = pedaco
            else:
                atual = palavra

        if atual:
            linhas.append(atual)

    return linhas or [""]


def desenhar_paragrafo(
    superficie: pygame.Surface,
    texto: str,
    fonte_usada: pygame.font.Font,
    cor: tuple[int, int, int],
    rect,
    espacamento: int = 5,
    limite_linhas: int | None = None,
) -> int:
    """Desenha um parágrafo com quebra de linha e recorte na área indicada."""
    rect = pygame.Rect(rect)
    if rect.w <= 0 or rect.h <= 0:
        return 0

    linhas = quebrar_texto(texto, fonte_usada, rect.w)
    if limite_linhas is not None:
        linhas = linhas[:limite_linhas]

    recorte_anterior = superficie.get_clip()
    superficie.set_clip(rect)

    y = rect.y
    altura_linha = fonte_usada.get_linesize()
    for linha in linhas:
        if y + altura_linha > rect.bottom:
            break
        if linha:
            imagem = fonte_usada.render(linha, True, cor)
            superficie.blit(imagem, (rect.x, y))
        y += altura_linha + espacamento

    superficie.set_clip(recorte_anterior)
    return y - rect.y


def desenhar_texto(
    superficie: pygame.Surface,
    texto: str,
    fonte_usada: pygame.font.Font,
    cor: tuple[int, int, int],
    pos,
    alinhamento: str = "esquerda",
) -> pygame.Rect:
    imagem = fonte_usada.render(str(texto), True, cor)
    rect = imagem.get_rect()

    if alinhamento == "centro":
        rect.midtop = pos
    elif alinhamento == "direita":
        rect.topright = pos
    else:
        rect.topleft = pos

    superficie.blit(imagem, rect)
    return rect


def desenhar_texto_espacado(
    superficie: pygame.Surface,
    texto: str,
    fonte_usada: pygame.font.Font,
    cor: tuple[int, int, int],
    pos,
    espacamento: int = 2,
) -> pygame.Rect:
    """Small caps com espaçamento manual, usado nos rótulos de seção."""
    texto = str(texto).upper()
    letras = [fonte_usada.render(caractere, True, cor) for caractere in texto]
    largura = sum(letra.get_width() for letra in letras)
    largura += max(0, len(letras) - 1) * espacamento
    altura = fonte_usada.get_height()

    rect = pygame.Rect(pos[0], pos[1], largura, altura)
    x = rect.x
    for letra in letras:
        superficie.blit(letra, (x, rect.y))
        x += letra.get_width() + espacamento
    return rect


# ---------------------------------------------------------------
# Superfícies e painéis
# ---------------------------------------------------------------

_GRADIENTES: dict[tuple, pygame.Surface] = {}
_OVERLAYS: dict[tuple, pygame.Surface] = {}


def gradiente_vertical(
    tamanho,
    cor_inicio: tuple[int, int, int],
    cor_fim: tuple[int, int, int],
    alpha_inicio: int,
    alpha_fim: int,
) -> pygame.Surface:
    chave = ("v", tuple(tamanho), cor_inicio, cor_fim, alpha_inicio, alpha_fim)
    if chave in _GRADIENTES:
        return _GRADIENTES[chave]

    largura, altura = int(tamanho[0]), int(tamanho[1])
    superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
    divisor = max(1, altura - 1)

    for y in range(altura):
        t = y / divisor
        cor = (
            int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * t),
            int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * t),
            int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * t),
            int(alpha_inicio + (alpha_fim - alpha_inicio) * t),
        )
        pygame.draw.line(superficie, cor, (0, y), (largura, y))

    _GRADIENTES[chave] = superficie
    return superficie


def gradiente_horizontal(
    tamanho,
    cor_inicio: tuple[int, int, int],
    cor_fim: tuple[int, int, int],
    alpha_inicio: int,
    alpha_fim: int,
) -> pygame.Surface:
    chave = ("h", tuple(tamanho), cor_inicio, cor_fim, alpha_inicio, alpha_fim)
    if chave in _GRADIENTES:
        return _GRADIENTES[chave]

    largura, altura = int(tamanho[0]), int(tamanho[1])
    superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)
    divisor = max(1, largura - 1)

    for x in range(largura):
        t = x / divisor
        cor = (
            int(cor_inicio[0] + (cor_fim[0] - cor_inicio[0]) * t),
            int(cor_inicio[1] + (cor_fim[1] - cor_inicio[1]) * t),
            int(cor_inicio[2] + (cor_fim[2] - cor_inicio[2]) * t),
            int(alpha_inicio + (alpha_fim - alpha_inicio) * t),
        )
        pygame.draw.line(superficie, cor, (x, 0), (x, altura))

    _GRADIENTES[chave] = superficie
    return superficie


def overlay(tamanho, cor: tuple[int, int, int], alpha: int) -> pygame.Surface:
    chave = (tuple(tamanho), cor, int(alpha))
    if chave not in _OVERLAYS:
        superficie = pygame.Surface((int(tamanho[0]), int(tamanho[1])), pygame.SRCALPHA)
        superficie.fill((*cor, int(alpha)))
        _OVERLAYS[chave] = superficie
    return _OVERLAYS[chave]


def aplicar_vinheta(superficie: pygame.Surface) -> None:
    largura, altura = superficie.get_size()

    superficie.blit(
        gradiente_vertical((largura, 190), (5, 9, 14), (5, 9, 14), 175, 0),
        (0, 0),
    )
    superficie.blit(
        gradiente_vertical((largura, 250), (5, 9, 14), (5, 9, 14), 0, 215),
        (0, altura - 250),
    )
    superficie.blit(
        gradiente_horizontal((170, altura), (5, 9, 14), (5, 9, 14), 135, 0),
        (0, 0),
    )
    superficie.blit(
        gradiente_horizontal((170, altura), (5, 9, 14), (5, 9, 14), 0, 135),
        (largura - 170, 0),
    )


def desenhar_painel(
    superficie: pygame.Surface,
    rect,
    cor: tuple[int, int, int] = PAINEL,
    borda: tuple[int, int, int] = BORDA,
    raio: int = RAIO,
    alpha: int = 238,
    sombra: bool = True,
    brilho_superior: bool = True,
) -> pygame.Rect:
    rect = pygame.Rect(rect)

    if sombra:
        camada_sombra = pygame.Surface((rect.w + 16, rect.h + 18), pygame.SRCALPHA)
        pygame.draw.rect(
            camada_sombra,
            (0, 0, 0, 95),
            pygame.Rect(8, 8, rect.w, rect.h),
            border_radius=raio + 2,
        )
        superficie.blit(camada_sombra, (rect.x - 8, rect.y - 4))

    camada = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(camada, (*cor, alpha), camada.get_rect(), border_radius=raio)
    pygame.draw.rect(camada, (*borda, 255), camada.get_rect(), 1, border_radius=raio)

    if brilho_superior:
        pygame.draw.line(
            camada,
            (255, 255, 255, 22),
            (raio + 2, 1),
            (rect.w - raio - 2, 1),
        )

    superficie.blit(camada, rect.topleft)
    return rect


def desenhar_divisoria(
    superficie: pygame.Surface,
    x1: int,
    x2: int,
    y: int,
    cor: tuple[int, int, int] = BORDA,
    alpha: int = 120,
) -> None:
    camada = pygame.Surface((max(1, x2 - x1), 1), pygame.SRCALPHA)
    camada.fill((*cor, alpha))
    superficie.blit(camada, (x1, y))


def desenhar_ponto(
    superficie: pygame.Surface,
    centro,
    raio: int,
    cor: tuple[int, int, int],
    alpha: int = 255,
) -> None:
    camada = pygame.Surface((raio * 2 + 2, raio * 2 + 2), pygame.SRCALPHA)
    pygame.draw.circle(camada, (*cor, alpha), (raio + 1, raio + 1), raio)
    superficie.blit(camada, (centro[0] - raio - 1, centro[1] - raio - 1))


def desenhar_etiqueta(
    superficie: pygame.Surface,
    rect,
    texto: str,
    cor: tuple[int, int, int] = DOURADO,
    fundo_cor: tuple[int, int, int] = TINTA,
    alpha: int = 255,
) -> pygame.Rect:
    rect = pygame.Rect(rect)
    camada = pygame.Surface(rect.size, pygame.SRCALPHA)
    camada.fill((*fundo_cor, alpha))
    pygame.draw.rect(camada, (*cor, 220), camada.get_rect(), 1, border_radius=4)
    superficie.blit(camada, rect.topleft)

    texto_img = fonte("ui", 11, True).render(str(texto).upper(), True, cor)
    superficie.blit(texto_img, texto_img.get_rect(center=rect.center))
    return rect
