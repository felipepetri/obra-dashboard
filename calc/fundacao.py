"""
Fundação: estacas + blocos e vigas baldrame (aba "CONCRETO E TELA POP",
seções superiores da planilha). Volume/perda seguem a mesma lógica de
models.Viga/Pilar; o preço do concreto vem sempre do catálogo.
"""

import math

import pandas as pd

import catalog

NOME = "Fundação (Estacas e Blocos Baldrame)"


def calcular(dados: dict):
    parametros = dados.get("parametros_gerais", {})
    perda = parametros.get("perda_padrao", 0.10)
    fundacao = dados.get("fundacao", {})

    linhas = []
    for e in fundacao.get("estacas", []):
        volume = math.pi / 4 * (e["diametro_m"] ** 2) * e["profundidade_m"]
        total_m3 = volume * e["qtd"]
        total_perda = total_m3 * (1 + perda)
        custo_m3 = catalog.preco_concreto_m3(dados, e["fck_mpa"])
        linhas.append({
            "grupo": "Estaca",
            "item": e["tipo"],
            "quantidade": e["qtd"],
            "volume_unitario_m3": round(volume, 4),
            "volume_total_m3": round(total_m3, 3),
            "volume_com_perda_m3": round(total_perda, 3),
            "custo_concreto_m3": custo_m3,
            "custo_total": round(total_perda * custo_m3, 2),
        })

    for b in fundacao.get("blocos_baldrame", []):
        volume = b["comprimento_m"] * b["largura_m"] * b["altura_m"]
        total_m3 = volume * b["quantidade"]
        total_perda = total_m3 * (1 + perda)
        custo_m3 = catalog.preco_concreto_m3(dados, b["fck_mpa"])
        linhas.append({
            "grupo": "Bloco Baldrame",
            "item": b["nomenclatura"],
            "quantidade": b["quantidade"],
            "volume_unitario_m3": round(volume, 4),
            "volume_total_m3": round(total_m3, 3),
            "volume_com_perda_m3": round(total_perda, 3),
            "custo_concreto_m3": custo_m3,
            "custo_total": round(total_perda * custo_m3, 2),
        })

    df = pd.DataFrame(linhas)
    custo_total = float(df["custo_total"].sum()) if not df.empty else 0.0
    volume_total = float(df["volume_com_perda_m3"].sum()) if not df.empty else 0.0
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{volume_total:.2f} m³ de concreto (estacas + blocos baldrame)",
    }
    return df, totais
