"""
Acesso ao catálogo de preços (equivalente à aba "BANCO DE DADOS" da
planilha). Todo módulo de cálculo busca preço por aqui — nunca com valor
fixo no código — para que uma edição no catálogo (feita na página de
Inputs) se reflita automaticamente em todas as abas que usam aquele
material, e no Resumo Geral.
"""

from typing import Optional


def preco(dados: dict, material: str, segmento: Optional[str] = None, default: float = 0.0) -> float:
    """Busca o valor unitário de `material` no catálogo (equivalente ao PROCV manual da planilha).

    Se `segmento` for informado, restringe a busca a ele (útil quando dois
    segmentos têm materiais de mesmo nome). Retorna `default` se não achar.
    """
    for item in dados.get("catalogo", []):
        if item["material"] == material and (segmento is None or item["segmento"] == segmento):
            return float(item["valor"])
    return default


def preco_concreto_m3(dados: dict, fck_mpa: float) -> float:
    """Busca o preço do concreto pelo Fck mais próximo cadastrado no catálogo."""
    candidatos = {
        item["material"]: item["valor"]
        for item in dados.get("catalogo", [])
        if item["segmento"] == "CONCRETO"
    }
    if not candidatos:
        return 0.0
    fcks = {float(nome.split("FCK")[1].split("MPA")[0].strip()): valor for nome, valor in candidatos.items()}
    fck_mais_proximo = min(fcks, key=lambda k: abs(k - fck_mpa))
    return float(fcks[fck_mais_proximo])


def segmentos(dados: dict) -> list:
    vistos = []
    for item in dados.get("catalogo", []):
        if item["segmento"] not in vistos:
            vistos.append(item["segmento"])
    return vistos
