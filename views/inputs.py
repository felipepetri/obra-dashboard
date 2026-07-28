"""
Página de Inputs — tudo que alimenta as demais abas de orçamento:
arquivos .LST (vigas/pilares do TQS), catálogo de preços de materiais e
parâmetros gerais da obra. Qualquer edição aqui é salva no data_store e
passa a valer automaticamente em toda página que lê aquele dado.
"""

import streamlit as st

import data_store
from parser_tqs import _ler_texto, _nome_pavimento, extrair_pilares, extrair_vigas, vigas_para_dimensoes
from utils import editar_tabela

st.title("📥 Inputs Gerais")
st.caption(
    "Envie os .LST, ajuste o catálogo de preços e os parâmetros da obra aqui — "
    "todas as abas de orçamento e o Resumo Geral usam estes valores automaticamente."
)

dados = data_store.carregar()

# ---------------------------------------------------------------------
# 1) Arquivos .LST (TQS Formas) — vigas e pilares
# ---------------------------------------------------------------------
st.subheader("1. Arquivos .LST do TQS (Vigas e Pilares)")

arquivos = st.file_uploader(
    "Arquivos .LST do projeto", type=["lst", "LST"], accept_multiple_files=True, key="lst_uploader"
)

if arquivos and st.button("Processar arquivos .LST"):
    fontes = dados.setdefault("fontes_estruturais", [])
    for arquivo in arquivos:
        texto = _ler_texto(arquivo.read())
        pavimento = _nome_pavimento(arquivo.name)
        dimensoes = vigas_para_dimensoes(extrair_vigas(texto, pavimento))
        pilares = extrair_pilares(texto, pavimento)

        nova_fonte = {
            "arquivo": arquivo.name,
            "pavimento": pavimento,
            "ativo": True,
            "vigas": list(dimensoes.values()),
            "pilares": [p.__dict__ for p in pilares],
        }
        # Se já existe uma fonte com o mesmo nome de arquivo, substitui em vez de duplicar.
        fontes[:] = [f for f in fontes if f["arquivo"] != arquivo.name]
        fontes.append(nova_fonte)

    data_store.salvar(dados)
    st.success(f"{len(arquivos)} arquivo(s) processado(s) e adicionado(s) ao projeto.")
    st.rerun()

fontes = dados.get("fontes_estruturais", [])
if fontes:
    st.markdown("**Arquivos carregados no projeto:**")
    for i, fonte in enumerate(fontes):
        col_check, col_info, col_remover = st.columns([1, 4, 1])
        ativo = col_check.checkbox(
            "Incluir", value=fonte.get("ativo", True), key=f"fonte_ativa_{i}"
        )
        if ativo != fonte.get("ativo", True):
            fonte["ativo"] = ativo
            data_store.salvar(dados)
        col_info.write(
            f"**{fonte['arquivo']}** — pavimento {fonte['pavimento']} "
            f"({len(fonte['vigas'])} vigas, {len(fonte['pilares'])} pilares)"
        )
        if col_remover.button("🗑️ Remover", key=f"fonte_remover_{i}"):
            fontes.pop(i)
            data_store.salvar(dados)
            st.rerun()
else:
    st.info("Nenhum arquivo .LST carregado ainda.")

st.divider()

# ---------------------------------------------------------------------
# 2) Catálogo de preços (BANCO DE DADOS)
# ---------------------------------------------------------------------
st.subheader("2. Catálogo de Preços de Materiais (Banco de Dados)")
st.caption(
    "Mudar um preço aqui atualiza automaticamente todas as abas que usam esse "
    "material (ex.: mudar o preço do concreto reflete em Fundação, Vigas e "
    "Pilares, Alvenaria — mudar o preço de um misturador reflete em Acabamentos)."
)

catalogo_editado = editar_tabela(
    dados.get("catalogo", []),
    key="catalogo_editor",
    column_config={
        "valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f"),
    },
)
if catalogo_editado != dados.get("catalogo", []):
    dados["catalogo"] = catalogo_editado
    data_store.salvar(dados)

st.divider()

# ---------------------------------------------------------------------
# 3) Parâmetros gerais da obra
# ---------------------------------------------------------------------
st.subheader("3. Parâmetros Gerais da Obra")

p = dados.setdefault("parametros_gerais", {})
col1, col2, col3 = st.columns(3)
with col1:
    p["fck_padrao_mpa"] = st.selectbox(
        "Fck padrão do concreto (MPa)", [25, 30, 35],
        index=[25, 30, 35].index(p.get("fck_padrao_mpa", 25)),
    )
    p["perda_padrao"] = st.number_input("Perda padrão de concreto (%)", value=p.get("perda_padrao", 0.10) * 100, step=1.0) / 100
    p["preco_aco_kg"] = st.number_input("Preço do aço (R$/kg)", value=p.get("preco_aco_kg", 8.5), step=0.1)
with col2:
    p["taxa_aco_viga_kg_m3"] = st.number_input("Taxa de aço em vigas (kg/m³)", value=p.get("taxa_aco_viga_kg_m3", 100.0), step=1.0)
    p["taxa_aco_pilar_kg_m3"] = st.number_input("Taxa de aço em pilares (kg/m³)", value=p.get("taxa_aco_pilar_kg_m3", 90.0), step=1.0)
    p["altura_muro_divisa_m"] = st.number_input("Altura padrão do muro de divisa (m)", value=p.get("altura_muro_divisa_m", 2.0), step=0.1)
with col3:
    p["preco_m2_gesso"] = st.number_input("Preço/m² gesso liso (R$)", value=p.get("preco_m2_gesso", 45.0), step=1.0)
    p["preco_m2_forro"] = st.number_input("Preço/m² forro (R$)", value=p.get("preco_m2_forro", 60.0), step=1.0)
    p["preco_m2_piso"] = st.number_input("Preço/m² revestimento de piso (R$)", value=p.get("preco_m2_piso", 80.0), step=1.0)
    p["preco_m2_parede_revest"] = st.number_input("Preço/m² revestimento de parede (R$)", value=p.get("preco_m2_parede_revest", 55.0), step=1.0)

dados["parametros_gerais"] = p
data_store.salvar(dados)
