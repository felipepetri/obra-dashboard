"""
Cálculos de quantitativos de obra — tradução das fórmulas da planilha
"Planilha_Planejamento_de_Obras.xlsx" (abas CONCRETO E TELA POP / BANCO DE DADOS)
para Python puro.

Os preços (concreto por Fck, aço) e a taxa de armadura vêm do catálogo/
parâmetros gerais (`catalog.py` / `data_store.py`), nunca de constantes
fixas aqui — assim uma edição na página de Inputs se reflete em todo
cálculo que passa por este módulo.
"""

from typing import Iterable, List

import catalog
from models import Pilar, ResumoOrcamento, Viga


def custo_concreto_m3(dados: dict, fck: float) -> float:
    return catalog.preco_concreto_m3(dados, fck)


def calcular_viga(viga: Viga, dados: dict) -> dict:
    parametros = dados.get("parametros_gerais", {})
    custo_m3 = custo_concreto_m3(dados, viga.fck)
    volume = viga.volume_m3
    volume_perda = viga.volume_com_perda_m3
    taxa_aco = parametros.get("taxa_aco_viga_kg_m3", 100.0)
    preco_aco = parametros.get("preco_aco_kg", 8.5)
    peso_aco = volume * taxa_aco
    return {
        "pavimento": viga.pavimento,
        "elemento": viga.nomenclatura,
        "largura_m": viga.largura,
        "comprimento_m": viga.comprimento,
        "altura_m": viga.profundidade,
        "fck_mpa": viga.fck,
        "volume_m3": round(volume, 4),
        "volume_com_perda_m3": round(volume_perda, 4),
        "custo_concreto_m3": custo_m3,
        "custo_concreto_total": round(volume_perda * custo_m3, 2),
        "peso_aco_estimado_kg": round(peso_aco, 1),
        "custo_aco_estimado": round(peso_aco * preco_aco, 2),
    }


def calcular_pilar(pilar: Pilar, dados: dict) -> dict:
    parametros = dados.get("parametros_gerais", {})
    custo_m3 = custo_concreto_m3(dados, pilar.fck)
    volume = pilar.volume_m3
    volume_perda = pilar.volume_com_perda_m3
    taxa_aco = parametros.get("taxa_aco_pilar_kg_m3", 90.0)
    preco_aco = parametros.get("preco_aco_kg", 8.5)
    peso_aco = volume * taxa_aco
    return {
        "pavimento": pilar.pavimento,
        "elemento": pilar.nomenclatura,
        "altura_m": pilar.altura,
        "largura_m": pilar.largura,
        "profundidade_m": pilar.profundidade,
        "fck_mpa": pilar.fck,
        "volume_m3": round(volume, 4),
        "volume_com_perda_m3": round(volume_perda, 4),
        "custo_concreto_m3": custo_m3,
        "custo_concreto_total": round(volume_perda * custo_m3, 2),
        "peso_aco_estimado_kg": round(peso_aco, 1),
        "custo_aco_estimado": round(peso_aco * preco_aco, 2),
    }


def resumir(vigas: Iterable[Viga], pilares: Iterable[Pilar], dados: dict) -> ResumoOrcamento:
    itens = [calcular_viga(v, dados) for v in vigas] + [calcular_pilar(p, dados) for p in pilares]
    resumo = ResumoOrcamento(itens=itens)
    for item in itens:
        resumo.volume_concreto_m3 += item["volume_com_perda_m3"]
        resumo.custo_concreto += item["custo_concreto_total"]
        resumo.peso_aco_kg += item["peso_aco_estimado_kg"]
        resumo.custo_aco += item["custo_aco_estimado"]
    resumo.volume_concreto_m3 = round(resumo.volume_concreto_m3, 3)
    resumo.custo_concreto = round(resumo.custo_concreto, 2)
    resumo.peso_aco_kg = round(resumo.peso_aco_kg, 1)
    resumo.custo_aco = round(resumo.custo_aco, 2)
    return resumo


def vigas_a_partir_do_parser(dimensoes_agrupadas: dict, fck: float = 25.0) -> List[Viga]:
    """
    Converte a saída de parser_tqs.vigas_para_dimensoes() em objetos Viga,
    prontos para calcular_viga()/resumir().
    """
    vigas = []
    for dados in dimensoes_agrupadas.values():
        vigas.append(
            Viga(
                nomenclatura=dados["viga"],
                largura=dados["largura_m"],
                comprimento=dados["comprimento_total_m"],
                profundidade=dados["altura_m"],
                fck=fck,
                pavimento=dados["pavimento"],
            )
        )
    return vigas
