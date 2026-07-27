"""Abas "TORNEIRAS,CUBAS ETC" + "LOUÇAS E METAIS DEFINIDOS" (mescladas)."""

import streamlit as st

import data_store
from calc import acabamentos
from utils import editar_tabela, moeda

st.title("🚿 Acabamentos (Louças, Metais e Torneiras)")
st.caption(
    "Na planilha original estas eram duas abas com a mesma lista de itens "
    "reapresentada — aqui viram uma única tabela editável."
)

dados = data_store.carregar()

materiais_disponiveis = sorted({
    item["material"] for item in dados["catalogo"] if item["segmento"] == "ACABAMENTOS"
})

itens = editar_tabela(
    dados["acabamentos"]["itens"], key="acabamentos_editor",
    column_config={
        "material": st.column_config.SelectboxColumn("Material", options=materiais_disponiveis),
    },
)
if itens != dados["acabamentos"]["itens"]:
    dados["acabamentos"]["itens"] = itens
    data_store.salvar(dados)

df, totais = acabamentos.calcular(dados)
col1, col2 = st.columns(2)
col1.metric("Itens", totais["resumo"])
col2.metric("Custo total", moeda(totais["custo_total"]))
st.dataframe(df, use_container_width=True)
st.caption("Preço unitário vem do catálogo (página Inputs, segmento ACABAMENTOS).")
