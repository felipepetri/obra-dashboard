"""Aba "GESSO LISO"."""

import streamlit as st

import data_store
from calc import gesso
from utils import editar_tabela, moeda

st.title("🎨 Gesso Liso")

dados = data_store.carregar()

paredes = editar_tabela(dados["gesso"]["paredes"], key="gesso_editor")
if paredes != dados["gesso"]["paredes"]:
    dados["gesso"]["paredes"] = paredes
    data_store.salvar(dados)

df, totais = gesso.calcular(dados)
col1, col2 = st.columns(2)
col1.metric("Área", totais["resumo"])
col2.metric("Custo total", moeda(totais["custo_total"]))
st.dataframe(df, use_container_width=True)
st.caption("Preço/m² ajustável na página Inputs (parâmetros gerais).")
