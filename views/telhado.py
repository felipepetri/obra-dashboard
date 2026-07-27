"""Aba "TELHADO "."""

import streamlit as st

import data_store
from calc import telhado
from utils import editar_tabela, moeda

st.title("🏘️ Telhado")

dados = data_store.carregar()

materiais_disponiveis = sorted({
    item["material"] for item in dados["catalogo"] if item["segmento"] == "TELHADO"
})

itens = editar_tabela(
    dados["telhado"]["itens"], key="telhado_editor",
    column_config={
        "material": st.column_config.SelectboxColumn("Material", options=materiais_disponiveis),
    },
)
if itens != dados["telhado"]["itens"]:
    dados["telhado"]["itens"] = itens
    data_store.salvar(dados)

df, totais = telhado.calcular(dados)
col1, col2 = st.columns(2)
col1.metric("Itens", totais["resumo"])
col2.metric("Custo total", moeda(totais["custo_total"]))
st.dataframe(df, use_container_width=True)
st.caption("Preço unitário vem do catálogo (página Inputs, segmento TELHADO).")
