"""
Resumo Geral da Obra — agregado de todas as abas (equivalente simplificado
da aba "GERAL" da planilha). Chama a mesma função `calcular()` que cada
aba usa para se exibir, então o número aqui é sempre igual ao número da
aba individual — nunca uma cópia recalculada em separado.
"""

import io

import pandas as pd
import streamlit as st

import data_store
from calc import acabamentos, alvenaria, concreto_tela_pop, forro, formas, fundacao, gesso, metragens, telhado
from utils import moeda

st.title("📊 Resumo Geral da Obra")

dados = data_store.carregar()

MODULOS = [
    fundacao, concreto_tela_pop, alvenaria, gesso, forro, metragens, acabamentos, telhado, formas,
]

linhas_resumo = []
dataframes = {}
for modulo in MODULOS:
    df, totais = modulo.calcular(dados)
    dataframes[modulo.NOME] = df
    linhas_resumo.append({
        "Etapa": modulo.NOME,
        "Resumo": totais["resumo"],
        "Custo Total (R$)": totais["custo_total"],
    })

df_resumo = pd.DataFrame(linhas_resumo)
custo_total_obra = float(df_resumo["Custo Total (R$)"].sum())

st.metric("Custo total estimado da obra", moeda(custo_total_obra))
st.dataframe(df_resumo, use_container_width=True)

st.subheader("Custo por etapa")
st.bar_chart(df_resumo.set_index("Etapa")["Custo Total (R$)"])

st.divider()
st.subheader("Baixar orçamento consolidado (.xlsx)")

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_resumo.to_excel(writer, sheet_name="Resumo Geral", index=False)
    for nome, df in dataframes.items():
        if df.empty:
            continue
        aba = nome[:31]
        df.to_excel(writer, sheet_name=aba, index=False)

st.download_button(
    "⬇️ Baixar planilha consolidada (.xlsx)",
    data=buffer.getvalue(),
    file_name="orcamento_obra_consolidado.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
