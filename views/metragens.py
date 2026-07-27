"""Aba "METRAGENS DOS AMBIENTES" (piso e parede — revestimento)."""

import streamlit as st

import data_store
from calc import metragens
from utils import editar_tabela, moeda

st.title("📐 Metragens dos Ambientes (Revestimento)")

dados = data_store.carregar()

aba_piso, aba_parede = st.tabs(["Piso", "Parede"])

with aba_piso:
    piso = editar_tabela(dados["metragens"]["piso"], key="metragens_piso_editor")
    if piso != dados["metragens"]["piso"]:
        dados["metragens"]["piso"] = piso
        data_store.salvar(dados)

with aba_parede:
    parede = editar_tabela(dados["metragens"]["parede"], key="metragens_parede_editor")
    if parede != dados["metragens"]["parede"]:
        dados["metragens"]["parede"] = parede
        data_store.salvar(dados)

df, totais = metragens.calcular(dados)
col1, col2 = st.columns(2)
col1.metric("Área (com perda)", totais["resumo"])
col2.metric("Custo total", moeda(totais["custo_total"]))
st.dataframe(df, use_container_width=True)
st.caption("Perda padrão e preços/m² (piso/parede) ajustáveis na página Inputs.")
