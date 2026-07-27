"""
Alvenaria e embasamento (aba "ALVENARIA E EMBASAMENTO"). Simplificação:
em vez de reproduzir fiada a fiada, calcula m² de parede e converte para
quantidade de blocos pela área da face de cada tipo de bloco. O custo por
bloco vem do catálogo (segmento BLOCOS) — editável na página de Inputs.
"""

import math

import pandas as pd

import catalog

NOME = "Alvenaria e Embasamento"

# Face do bloco (comprimento x altura, em m) usada para converter m² -> quantidade.
# Simplificação: a planilha original varia fiada a fiada; aqui usamos a área
# da face do bloco deitado, que é a mesma lógica de fundo (m² / área-por-bloco).
FACE_BLOCO_M2 = {
    "CONCRETO 14X19X39": 0.39 * 0.19,
    "CERAMICO 14X19X39": 0.39 * 0.19,
    "CONCRETO 19X19X19": 0.19 * 0.19,
}


def calcular(dados: dict):
    alvenaria = dados.get("alvenaria", {})
    linhas = []
    for p in alvenaria.get("paredes", []):
        m2 = p["comprimento_m"] * p["altura_m"]
        bloco = p.get("bloco", "CERAMICO 14X19X39")
        face = FACE_BLOCO_M2.get(bloco, 0.39 * 0.19)
        qtd_blocos = math.ceil(m2 / face) if m2 > 0 else 0
        preco_bloco = catalog.preco(dados, bloco, segmento="BLOCOS")
        custo = qtd_blocos * preco_bloco
        linhas.append({
            "pavimento": p["pavimento"],
            "identificacao": p["identificacao"],
            "comprimento_m": p["comprimento_m"],
            "altura_m": p["altura_m"],
            "m2_parede": round(m2, 2),
            "bloco": bloco,
            "qtd_blocos": qtd_blocos,
            "preco_unit_bloco": preco_bloco,
            "custo_total": round(custo, 2),
        })

    df = pd.DataFrame(linhas)
    custo_total = float(df["custo_total"].sum()) if not df.empty else 0.0
    m2_total = float(df["m2_parede"].sum()) if not df.empty else 0.0
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{m2_total:.1f} m² de alvenaria",
    }
    return df, totais
