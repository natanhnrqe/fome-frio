
class SistemaInvestigacao:
    def __init__(self, mapa, diario, pistas):
        self.mapa = mapa
        self.diario = diario
        self.pistas = pistas

    def investigar_local(self):
        local = self.mapa.obter_local_atual()

        if local is None:
            raise RuntimeError(
                "É necessário estar em um local para investigá-lo."
            )

        pistas_encontradas = [
            pista
            for pista in self.pistas.values()
            if pista.local_id == local.id
        ]

        pistas_novas = []

        for pista in pistas_encontradas:
            if self.diario.registrar_pista(pista):
                pistas_novas.append(pista)

        return {
            "local": local,
            "pistas_encontradas": pistas_encontradas,
            "pistas_novas": pistas_novas
        }

    def obter_pistas_do_local_atual(self):
        local = self.mapa.obter_local_atual()

        if local is None:
            return []

        return [
            pista
            for pista in self.pistas.values()
            if pista.local_id == local.id
        ]
