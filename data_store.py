"""
Camada única de persistência do dashboard — lê e grava um JSON local
(`dados_obra.json`) que serve de fonte da verdade para todas as páginas.

Cada página do Streamlit chama `carregar()` no início da execução e
`salvar(dados)` a cada edição do usuário. Como o Streamlit reroda o script
inteiro a cada navegação/interação, isso garante que qualquer página sempre
lê o estado mais recente gravado por outra — é assim que uma mudança de
preço ou quantidade feita em "Inputs" aparece automaticamente em todas as
abas de orçamento e no Resumo Geral, sem precisar copiar/colar nada.

Os valores semente abaixo foram extraídos da planilha real do usuário
("Planilha Planejamento de Obras.xlsx"), não são dados fictícios — apenas
reorganizados no formato que o app usa. Onde a planilha não tinha um preço
lançado (ex.: preço por m² de gesso/forro/revestimento), foi assumida uma
estimativa editável, sinalizada no comentário.
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "dados_obra.json"


def _seed() -> dict:
    return {
        "parametros_gerais": {
            "perda_padrao": 0.10,
            "fck_padrao_mpa": 25,
            "taxa_aco_viga_kg_m3": 100.0,
            "taxa_aco_pilar_kg_m3": 90.0,
            "preco_aco_kg": 8.50,
            "largura_bloco_concreto_m": 0.4,
            "altura_bloco_concreto_m": 0.2,
            "altura_muro_divisa_m": 2.0,
            # Estimativas — a planilha original não tem uma célula única de
            # preço/m² para estes itens (o custo vem de vários materiais
            # somados). Ajuste livremente na página de Inputs.
            "preco_m2_gesso": 45.0,
            "preco_m2_forro": 60.0,
            "preco_m2_piso": 80.0,
            "preco_m2_parede_revest": 55.0,
            "largura_media_viga_m": 0.20,
            "altura_media_viga_m": 0.45,
        },
        "catalogo": [
            {"segmento": "BÁSICOS", "material": "AREIA MÉDIA", "unidade": "M3", "valor": 204.0},
            {"segmento": "BÁSICOS", "material": "AREIA FINA", "unidade": "M3", "valor": 219.0},
            {"segmento": "BÁSICOS", "material": "PEDRISCO", "unidade": "M3", "valor": 175.0},
            {"segmento": "BÁSICOS", "material": "CIMENTO", "unidade": "UN", "valor": 34.14},
            {"segmento": "BÁSICOS", "material": "ARGAMASSA C3 CINZA 25KG", "unidade": "UN", "valor": 35.0},
            {"segmento": "CONCRETO", "material": "CONCRETO FCK 25 MPA", "unidade": "M3", "valor": 440.0},
            {"segmento": "CONCRETO", "material": "CONCRETO FCK 30 MPA", "unidade": "M3", "valor": 470.0},
            {"segmento": "CONCRETO", "material": "CONCRETO FCK 35 MPA", "unidade": "M3", "valor": 480.0},
            {"segmento": "BLOCOS", "material": "CERAMICO CABEÇA 14X19X14", "unidade": "UN", "valor": 5.3},
            {"segmento": "BLOCOS", "material": "CERAMICO 14X19X39", "unidade": "UN", "valor": 2.73},
            {"segmento": "BLOCOS", "material": "CERAMICO CABEÇA 19X19X19", "unidade": "UN", "valor": 3.16},
            {"segmento": "BLOCOS", "material": "CONCRETO 14X19X14", "unidade": "UN", "valor": 2.62},
            {"segmento": "BLOCOS", "material": "CONCRETO 14X19X39", "unidade": "UN", "valor": 4.17},
            {"segmento": "BLOCOS", "material": "CONCRETO 19X19X19", "unidade": "UN", "valor": 3.16},
            {"segmento": "BLOCOS", "material": "CONCRETO 19X19X39", "unidade": "UN", "valor": 5.4},
            {"segmento": "BLOCOS", "material": "CONCRETO CANALETA 14X19X39", "unidade": "UN", "valor": 4.5},
            {"segmento": "BLOCOS", "material": "CONCRETO CANALETA 19X19X39", "unidade": "UN", "valor": 5.73},
            {"segmento": "MADEIRAS", "material": "MADEIRITE PLASTIFICADA 1,10 X 2,2", "unidade": "UN", "valor": 116.4},
            {"segmento": "MADEIRAS", "material": "SARRAFOS 3M X 7 CM", "unidade": "UN", "valor": 13.11},
            {"segmento": "MADEIRAS", "material": "TÁBUAS PINUS 3 M X 0,30 M", "unidade": "UN", "valor": 33.44},
            {"segmento": "MADEIRAS", "material": "TÁBUAS MISTAS 3 M X 0,30 M", "unidade": "UN", "valor": 56.31},
            {"segmento": "DIVERSOS", "material": "BROCHA", "unidade": "UN", "valor": 11.9},
            {"segmento": "DIVERSOS", "material": "CAIXA DAGUA 2000 L", "unidade": "UN", "valor": 1800.0},
            {"segmento": "DIVERSOS", "material": "PREGOS 18X27", "unidade": "KG", "valor": 15.0},
            {"segmento": "DIVERSOS", "material": "PREGOS 17X21", "unidade": "KG", "valor": 15.0},
            {"segmento": "DIVERSOS", "material": "ARAME 18", "unidade": "KG", "valor": 12.38},
            {"segmento": "DIVERSOS", "material": "ARAME 12", "unidade": "KG", "valor": 12.38},
            {"segmento": "DIVERSOS", "material": "ESPAÇADORES", "unidade": "UNIDADES", "valor": 0.8},
            {"segmento": "QUÍMICOS", "material": "VIAPLUS1000", "unidade": "UN", "valor": 55.6},
            {"segmento": "QUÍMICOS", "material": "VIAPLUS7000", "unidade": "UN", "valor": 221.0},
            {"segmento": "QUÍMICOS", "material": "ADITIVO CRISTALIZANTE", "unidade": "UN", "valor": 130.0},
            {"segmento": "QUÍMICOS", "material": "NEUTROL VEDACIT", "unidade": "UN", "valor": 273.0},
            {"segmento": "QUÍMICOS", "material": "LIGMASSA GALÃO 5 L", "unidade": "UN", "valor": 44.5},
            {"segmento": "QUÍMICOS", "material": "SAQUINHO MACTRACOL", "unidade": "UN", "valor": 28.9},
            {"segmento": "AÇOS", "material": "VERGALHÃO 10MM 12 METROS", "unidade": "UN", "valor": 41.87},
            {"segmento": "AÇOS", "material": "TELA POP - 4.2 3 X 2", "unidade": "UN", "valor": 72.9},
            {"segmento": "EQUIPAMENTOS", "material": "VIBRADOR 1,5 3CM 10A", "unidade": "DIARIA", "valor": 165.0},
            {"segmento": "EQUIPAMENTOS", "material": "COMPACTADOR SAPO", "unidade": "DIARIA", "valor": 272.0},
            {"segmento": "EQUIPAMENTOS", "material": "ESCORA METÁLICA", "unidade": "MENSAL / PÇ", "valor": 16.0},
            {"segmento": "EQUIPAMENTOS", "material": "ANDAIME", "unidade": "MENSAL / PÇ", "valor": 9.0},
            {"segmento": "ACABAMENTOS", "material": "Cuba apoio", "unidade": "UN", "valor": 750.0},
            {"segmento": "ACABAMENTOS", "material": "Cuba slim", "unidade": "UN", "valor": 750.0},
            {"segmento": "ACABAMENTOS", "material": "Tanque", "unidade": "UN", "valor": 650.0},
            {"segmento": "ACABAMENTOS", "material": "Cuba inox", "unidade": "UN", "valor": 500.0},
            {"segmento": "ACABAMENTOS", "material": "Cuba inox pequena", "unidade": "UN", "valor": 450.0},
            {"segmento": "ACABAMENTOS", "material": "Chuveiro Acqua Plus", "unidade": "UN", "valor": 780.0},
            {"segmento": "ACABAMENTOS", "material": "Misturador Monocomando", "unidade": "UN", "valor": 650.0},
            {"segmento": "ACABAMENTOS", "material": "Torneira Simples", "unidade": "UN", "valor": 220.0},
            {"segmento": "ACABAMENTOS", "material": "Misturador Gourmet", "unidade": "UN", "valor": 900.0},
            {"segmento": "TELHADO", "material": "Telha fibrocimento", "unidade": "un", "valor": 95.0},
            {"segmento": "TELHADO", "material": "Cumeeira", "unidade": "un", "valor": 60.0},
            {"segmento": "TELHADO", "material": "Parafusos/vedação", "unidade": "un", "valor": 1.2},
            {"segmento": "TELHADO", "material": "Rufos", "unidade": "m", "valor": 90.0},
            {"segmento": "TELHADO", "material": "Calhas", "unidade": "m", "valor": 120.0},
            {"segmento": "TELHADO", "material": "Condutores", "unidade": "m", "valor": 50.0},
            {"segmento": "TELHADO", "material": "Caibros 5x6", "unidade": "m", "valor": 8.0},
            {"segmento": "TELHADO", "material": "Terças 5x10", "unidade": "m", "valor": 18.0},
            {"segmento": "TELHADO", "material": "Vigas 6x12/16", "unidade": "m", "valor": 35.0},
            {"segmento": "TELHADO", "material": "Fixações diversas", "unidade": "vb", "valor": 1200.0},
            {"segmento": "TELHADO", "material": "Cantoneiras/chapas", "unidade": "vb", "valor": 800.0},
        ],
        "fontes_estruturais": [],
        "fundacao": {
            "estacas": [
                {"tipo": "FIXO Ø0,50m", "qtd": 11, "profundidade_m": 8.4, "diametro_m": 0.5, "fck_mpa": 25},
                {"tipo": "Ø0,40m", "qtd": 9, "profundidade_m": 8.4, "diametro_m": 0.4, "fck_mpa": 25},
                {"tipo": "Ø0,30m (A)", "qtd": 8, "profundidade_m": 8.4, "diametro_m": 0.3, "fck_mpa": 25},
                {"tipo": "Ø0,30m (B)", "qtd": 17, "profundidade_m": 4.4, "diametro_m": 0.3, "fck_mpa": 25},
                {"tipo": "Ø0,30m (C)", "qtd": 8, "profundidade_m": 7.0, "diametro_m": 0.3, "fck_mpa": 25},
            ],
            "blocos_baldrame": [
                {"nomenclatura": "BLOCOS SIMPLES 0,60X0,60X0,60", "comprimento_m": 0.6, "largura_m": 0.6, "altura_m": 0.6, "fck_mpa": 35, "quantidade": 6},
                {"nomenclatura": "BLOCOS SIMPLES 0,6X0,6X0,5", "comprimento_m": 0.6, "largura_m": 0.6, "altura_m": 0.5, "fck_mpa": 25, "quantidade": 8},
                {"nomenclatura": "BLOCOS SIMPLES 0,80X0,80X0,60", "comprimento_m": 0.8, "largura_m": 0.8, "altura_m": 0.6, "fck_mpa": 25, "quantidade": 4},
                {"nomenclatura": "BLOCOS SIMPLES 0,7X0,7X0,6", "comprimento_m": 0.7, "largura_m": 0.7, "altura_m": 0.6, "fck_mpa": 25, "quantidade": 1},
                {"nomenclatura": "BLOCOS DUPLOS 1,5X0,6X0,6", "comprimento_m": 1.5, "largura_m": 0.6, "altura_m": 0.6, "fck_mpa": 25, "quantidade": 1},
                {"nomenclatura": "BLOCOS DUPLOS 1,9X0,7X0,60", "comprimento_m": 1.9, "largura_m": 0.7, "altura_m": 0.6, "fck_mpa": 25, "quantidade": 4},
                {"nomenclatura": "BLOCOS DUPLOS 2,3X0,8X0,7", "comprimento_m": 2.3, "largura_m": 0.8, "altura_m": 0.7, "fck_mpa": 25, "quantidade": 2},
                {"nomenclatura": "BLOCOS TRIPLOS", "comprimento_m": 2.267, "largura_m": 1.0, "altura_m": 0.7, "fck_mpa": 25, "quantidade": 1},
            ],
        },
        "alvenaria": {
            "paredes": [
                *[{"pavimento": "EMBASAMENTO", "identificacao": nome, "comprimento_m": c, "altura_m": a, "bloco": "CONCRETO 14X19X39"}
                  for nome, c, a in [
                      ("MURO - MINI 1", 4.0, 0.4), ("MURO - MINI 2", 4.0, 0.4),
                      ("MURO - M1", 4.49, 0.8), ("MURO - M2", 9.32, 0.8),
                      ("MURO - M3", 21.01, 0.8), ("MURO - M4", 10.0, 0.8),
                      ("EMB. GARAGEM 01", 3.62, 0.2), ("EMB. GARAGEM 02", 2.28, 0.2),
                      ("EMB. GARAGEM 03", 1.7, 0.2), ("EMB. GARAGEM 04", 2.22, 0.2),
                      ("PAR01", 6.35, 0.8), ("PAR02", 1.63, 0.8), ("PAR03", 1.63, 0.8),
                      ("PAR04", 3.13, 0.8), ("PAR05", 3.13, 0.8), ("PAR06", 3.77, 0.8),
                      ("PAR07", 4.01, 0.8), ("PAR08", 7.19, 0.8), ("PAR09", 4.16, 0.8),
                      ("PAR10", 4.51, 0.8), ("PAR11", 12.26, 0.8),
                  ]],
                *[{"pavimento": "TÉRREO", "identificacao": nome, "comprimento_m": c, "altura_m": a, "bloco": "CERAMICO 14X19X39"}
                  for nome, c, a in [
                      ("M1", 4.49, 1.4), ("M2", 9.32, 1.4), ("M3", 21.01, 1.4), ("M4", 10.0, 1.4),
                      ("PAR01", 6.35, 2.4), ("PAR02", 1.63, 2.4), ("PAR03", 1.63, 2.4),
                      ("PAR04", 3.13, 2.4), ("PAR05", 3.13, 2.4), ("PAR06", 3.77, 2.4),
                      ("PAR07", 4.01, 2.4), ("PAR08", 7.19, 2.4), ("PAR09", 4.16, 2.4),
                      ("PAR10", 4.51, 2.4), ("PAR11", 12.26, 2.4),
                  ]],
                *[{"pavimento": "SUPERIOR", "identificacao": nome, "comprimento_m": c, "altura_m": 3.0, "bloco": "CERAMICO 14X19X39"}
                  for nome, c in [
                      ("PAR01", 6.35), ("PAR02", 7.86), ("PAR03", 2.55), ("PAR04", 3.52),
                      ("PAR05", 3.27), ("PAR06", 3.11), ("PAR07", 4.09), ("PAR08", 8.11),
                      ("PAR09", 4.16), ("PAR10", 1.54), ("PAR11", 3.65), ("PAR12", 0.91),
                      ("PAR13", 2.34), ("PAR14", 4.16), ("PAR15", 12.27),
                  ]],
                *[{"pavimento": "PISCINA", "identificacao": nome, "comprimento_m": c, "altura_m": 1.4, "bloco": "CONCRETO 19X19X19"}
                  for nome, c in [("PISC01", 5.0), ("PISC02", 5.0), ("PISC03", 2.4), ("PISC04", 2.4)]],
            ],
        },
        "gesso": {
            "paredes": [
                *[{"pavimento": "TÉRREO", "identificacao": nome, "comprimento_m": c, "pe_direito_m": 3.0}
                  for nome, c in [
                      ("PAR01", 6.35), ("PAR02", 1.63), ("PAR03", 1.63), ("PAR04", 3.13),
                      ("PAR05", 3.13), ("PAR06", 3.77), ("PAR07", 4.01), ("PAR08", 7.19),
                      ("PAR09", 4.16), ("PAR10", 4.51), ("PAR11", 12.26),
                  ]],
                *[{"pavimento": "SUPERIOR", "identificacao": nome, "comprimento_m": c, "pe_direito_m": 3.0}
                  for nome, c in [
                      ("PAR01", 6.35), ("PAR02", 7.86), ("PAR03", 2.55), ("PAR04", 3.52),
                      ("PAR05", 3.27), ("PAR06", 3.11), ("PAR07", 4.09), ("PAR08", 8.11),
                      ("PAR09", 4.16), ("PAR10", 1.54), ("PAR11", 3.65), ("PAR12", 0.91),
                      ("PAR13", 2.34), ("PAR14", 4.16), ("PAR15", 12.27),
                  ]],
            ],
        },
        "forro": {
            "ambientes": [
                {"pavimento": "TÉRREO", "nome": "GARAGEM", "area_m2": 23.13},
                {"pavimento": "TÉRREO", "nome": "SALA DE ESTAR", "area_m2": 11.18},
                {"pavimento": "TÉRREO", "nome": "SALA DE JANTAR", "area_m2": 18.52},
                {"pavimento": "TÉRREO", "nome": "COZINHA", "area_m2": 17.19},
                {"pavimento": "TÉRREO", "nome": "DESPENSA", "area_m2": 4.14},
                {"pavimento": "TÉRREO", "nome": "LAVANDERIA", "area_m2": 5.74},
                {"pavimento": "TÉRREO", "nome": "DEPÓSITO", "area_m2": 3.04},
                {"pavimento": "TÉRREO", "nome": "ÁREA GOURMET", "area_m2": 12.95},
                {"pavimento": "TÉRREO", "nome": "BANHEIRO 01", "area_m2": 3.19},
                {"pavimento": "SUPERIOR", "nome": "VARANDA", "area_m2": 2.93},
                {"pavimento": "SUPERIOR", "nome": "DORMITÓRIO 02", "area_m2": 8.71},
                {"pavimento": "SUPERIOR", "nome": "HOME OFFICE CIRCULAÇÃO", "area_m2": 13.99},
                {"pavimento": "SUPERIOR", "nome": "CLOSET", "area_m2": 7.18},
                {"pavimento": "SUPERIOR", "nome": "BANHEIRO 02", "area_m2": 3.35},
                {"pavimento": "SUPERIOR", "nome": "SUITE MASTER", "area_m2": 13.5},
                {"pavimento": "SUPERIOR", "nome": "BANHEIRO 03", "area_m2": 9.44},
            ],
        },
        "metragens": {
            "piso": [
                {"pavimento": "TÉRREO", "nome": "GARAGEM", "area_m2": 23.13},
                {"pavimento": "TÉRREO", "nome": "SALA DE ESTAR", "area_m2": 11.18},
                {"pavimento": "TÉRREO", "nome": "SALA DE JANTAR", "area_m2": 18.52},
                {"pavimento": "TÉRREO", "nome": "COZINHA", "area_m2": 17.19},
                {"pavimento": "TÉRREO", "nome": "DESPENSA", "area_m2": 4.14},
                {"pavimento": "TÉRREO", "nome": "LAVANDERIA", "area_m2": 5.74},
                {"pavimento": "TÉRREO", "nome": "DEPÓSITO", "area_m2": 3.04},
                {"pavimento": "TÉRREO", "nome": "ÁREA GOURMET", "area_m2": 12.95},
                {"pavimento": "TÉRREO", "nome": "BANHEIRO 01", "area_m2": 3.19},
                {"pavimento": "TÉRREO", "nome": "ÁREA EXTERNA", "area_m2": 38.17},
                {"pavimento": "SUPERIOR", "nome": "VARANDA", "area_m2": 2.93},
                {"pavimento": "SUPERIOR", "nome": "DORMITÓRIO 02", "area_m2": 8.71},
                {"pavimento": "SUPERIOR", "nome": "HOME OFFICE CIRCULAÇÃO", "area_m2": 13.99},
                {"pavimento": "SUPERIOR", "nome": "CLOSET", "area_m2": 7.18},
                {"pavimento": "SUPERIOR", "nome": "BANHEIRO 02", "area_m2": 3.35},
                {"pavimento": "SUPERIOR", "nome": "SUITE MASTER", "area_m2": 13.5},
                {"pavimento": "SUPERIOR", "nome": "BANHEIRO 03", "area_m2": 9.44},
            ],
            "parede": [],
        },
        "acabamentos": {
            "itens": [
                {"ambiente": "WC", "item": "Cuba", "material": "Cuba apoio", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC SUITE 1", "item": "Cuba", "material": "Cuba apoio", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC SUITE 2", "item": "Cuba", "material": "Cuba apoio", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC SUITE MASTER", "item": "Cuba", "material": "Cuba apoio", "marca": "Deca", "qtd": 2},
                {"ambiente": "Lavabo", "item": "Cuba", "material": "Cuba slim", "marca": "Deca", "qtd": 1},
                {"ambiente": "Lavanderia", "item": "Tanque", "material": "Tanque", "marca": "Deca", "qtd": 1},
                {"ambiente": "Cozinha", "item": "Pia", "material": "Cuba inox", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC Estar", "item": "Cuba", "material": "Cuba apoio", "marca": "Deca", "qtd": 1},
                {"ambiente": "Área Gourmet", "item": "Cuba", "material": "Cuba inox", "marca": "Deca", "qtd": 1},
                {"ambiente": "Bar", "item": "Cuba", "material": "Cuba inox pequena", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC", "item": "Chuveiro", "material": "Chuveiro Acqua Plus", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC SUITE 1", "item": "Chuveiro", "material": "Chuveiro Acqua Plus", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC SUITE 2", "item": "Chuveiro", "material": "Chuveiro Acqua Plus", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC SUITE MASTER", "item": "Chuveiro", "material": "Chuveiro Acqua Plus", "marca": "Deca", "qtd": 2},
                {"ambiente": "WC Estar", "item": "Chuveiro", "material": "Chuveiro Acqua Plus", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC", "item": "Misturador", "material": "Misturador Monocomando", "marca": "Deca", "qtd": 2},
                {"ambiente": "WC SUITE 1", "item": "Misturador", "material": "Misturador Monocomando", "marca": "Deca", "qtd": 2},
                {"ambiente": "WC SUITE 2", "item": "Misturador", "material": "Misturador Monocomando", "marca": "Deca", "qtd": 2},
                {"ambiente": "WC SUITE MASTER", "item": "Misturador", "material": "Misturador Monocomando", "marca": "Deca", "qtd": 4},
                {"ambiente": "Lavabo", "item": "Misturador", "material": "Misturador Monocomando", "marca": "Deca", "qtd": 1},
                {"ambiente": "Lavanderia", "item": "Torneira", "material": "Torneira Simples", "marca": "Deca", "qtd": 1},
                {"ambiente": "Cozinha", "item": "Misturador", "material": "Misturador Gourmet", "marca": "Deca", "qtd": 1},
                {"ambiente": "WC Estar", "item": "Misturador", "material": "Misturador Monocomando", "marca": "Deca", "qtd": 2},
            ],
        },
        "telhado": {
            "itens": [
                {"categoria": "Telhas", "material": "Telha fibrocimento", "unidade": "un", "quantidade": 200},
                {"categoria": "Telhas", "material": "Cumeeira", "unidade": "un", "quantidade": 40},
                {"categoria": "Telhas", "material": "Parafusos/vedação", "unidade": "un", "quantidade": 1100},
                {"categoria": "Drenagem", "material": "Rufos", "unidade": "m", "quantidade": 80},
                {"categoria": "Drenagem", "material": "Calhas", "unidade": "m", "quantidade": 50},
                {"categoria": "Drenagem", "material": "Condutores", "unidade": "m", "quantidade": 24},
                {"categoria": "Madeira", "material": "Caibros 5x6", "unidade": "m", "quantidade": 1200},
                {"categoria": "Madeira", "material": "Terças 5x10", "unidade": "m", "quantidade": 380},
                {"categoria": "Madeira", "material": "Vigas 6x12/16", "unidade": "m", "quantidade": 140},
                {"categoria": "Complementos", "material": "Fixações diversas", "unidade": "vb", "quantidade": 1},
                {"categoria": "Complementos", "material": "Cantoneiras/chapas", "unidade": "vb", "quantidade": 1},
            ],
        },
        "formas": {
            "parametros": {
                "cobertura_tabua_pinus_m2": 0.9,
                "cobertura_tabua_mista_m2": 0.8,
                "espacamento_gravata_m": 0.4,
                "espacamento_escora_viga_m": 0.4,
                "espacamento_escora_laje_m": 0.6,
                "fracao_area_lateral": 2 / 3,
                "fracao_area_fundo": 1 / 3,
                "perda_sarrafo": 0.15,
            },
        },
    }


def carregar() -> dict:
    """Lê o dados_obra.json; cria com os valores semente se não existir.

    Faz merge raso das chaves de topo com a semente, para que uma
    atualização do app (nova aba/campo) não quebre um JSON já salvo.
    """
    seed = _seed()
    if not DATA_FILE.exists():
        salvar(seed)
        return seed

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        dados = json.load(f)

    alterado = False
    for chave, valor in seed.items():
        if chave not in dados:
            dados[chave] = valor
            alterado = True

    if "fontes_estruturais" not in dados or not dados["fontes_estruturais"]:
        if _migrar_lst_dados_antigo(dados):
            alterado = True

    if alterado:
        salvar(dados)
    return dados


def _migrar_lst_dados_antigo(dados: dict) -> bool:
    """Converte o antigo blob único `lst_dados` (vigas/pilares de todos os
    arquivos misturados) para uma fonte por pavimento em `fontes_estruturais`,
    agrupando pelo campo `pavimento` que cada item já carrega. Não perde os
    dados já processados em versões anteriores do app."""
    antigo = dados.pop("lst_dados", None)
    if not antigo or not (antigo.get("vigas") or antigo.get("pilares")):
        return False

    pavimentos = {}
    for v in antigo.get("vigas", []):
        pavimentos.setdefault(v["pavimento"], {"vigas": [], "pilares": []})["vigas"].append(v)
    for p in antigo.get("pilares", []):
        pavimentos.setdefault(p["pavimento"], {"vigas": [], "pilares": []})["pilares"].append(p)

    dados["fontes_estruturais"] = [
        {
            "arquivo": f"{pavimento}.LST",
            "pavimento": pavimento,
            "ativo": True,
            "vigas": conteudo["vigas"],
            "pilares": conteudo["pilares"],
        }
        for pavimento, conteudo in pavimentos.items()
    ]
    return True


def vigas_ativas(dados: dict) -> list:
    """Concatena as vigas de toda fonte estrutural com `ativo=True`."""
    vigas = []
    for fonte in dados.get("fontes_estruturais", []):
        if fonte.get("ativo", True):
            vigas.extend(fonte.get("vigas", []))
    return vigas


def pilares_ativas(dados: dict) -> list:
    """Concatena os pilares de toda fonte estrutural com `ativo=True`."""
    pilares = []
    for fonte in dados.get("fontes_estruturais", []):
        if fonte.get("ativo", True):
            pilares.extend(fonte.get("pilares", []))
    return pilares


def salvar(dados: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
