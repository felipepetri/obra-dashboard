"""Acabamentos: louças, metais e torneiras (abas "TORNEIRAS,CUBAS ETC" e
"LOUÇAS E METAIS DEFINIDOS" — mescladas aqui, pois são a mesma lista de
itens na planilha original, só reapresentada). Preço unitário vem do
catálogo (segmento ACABAMENTOS)."""

import pandas as pd

import catalog

NOME = "Acabamentos (Louças, Metais e Torneiras)"


def calcular(dados: dict):
    linhas = []
    for it in dados.get("acabamentos", {}).get("itens", []):
        preco_unit = catalog.preco(dados, it["material"], segmento="ACABAMENTOS")
        total = it["qtd"] * preco_unit
        linhas.append({
            "ambiente": it["ambiente"],
            "item": it["item"],
            "material": it["material"],
            "marca": it.get("marca", ""),
            "qtd": it["qtd"],
            "valor_unit": preco_unit,
            "total": round(total, 2),
        })

    df = pd.DataFrame(linhas)
    custo_total = float(df["total"].sum()) if not df.empty else 0.0
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{len(df)} itens de louças/metais/torneiras",
    }
    return df, totais
