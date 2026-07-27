"""
Vigas e pilares extraídos dos `.LST` do TQS (aba "CONCRETO E TELA POP").
Reaproveita a lógica existente em `calculos.py`/`models.py`; os dados de
entrada (vigas já agregadas por pavimento) vêm do que foi salvo em
`dados["lst_dados"]` pela página de Inputs após o upload dos `.LST`.
"""

import pandas as pd

import calculos
from models import Pilar, Viga

NOME = "Vigas e Pilares (TQS)"


def calcular(dados: dict):
    fck_padrao = dados.get("parametros_gerais", {}).get("fck_padrao_mpa", 25)
    vigas_salvas = dados.get("lst_dados", {}).get("vigas", [])

    vigas = [
        Viga(
            nomenclatura=v["viga"],
            largura=v["largura_m"],
            comprimento=v["comprimento_total_m"],
            profundidade=v["altura_m"],
            fck=fck_padrao,
            pavimento=v["pavimento"],
        )
        for v in vigas_salvas
    ]
    # Pilares extraídos do TQS não trazem largura x profundidade (só área/volume
    # reais) — mesma limitação da planilha original, ficam de fora do custo por
    # Fck até serem completados manualmente (ver README).
    pilares: list[Pilar] = []

    resumo = calculos.resumir(vigas, pilares, dados)
    df = pd.DataFrame(resumo.itens)
    totais = {
        "custo_total": round(resumo.custo_total, 2),
        "resumo": f"{resumo.volume_concreto_m3:.2f} m³ de concreto em vigas",
    }
    return df, totais
