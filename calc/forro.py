"""Forro (aba "(FORRO)"). Soma de m² por ambiente x preço/m² (parâmetro geral)."""

import pandas as pd

NOME = "Forro"


def calcular(dados: dict):
    preco_m2 = dados.get("parametros_gerais", {}).get("preco_m2_forro", 0.0)
    linhas = []
    for a in dados.get("forro", {}).get("ambientes", []):
        custo = a["area_m2"] * preco_m2
        linhas.append({
            "pavimento": a["pavimento"],
            "ambiente": a["nome"],
            "area_m2": a["area_m2"],
            "preco_m2": preco_m2,
            "custo_total": round(custo, 2),
        })

    df = pd.DataFrame(linhas)
    custo_total = float(df["custo_total"].sum()) if not df.empty else 0.0
    area_total = float(df["area_m2"].sum()) if not df.empty else 0.0
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{area_total:.1f} m² de forro",
    }
    return df, totais
