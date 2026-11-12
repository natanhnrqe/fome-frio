
class Mapa:
    def __init__(self, locais: list):
        self.locais = {
            local.id: local
            for local in locais
        }

        self.local_atual = None

    def iniciar_exploracao(self, local_id: str):
        return self.acessar_local(local_id)

    def acessar_local(self, local_id: str):
        local = self.locais.get(local_id)

        if local is None:
            raise ValueError(f"Local '{local_id}' não encontrado.")

        if not local.desbloqueado:
            return False

        self.local_atual = local
        local.visitado = True

        return True

    def obter_local_atual(self):
        return self.local_atual

    def listar_locais(self):
        return list(self.locais.values())

    def listar_locais_visitados(self):
        return [
            local
            for local in self.locais.values()
            if local.visitado
        ]

    def listar_personagens_no_local(self):
        if self.local_atual is None:
            return []

        return self.local_atual.personagens

    def desbloquear_local(self, local_id: str):
        local = self.locais.get(local_id)

        if local is None:
            raise ValueError(f"Local '{local_id}' não encontrado.")

        local.desbloqueado = True

    def voltar_ao_mapa(self):
        self.local_atual = None
