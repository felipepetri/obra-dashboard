"""Metragens dos ambientes / revestimento (piso e parede), aba
"METRAGENS DOS AMBIENTES". Aplica a perda padrão e o preço/m² (parâmetros
gerais) por tipo de revestimento."""

import pandas as pd

NOME = "Metragens dos Ambientes (Revestimento)"


def _linhas(itens, tipo, preco_m2, perda):
    linhas = []
    for a in itens:
        area_com_perda = a["area_m2"] * (1 + perda)
        custo = area_com_perda * preco_m2
        linhas.append({
            "tipo": tipo,
            "pavimento": a["pavimento"],
            "ambiente": a["nome"],
            "area_m2": a["area_m2"],
            "area_com_perda_m2": round(area_com_perda, 2),
            "preco_m2": preco_m2,
            "custo_total": round(custo, 2),
        })
    return linhas


def calcular(dados: dict):
    parametros = dados.get("parametros_gerais", {})
    perda = parametros.get("perda_padrao", 0.10)
    metragens = dados.get("metragens", {})

    linhas = _linhas(metragens.get("piso", []), "Piso", parametros.get("preco_m2_piso", 0.0), perda)
    linhas += _linhas(metragens.get("parede", []), "Parede", parametros.get("preco_m2_parede_revest", 0.0), perda)

    df = pd.DataFrame(linhas)
    custo_total = float(df["custo_total"].sum()) if not df.empty else 0.0
    area_total = float(df["area_com_perda_m2"].sum()) if not df.empty else 0.0
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{area_total:.1f} m² de revestimento (com perda)",
    }
    return df, totais
