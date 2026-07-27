"""Aba "FORMAS" — conectada automaticamente às vigas processadas em Inputs."""

import streamlit as st

import data_store
from calc import formas
from utils import moeda

st.title("🪵 Formas")

dados = data_store.carregar()

with st.expander("Parâmetros de cálculo (cobertura, espaçamentos)"):
    fp = dados["formas"]["parametros"]
    col1, col2, col3 = st.columns(3)
    with col1:
        fp["cobertura_tabua_pinus_m2"] = st.number_input("Cobertura tábua pinus (m²/peça)", value=fp.get("cobertura_tabua_pinus_m2", 0.9), step=0.05)
        fp["cobertura_tabua_mista_m2"] = st.number_input("Cobertura tábua mista (m²/peça)", value=fp.get("cobertura_tabua_mista_m2", 0.8), step=0.05)
    with col2:
        fp["espacamento_gravata_m"] = st.number_input("Espaçamento gravatas (m)", value=fp.get("espacamento_gravata_m", 0.4), step=0.05)
        fp["espacamento_escora_viga_m"] = st.number_input("Espaçamento escoras de viga (m)", value=fp.get("espacamento_escora_viga_m", 0.4), step=0.05)
        fp["espacamento_escora_laje_m"] = st.number_input("Espaçamento escoras de laje (m)", value=fp.get("espacamento_escora_laje_m", 0.6), step=0.05)
    with col3:
        fp["perda_sarrafo"] = st.number_input("Perda de sarrafos (%)", value=fp.get("perda_sarrafo", 0.15) * 100, step=1.0) / 100
        fp["escoras_lajes_qtd"] = st.number_input("Quantidade de escoras de laje", value=fp.get("escoras_lajes_qtd", 1800), step=10)
    dados["formas"]["parametros"] = fp
    data_store.salvar(dados)

df, totais = formas.calcular(dados)
col1, col2 = st.columns(2)
col1.metric("Vigas / formas", totais["resumo"])
col2.metric("Custo total", moeda(totais["custo_total"]))
st.dataframe(df, use_container_width=True)
st.caption(
    "O comprimento total de vigas vem automaticamente das dimensões processadas "
    "na página Inputs (upload dos .LST) — não precisa ser digitado aqui."
)
