"""
Dashboard de planejamento de obra — ponto de entrada.

Executar com:
    streamlit run app.py

Só monta a navegação (menu à esquerda, agrupado por seção); cada página
mora em `views/` e lê/grava estado através de `data_store.py`, que é a
fonte única da verdade compartilhada entre todas elas.
"""

import streamlit as st

st.set_page_config(page_title="Planejamento de Obra", layout="wide", page_icon="🏗️")

pg = st.navigation(
    {
        "Inputs": [
            st.Page("views/inputs.py", title="Inputs Gerais", icon="📥", default=True),
        ],
        "Orçamentos": [
            st.Page("views/concreto_tela_pop.py", title="Concreto e Tela Pop", icon="🏗️"),
            st.Page("views/formas.py", title="Formas", icon="🪵"),
            st.Page("views/alvenaria.py", title="Alvenaria e Embasamento", icon="🧱"),
            st.Page("views/gesso.py", title="Gesso Liso", icon="🎨"),
            st.Page("views/forro.py", title="Forro", icon="🏠"),
            st.Page("views/metragens.py", title="Metragens dos Ambientes", icon="📐"),
            st.Page("views/acabamentos.py", title="Acabamentos (Louças e Metais)", icon="🚿"),
            st.Page("views/telhado.py", title="Telhado", icon="🏘️"),
        ],
        "Resumo": [
            st.Page("views/resumo_geral.py", title="Resumo Geral da Obra", icon="📊"),
        ],
    }
)
pg.run()
