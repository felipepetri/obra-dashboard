"""Gesso liso (aba "GESSO LISO"). m² = comprimento x pé-direito; custo por m² é
parâmetro geral editável (a planilha original não isola um preço/m² único)."""

import pandas as pd

NOME = "Gesso Liso"


def calcular(dados: dict):
    preco_m2 = dados.get("parametros_gerais", {}).get("preco_m2_gesso", 0.0)
    linhas = []
    for p in dados.get("gesso", {}).get("paredes", []):
        m2 = p["comprimento_m"] * p["pe_direito_m"]
        linhas.append({
            "pavimento": p["pavimento"],
            "identificacao": p["identificacao"],
            "comprimento_m": p["comprimento_m"],
            "pe_direito_m": p["pe_direito_m"],
            "m2_parede": round(m2, 2),
            "preco_m2": preco_m2,
            "custo_total": round(m2 * preco_m2, 2),
        })

    df = pd.DataFrame(linhas)
    custo_total = float(df["custo_total"].sum()) if not df.empty else 0.0
    m2_total = float(df["m2_parede"].sum()) if not df.empty else 0.0
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{m2_total:.1f} m² de gesso liso",
    }
    return df, totais
