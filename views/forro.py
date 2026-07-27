"""Aba "(FORRO)"."""

import streamlit as st

import data_store
from calc import forro
from utils import editar_tabela, moeda

st.title("🏠 Forro")

dados = data_store.carregar()

ambientes = editar_tabela(dados["forro"]["ambientes"], key="forro_editor")
if ambientes != dados["forro"]["ambientes"]:
    dados["forro"]["ambientes"] = ambientes
    data_store.salvar(dados)

df, totais = forro.calcular(dados)
col1, col2 = st.columns(2)
col1.metric("Área", totais["resumo"])
col2.metric("Custo total", moeda(totais["custo_total"]))
st.dataframe(df, use_container_width=True)
st.caption("Preço/m² ajustável na página Inputs (parâmetros gerais).")
