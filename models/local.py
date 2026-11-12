
from dataclasses import dataclass, field


@dataclass
class Local:
    id: str
    nome: str
    descricao: str
    personagens: list[str] = field(default_factory=list)
    visitado: bool = False
    desbloqueado: bool = True
