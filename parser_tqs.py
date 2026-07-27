"""
Parser dos relatórios TQS Formas (.LST) — extrai vigas e pilares.

Mesma lógica implementada em VBA no chat anterior, agora em Python puro,
pronta para ser chamada de dentro do Streamlit (upload de arquivo em
memória, sem precisar salvar em disco).
"""

import io
import re
from dataclasses import dataclass
from typing import List, Union

# --------------------------------------------------------------------
# Padrões usados na extração. Evitam depender de caracteres acentuados
# (ex. "VÃO") para funcionar independente da codificação do arquivo.
# --------------------------------------------------------------------
RE_BLOCO_VIGA = re.compile(r"da VIGA\s+(\S+)")
RE_VAO = re.compile(r"=\s+(\d+)\s+/L=\s*([\d.]+)\s*/B=\s*([\d.]+)\s*/H=\s*([\d.]+)")
RE_PILAR = re.compile(
    r"^\s*(P+\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", re.MULTILINE
)
RE_PE_DIREITO = re.compile(r"^\s*\d+\s+\S+\s+([\d.]+)\s+([\d.]+)\s+\d+", re.MULTILINE)


@dataclass
class VaoViga:
    pavimento: str
    viga: str
    vao: int
    comprimento_m: float
    largura_cm: float
    altura_cm: float


@dataclass
class QuantitativoPilar:
    pavimento: str
    pilar: str
    area_estruturada_m2: float
    area_formas_m2: float
    volume_concreto_m3: float
    volume_topo_m3: float
    pe_direito_ref_m: str


def _ler_texto(arquivo: Union[str, bytes, io.IOBase]) -> str:
    """Aceita caminho, bytes (upload do Streamlit) ou file-like object."""
    if hasattr(arquivo, "read"):
        conteudo = arquivo.read()
    elif isinstance(arquivo, (bytes, bytearray)):
        conteudo = arquivo
    else:
        with open(arquivo, "rb") as f:
            conteudo = f.read()
    if isinstance(conteudo, bytes):
        conteudo = conteudo.decode("latin-1")
    return conteudo


def _nome_pavimento(nome_arquivo: str) -> str:
    base = nome_arquivo.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    base = base.rsplit(".", 1)[0]
    return base.replace("_", " ")


def extrair_vigas(texto: str, pavimento: str) -> List[VaoViga]:
    resultado = []
    blocos = list(RE_BLOCO_VIGA.finditer(texto))
    for i, m in enumerate(blocos):
        inicio = m.end()
        fim = blocos[i + 1].start() if i + 1 < len(blocos) else len(texto)
        bloco_texto = texto[inicio:fim]
        for vao, L, B, H in RE_VAO.findall(bloco_texto):
            resultado.append(
                VaoViga(
                    pavimento=pavimento,
                    viga=f"V{m.group(1)}",
                    vao=int(vao),
                    comprimento_m=round(float(L) / 100, 3),
                    largura_cm=float(B),
                    altura_cm=float(H),
                )
            )
    return resultado


def extrair_pilares(texto: str, pavimento: str) -> List[QuantitativoPilar]:
    pd_match = RE_PE_DIREITO.search(texto)
    pd_ref = pd_match.group(2) if pd_match else ""

    resultado = []
    for pid, area_estr, area_formas, vol_conc, vol_topo in RE_PILAR.findall(texto):
        resultado.append(
            QuantitativoPilar(
                pavimento=pavimento,
                pilar=pid,
                area_estruturada_m2=float(area_estr),
                area_formas_m2=float(area_formas),
                volume_concreto_m3=float(vol_conc),
                volume_topo_m3=float(vol_topo),
                pe_direito_ref_m=pd_ref,
            )
        )
    return resultado


def processar_arquivo(nome_arquivo: str, conteudo_bytes: bytes):
    """Recebe nome + bytes (ex.: de um st.file_uploader) e retorna (vigas, pilares)."""
    texto = _ler_texto(conteudo_bytes)
    pavimento = _nome_pavimento(nome_arquivo)
    return extrair_vigas(texto, pavimento), extrair_pilares(texto, pavimento)


def vigas_para_dimensoes(vaos: List[VaoViga]) -> dict:
    """
    Agrega os vãos por viga (soma de comprimento por nome de viga),
    no formato que a aba 'VIGAS PRIMEIRA/SEGUNDA LAJE' da planilha espera:
    uma linha por viga com largura, comprimento total e profundidade.

    Largura e altura assumem o valor do primeiro vão (na prática são
    constantes ao longo da viga na maioria dos projetos residenciais;
    se houver mudança de seção no meio da viga, isso fica sinalizado
    em 'secao_variavel').
    """
    agregados = {}
    for v in vaos:
        chave = (v.pavimento, v.viga)
        if chave not in agregados:
            agregados[chave] = {
                "pavimento": v.pavimento,
                "viga": v.viga,
                "comprimento_total_m": 0.0,
                "larguras_cm": set(),
                "alturas_cm": set(),
            }
        agregados[chave]["comprimento_total_m"] += v.comprimento_m
        agregados[chave]["larguras_cm"].add(v.largura_cm)
        agregados[chave]["alturas_cm"].add(v.altura_cm)

    saida = {}
    for chave, dados in agregados.items():
        saida[chave] = {
            "pavimento": dados["pavimento"],
            "viga": dados["viga"],
            "comprimento_total_m": round(dados["comprimento_total_m"], 3),
            "largura_m": round(min(dados["larguras_cm"]) / 100, 3),
            "altura_m": round(min(dados["alturas_cm"]) / 100, 3),
            "secao_variavel": len(dados["larguras_cm"]) > 1 or len(dados["alturas_cm"]) > 1,
        }
    return saida
