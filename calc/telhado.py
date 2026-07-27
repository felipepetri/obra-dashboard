"""Telhado (aba "TELHADO "). Preço unitário vem do catálogo (segmento TELHADO)."""

import pandas as pd

import catalog

NOME = "Telhado"


def calcular(dados: dict):
    linhas = []
    for it in dados.get("telhado", {}).get("itens", []):
        preco_unit = catalog.preco(dados, it["material"], segmento="TELHADO")
        subtotal = it["quantidade"] * preco_unit
        linhas.append({
            "categoria": it["categoria"],
            "material": it["material"],
            "unidade": it["unidade"],
            "quantidade": it["quantidade"],
            "valor_unit": preco_unit,
            "subtotal": round(subtotal, 2),
        })

    df = pd.DataFrame(linhas)
    custo_total = float(df["subtotal"].sum()) if not df.empty else 0.0
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{len(df)} itens de telhado",
    }
    return df, totais
