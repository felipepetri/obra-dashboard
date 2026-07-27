"""Pequenos helpers compartilhados pelas páginas do dashboard."""

from typing import Optional

import pandas as pd
import streamlit as st


def moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}"


def editar_tabela(registros: list, key: str, column_config: Optional[dict] = None) -> list:
    """Mostra `registros` (lista de dicts) num st.data_editor editável e
    devolve a lista já limpa (sem linhas em branco) para salvar de volta no
    data_store. Uso padrão em toda página que edita uma tabela de inputs."""
    df = pd.DataFrame(registros)
    editado = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key=key,
        column_config=column_config,
    )
    editado = editado.dropna(how="all")
    for col in editado.columns:
        if pd.api.types.is_numeric_dtype(editado[col]):
            editado[col] = editado[col].fillna(0)
        else:
            editado[col] = editado[col].fillna("")
    return editado.to_dict("records")
