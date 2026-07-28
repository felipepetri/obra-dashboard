"""
Formas (aba "FORMAS"). Conectado automaticamente ao resultado das vigas
extraídas dos `.LST` (página Inputs / Concreto e Tela Pop): o comprimento
total de vigas não é mais digitado à mão — vem da soma real do que foi
parseado. Se nenhum `.LST` foi enviado ainda, cai para os parâmetros
médios editáveis (largura/altura média de viga).
"""

import math

import pandas as pd

import catalog
import data_store

NOME = "Formas"


def calcular(dados: dict):
    parametros_gerais = dados.get("parametros_gerais", {})
    parametros_formas = dados.get("formas", {}).get("parametros", {})
    vigas = data_store.vigas_ativas(dados)

    if vigas:
        comprimento_total = sum(v["comprimento_total_m"] for v in vigas)
        largura_media = sum(v["largura_m"] for v in vigas) / len(vigas)
        altura_media = sum(v["altura_m"] for v in vigas) / len(vigas)
        fonte = f"{len(vigas)} vigas dos .LST enviados"
    else:
        comprimento_total = 0.0
        largura_media = parametros_gerais.get("largura_media_viga_m", 0.20)
        altura_media = parametros_gerais.get("altura_media_viga_m", 0.45)
        fonte = "nenhum .LST enviado — usando largura/altura média dos parâmetros gerais"

    area_lateral = comprimento_total * altura_media * 2
    area_fundo = comprimento_total * largura_media
    area_total = area_lateral + area_fundo

    cobertura_pinus = parametros_formas.get("cobertura_tabua_pinus_m2", 0.9)
    cobertura_mista = parametros_formas.get("cobertura_tabua_mista_m2", 0.8)
    espac_gravata = parametros_formas.get("espacamento_gravata_m", 0.4)
    espac_escora_viga = parametros_formas.get("espacamento_escora_viga_m", 0.4)
    espac_escora_laje = parametros_formas.get("espacamento_escora_laje_m", 0.6)
    perda_sarrafo = parametros_formas.get("perda_sarrafo", 0.15)
    escoras_laje_qtd = parametros_formas.get("escoras_lajes_qtd", 1800)

    tabuas_pinus = math.ceil(area_lateral / cobertura_pinus) if cobertura_pinus else 0
    tabuas_mistas = math.ceil(area_fundo / cobertura_mista) if cobertura_mista else 0
    sarrafos = math.ceil((comprimento_total / espac_gravata) * (1 + perda_sarrafo)) if espac_gravata else 0
    escoras_vigas = math.ceil(comprimento_total / espac_escora_viga) if espac_escora_viga else 0

    preco_tabua_pinus = catalog.preco(dados, "TÁBUAS PINUS 3 M X 0,30 M", segmento="MADEIRAS")
    preco_tabua_mista = catalog.preco(dados, "TÁBUAS MISTAS 3 M X 0,30 M", segmento="MADEIRAS")
    preco_sarrafo = catalog.preco(dados, "SARRAFOS 3M X 7 CM", segmento="MADEIRAS")
    preco_escora = catalog.preco(dados, "ESCORA METÁLICA", segmento="EQUIPAMENTOS")

    linhas = [
        {"item": "Tábuas Pinus (laterais de vigas)", "unidade": "peças", "quantidade": tabuas_pinus, "valor_unit": preco_tabua_pinus, "custo_total": round(tabuas_pinus * preco_tabua_pinus, 2)},
        {"item": "Tábuas Mistas (fundo de vigas)", "unidade": "peças", "quantidade": tabuas_mistas, "valor_unit": preco_tabua_mista, "custo_total": round(tabuas_mistas * preco_tabua_mista, 2)},
        {"item": "Sarrafos (gravatas)", "unidade": "peças", "quantidade": sarrafos, "valor_unit": preco_sarrafo, "custo_total": round(sarrafos * preco_sarrafo, 2)},
        {"item": "Escoras de Vigas", "unidade": "unidades", "quantidade": escoras_vigas, "valor_unit": preco_escora, "custo_total": round(escoras_vigas * preco_escora, 2)},
        {"item": "Escoras de Lajes", "unidade": "unidades", "quantidade": escoras_laje_qtd, "valor_unit": preco_escora, "custo_total": round(escoras_laje_qtd * preco_escora, 2)},
    ]

    df = pd.DataFrame(linhas)
    custo_total = float(df["custo_total"].sum())
    totais = {
        "custo_total": round(custo_total, 2),
        "resumo": f"{comprimento_total:.1f} m de vigas ({fonte}) — {area_total:.1f} m² de formas",
        "comprimento_total_vigas_m": round(comprimento_total, 2),
        "area_total_formas_m2": round(area_total, 2),
    }
    return df, totais
