# Planejamento de Obra — Dashboard Multipage (Python + Streamlit)

Tradução em Python das 12 abas da planilha "Planilha Planejamento de Obras.xlsx"
para um dashboard com menu lateral, conectado ao parser de arquivos TQS Formas
(.LST) já desenvolvido anteriormente.

## Estrutura

```
Teste App/
├── app.py                  # ponto de entrada — só monta o menu lateral (st.navigation)
├── data_store.py            # fonte única da verdade: lê/grava dados_obra.json
├── catalog.py                # acesso ao catálogo de preços (equivalente ao PROCV manual)
├── models.py                  # dataclasses Viga, Pilar, ResumoOrcamento
├── parser_tqs.py               # extração de vigas/pilares dos .LST
├── calculos.py                  # volume, custo por Fck, estimativa de aço (vigas/pilares)
├── utils.py                       # formatação de moeda + helper de tabela editável
├── calc/                            # um módulo de cálculo por aba de orçamento
│   ├── fundacao.py                    # estacas + blocos/vigas baldrame
│   ├── concreto_tela_pop.py            # vigas/pilares do TQS
│   ├── alvenaria.py
│   ├── gesso.py
│   ├── forro.py
│   ├── metragens.py
│   ├── acabamentos.py                    # louças + metais + torneiras
│   ├── telhado.py
│   └── formas.py                           # conectado automaticamente às vigas do TQS
├── views/                                    # uma página Streamlit por aba
│   ├── inputs.py                              # upload .LST + catálogo + parâmetros gerais
│   ├── concreto_tela_pop.py
│   ├── formas.py / alvenaria.py / gesso.py / forro.py / metragens.py / acabamentos.py / telhado.py
│   └── resumo_geral.py                          # agregado geral da obra
├── dados_obra.json                                # gerado na 1ª execução (estado persistido)
└── requirements.txt
```

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre em `http://localhost:8501`. O menu lateral tem 3 seções:

- **Inputs**: envie os `.LST` do TQS, edite o catálogo de preços de materiais
  e os parâmetros gerais da obra (Fck padrão, perda, taxa/preço do aço,
  preço/m² de gesso/forro/revestimento).
- **Orçamentos**: uma página por aba da planilha original, com tabelas
  editáveis de quantidades/dimensões.
- **Resumo**: agregado geral da obra (custo total, custo por etapa, download
  do orçamento consolidado em `.xlsx`).

## Como funciona a reatividade

Todo o estado (catálogo de preços, parâmetros gerais, quantidades de cada
aba, resultado do último upload de `.LST`) vive num único arquivo
`dados_obra.json`, lido/gravado por `data_store.py`. Cada página carrega esse
arquivo no início da execução e salva a cada edição — como o Streamlit reroda
o script inteiro a cada interação, mudar um preço na página de Inputs (ex.:
concreto, bloco, torneira) atualiza automaticamente qualquer aba que usa
aquele preço, e o Resumo Geral, na próxima vez que a página rodar.

Cada aba de orçamento tem um módulo em `calc/` com uma função pura
`calcular(dados) -> (DataFrame, totais)`, usada tanto pela própria página
quanto pelo Resumo Geral — o número mostrado na aba e o número somado no
Resumo Geral vêm sempre do mesmo cálculo, nunca duplicado.

A aba **Formas** é o exemplo mais direto disso: o comprimento total de vigas
não é mais digitado à mão — vem da soma real das vigas processadas a partir
dos `.LST` na página de Inputs.

## Simplificações assumidas (com liberdade combinada com o usuário)

A planilha original tem fórmulas manuais e específicas de projeto (fiada a
fiada em alvenaria, tabelas de "teórico vs. prático", etc.). Para manter o
código sustentável, algumas contas foram simplificadas — documentado no
docstring de cada módulo em `calc/`. Os pontos principais:

- **Alvenaria**: quantidade de blocos = m² da parede / área da face do
  bloco (em vez de fiada a fiada).
- **Gesso, Forro, Metragens**: custo por m² é um parâmetro geral editável
  (a planilha original não isola um preço/m² único para esses itens — o
  custo lá vem de vários materiais somados).
- **Acabamentos**: as abas "TORNEIRAS,CUBAS ETC" e "LOUÇAS E METAIS
  DEFINIDOS" foram mescladas em uma só (eram a mesma lista de itens
  reapresentada na planilha original).
- **Aço** (vigas/pilares): taxa de armadura (kg/m³) estimada, editável em
  Inputs — a planilha original não calcula aço por fórmula, é lançamento
  manual.

## Limitação conhecida: pilares do TQS

Os arquivos `.LST` de **Formas** trazem área e volume por pilar, mas não a
seção transversal (largura × profundidade) individual — só o valor default
do projeto. Por isso os pilares extraídos do TQS aparecem no dashboard como
referência (área/volume real), mas não entram no custo por Fck sem
informar largura/profundidade manualmente — igual a planilha original.

## Próximos passos sugeridos

1. Trocar o JSON local por um banco leve (SQLite/Supabase) se o projeto
   crescer para múltiplas obras/usuários simultâneos.
2. Adicionar edição fiada a fiada de alvenaria, se a estimativa por m² não
   for precisa o suficiente para o seu caso.
3. Puxar a seção transversal de pilares de outro relatório do TQS (se
   disponível), para não depender de lançamento manual.
