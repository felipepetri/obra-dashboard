"""Vigas/pilares (TQS) + fundação (estacas e blocos baldrame) — aba
"CONCRETO E TELA POP" da planilha original."""

import streamlit as st

import data_store
from calc import concreto_tela_pop, fundacao
from utils import editar_tabela, moeda

st.title("🏗️ Concreto e Tela Pop")
st.caption(
    "Vigas e pilares vêm do processamento dos .LST na página de Inputs. "
    "Estacas e blocos de baldrame são editáveis aqui."
)

dados = data_store.carregar()

aba_vigas, aba_fundacao = st.tabs(["Vigas e Pilares (TQS)", "Fundação (Estacas e Blocos Baldrame)"])

with aba_vigas:
    vigas_ativas = data_store.vigas_ativas(dados)
    if not vigas_ativas:
        st.info("Nenhum .LST processado ainda — envie os arquivos na página **Inputs Gerais**.")
    else:
        df, totais = concreto_tela_pop.calcular(dados)
        col1, col2 = st.columns(2)
        col1.metric("Volume/custo", totais["resumo"])
        col2.metric("Custo total", moeda(totais["custo_total"]))
        st.dataframe(df, use_container_width=True)

        if any(v.get("secao_variavel") for v in vigas_ativas):
            st.warning(
                "Algumas vigas têm seção variável ao longo do comprimento — o "
                "cálculo usou a menor seção encontrada. Revise manualmente."
            )

        df_pilares = data_store.pilares_ativas(dados)
        if df_pilares:
            st.subheader("Pilares — quantitativos extraídos do TQS (área/volume)")
            st.dataframe(df_pilares, use_container_width=True)
            st.caption(
                "Os .LST de Formas não trazem largura x profundidade por pilar — "
                "apenas área e volume já calculados pelo TQS. Para entrar no custo "
                "por Fck, informe as dimensões manualmente (mesma limitação da "
                "planilha original)."
            )

with aba_fundacao:
    st.markdown("**Estacas**")
    estacas = editar_tabela(
        dados["fundacao"]["estacas"], key="estacas_editor",
        column_config={"fck_mpa": st.column_config.NumberColumn("Fck (MPa)")},
    )
    st.markdown("**Blocos e Vigas Baldrame**")
    blocos = editar_tabela(dados["fundacao"]["blocos_baldrame"], key="blocos_baldrame_editor")

    if estacas != dados["fundacao"]["estacas"] or blocos != dados["fundacao"]["blocos_baldrame"]:
        dados["fundacao"]["estacas"] = estacas
        dados["fundacao"]["blocos_baldrame"] = blocos
        data_store.salvar(dados)

    df_f, totais_f = fundacao.calcular(dados)
    col1, col2 = st.columns(2)
    col1.metric("Volume", totais_f["resumo"])
    col2.metric("Custo total", moeda(totais_f["custo_total"]))
    st.dataframe(df_f, use_container_width=True)
