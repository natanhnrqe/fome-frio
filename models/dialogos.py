
from dataclasses import dataclass, field


@dataclass
class EscolhaDialogo:
    texto: str
    resposta: str
    proxima_etapa: str | None = None
    pista_id: str | None = None


@dataclass
class Dialogo:
    id: str
    personagem_id: str | None
    falante: str
    fala: str
    escolhas: list[EscolhaDialogo] = field(default_factory=list)
