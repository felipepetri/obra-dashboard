"""
Modelos de dados para o planejamento de obra.

Traduz as tabelas da planilha (abas "CONCRETO E TELA POP") para
estruturas Python puras, sem depender do Excel.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Viga:
    """Representa uma viga (equivalente a uma linha da tabela de vigas na planilha)."""

    nomenclatura: str          # ex.: "V401"
    largura: float             # m  (coluna "LARGURA" na planilha)
    comprimento: float         # m  (coluna "COMPRIMENTO" — vem do parser TQS)
    profundidade: float        # m  (coluna "PROFUNDIDADE"/altura)
    fck: float = 25.0          # MPa
    pavimento: Optional[str] = None
    perda: float = 0.10        # 10% de perda, igual à planilha (*1.1)

    @property
    def volume_m3(self) -> float:
        """Equivalente a =LARGURA*COMPRIMENTO*PROFUNDIDADE na planilha."""
        return self.largura * self.comprimento * self.profundidade

    @property
    def volume_com_perda_m3(self) -> float:
        """Equivalente a =VOLUME*1.1 na planilha."""
        return self.volume_m3 * (1 + self.perda)


@dataclass
class Pilar:
    """Representa um pilar (equivalente às linhas da tabela 'PILARES')."""

    nomenclatura: str          # ex.: "P1", "P1 LANCE 2"
    altura: float               # m  (pé-direito / lance do pilar)
    largura: float               # m
    profundidade: float          # m
    fck: float = 25.0
    pavimento: Optional[str] = None
    perda: float = 0.10

    @property
    def volume_m3(self) -> float:
        return self.altura * self.largura * self.profundidade

    @property
    def volume_com_perda_m3(self) -> float:
        return self.volume_m3 * (1 + self.perda)


@dataclass
class ResumoOrcamento:
    """Agregado de custos e quantidades para exibição/dashboard."""

    volume_concreto_m3: float = 0.0
    custo_concreto: float = 0.0
    peso_aco_kg: float = 0.0
    custo_aco: float = 0.0
    itens: list = field(default_factory=list)

    @property
    def custo_total(self) -> float:
        return self.custo_concreto + self.custo_aco
