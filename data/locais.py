
from models.local import Local


def carregar_locais():
    return [
        Local(
            id="cozinha",
            nome="Cozinha",
            descricao="Local de preparo e armazenamento dos alimentos.",
            personagens=["lee"]
        ),
        Local(
            id="sala_capitao",
            nome="Sala do Capitão",
            descricao="O escritório particular do Capitão Estevão.",
            personagens=[]
        ),
        Local(
            id="caldeira",
            nome="Caldeira",
            descricao="Compartimento responsável pelo funcionamento do motor.",
            personagens=["edi"]
        ),
        Local(
            id="enfermaria",
            nome="Enfermaria",
            descricao="Local de atendimento médico da tripulação.",
            personagens=["alizandro"]
        ),
        Local(
            id="passadico",
            nome="Passadiço do Navegante",
            descricao="Local de navegação e armazenamento dos registros do navio.",
            personagens=["marco", "pery"]
        ),
        Local(
            id="alojamentos",
            nome="Cômodos da Tripulação",
            descricao="Compartimentos destinados ao descanso dos tripulantes.",
            personagens=["ciro"]
        ),
        Local(
            id="farol",
            nome="Farol Abandonado",
            descricao="Uma antiga construção isolada na ilha congelada.",
            personagens=["cleber"]
        ),
        Local(
            id="caverna",
            nome="Caverna da Montanha",
            descricao="Uma formação rochosa nas montanhas da ilha.",
            personagens=["armando"]
        ),
        Local(
            id="casa_abandonada",
            nome="Casa Abandonada",
            descricao="Uma construção esquecida próxima à região costeira.",
            personagens=[]
        )
    ]
