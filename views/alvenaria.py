"""Aba "ALVENARIA E EMBASAMENTO"."""

import streamlit as st

import data_store
from calc import alvenaria
from utils import editar_tabela, moeda

st.title("🧱 Alvenaria e Embasamento")

dados = data_store.carregar()

paredes = editar_tabela(
    dados["alvenaria"]["paredes"], key="alvenaria_editor",
    column_config={
        "bloco": st.column_config.SelectboxColumn(
            "Bloco", options=["CONCRETO 14X19X39", "CERAMICO 14X19X39", "CONCRETO 19X19X19"]
        ),
    },
)
if paredes != dados["alvenaria"]["paredes"]:
    dados["alvenaria"]["paredes"] = paredes
    data_store.salvar(dados)

df, totais = alvenaria.calcular(dados)
col1, col2 = st.columns(2)
col1.metric("Área", totais["resumo"])
col2.metric("Custo total", moeda(totais["custo_total"]))
st.dataframe(df, use_container_width=True)
st.caption(
    "Quantidade de blocos estimada por m² de parede / área da face do bloco "
    "(simplificação — a planilha original conta fiada a fiada). O preço por "
    "bloco vem do catálogo (página Inputs, segmento BLOCOS)."
)
