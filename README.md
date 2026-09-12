# TECH CHALLENGE 3 - PÓS TECH FIAP ☁️

> **Tech Challenge 3 - Data Analytics**
> Universidade FIAP - 2026

![AWS](https://img.shields.io/badge/Cloud-AWS%20Academy%20Lab-orange)
![Python](https://img.shields.io/badge/Linguagem-Python%20%7C%20PySpark-blue)
![Data Engineering](https://img.shields.io/badge/Tema-Data%20Engineering%20%26%20Analytics-purple)
![Status](https://img.shields.io/badge/Status-Concluído-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Sobre o Projeto

**📊 Case: O Mercado Brasileiro de Dados em 3 Anos de Pesquisa**

Este projeto simula o trabalho de uma consultoria estratégica de dados contratada por uma instituição financeira de grande porte que planeja expandir sua área de Dados, Analytics e Inteligência Artificial. Antes de contratar, capacitar e investir, a empresa precisa entender o mercado brasileiro de profissionais de dados com base em evidência, não em achismo.

Para isso, foi construído um pipeline completo de Engenharia de Dados e Analytics em ambiente Cloud (AWS), processando as 3 últimas edições completas da pesquisa **State of Data Brazil** (Data Hackers, em parceria com a Bain), da ingestão bruta até as consultas analíticas que respondem às perguntas de negócio do desafio.

---

## Objetivo do Trabalho

Construir uma solução de ponta a ponta capaz de:

* ingerir e organizar as 3 últimas edições da pesquisa State of Data Brazil em um Data Lake no S3;
* padronizar o schema entre edições com nomenclaturas de coluna diferentes (2023 vs. 2024/2025);
* tratar, transformar e catalogar os dados com AWS Glue (Jobs + Crawler + Data Catalog);
* organizar os dados em camadas **Bronze → Silver → Gold**;
* consultar as tabelas Gold via Amazon Athena para responder 7 perguntas de negócio;
* apresentar os resultados em um material executivo com DataViz e Storytelling.

---

## 📈 Sobre o Dataset

O projeto utiliza a pesquisa **State of Data Brazil**, da comunidade Data Hackers em parceria com a Bain, disponível no Kaggle.

Dataset utilizado:

[State of Data Brazil — Kaggle](https://www.kaggle.com/datahackers/datasets)

Foram usadas as **3 últimas edições completas** da pesquisa. A verificação da data real de coleta (não apenas o nome do arquivo) mostrou que a edição "2025-2026" já está fechada, coletada entre out/2025 e dez/2025 — por isso ela é, de fato, a mais recente disponível, e a edição de 2022 ficou fora do escopo obrigatório.

| Edição | Respostas | Período de coleta |
|---|---|---|
| 2023-2024 | 5.293 | 2023 |
| 2024-2025 | 5.217 | 14/out a 18/dez/2024 |
| 2025-2026 | 3.495 | 20/out a 22/dez/2025 |
| **Total** | **14.005** | |

Os arquivos brutos não são versionados neste repositório (ver `data/README.md` para instruções de download).

---

## ☁️ Arquitetura da Solução (AWS)

Pipeline em camadas, executado no **AWS Academy Lab**:

```
Kaggle (3 CSVs) → S3 [Bronze] → Glue Job (PySpark) → S3 [Silver]
                → Glue Job (agregação + unpivot) → S3 [Gold]
                → Glue Crawler → Glue Data Catalog
                → Amazon Athena → Material Executivo
```

* **Bronze** — os 3 CSVs brutos, sem tratamento.
* **Silver** — schema unificado entre as 3 edições (cada uma usa um formato de coluna diferente — ver `docs/mapeamento_schema.md`).
* **Gold** — tabelas agregadas por tema de negócio (cargos, senioridade, gênero, tecnologias, IA, região, modelo de trabalho).

O diagrama completo está em `architecture/diagrama_arquitetura.png` (fonte editável em `architecture/arquitetura_state_of_data.drawio`), e evidências reais de cada etapa rodando no AWS Academy Lab estão em `evidencias/`.

---

## Arquivos do Projeto

```text
tech-challenge-3-state-of-data-aws/
├── data/
│   └── README.md                          # instruções para baixar os 3 CSVs no Kaggle
│
├── notebooks/
│   └── analise_state_of_data.ipynb        # análise exploratória e validação local (pandas/PySpark)
│
├── glue_jobs/
│   ├── glue_job_bronze_to_silver.py       # padronização de schema entre as 3 edições
│   ├── glue_job_silver_to_gold.py         # agregações para as 7 perguntas de negócio
│   └── glue_job_tecnologias_unpivot.py    # unpivot das colunas de tecnologias/ferramentas
│
├── sql/
│   └── athena_queries.sql                 # as 7 consultas analíticas no Athena
│
├── architecture/
│   ├── arquitetura_state_of_data.drawio   # diagrama editável (Draw.io)
│   └── diagrama_arquitetura.png           # diagrama exportado
│
├── evidencias/
│   ├── 01_s3/                             # bucket e camadas Bronze/Silver/Gold
│   ├── 02_glue_jobs/                      # execuções dos 3 Glue Jobs
│   ├── 03_glue_crawler_catalogo/          # crawler e Data Catalog
│   └── 04_athena/                         # as 7 consultas rodando com dado real
│
├── results/
│   ├── grafico_top_cargos.png
│   ├── grafico_linguagens.png
│   ├── grafico_adocao_ia.png
│   └── grafico_regiao.png
│
├── docs/
│   ├── insights_principais.md             # os 7 achados, com números reais
│   ├── mapeamento_schema.md               # de-para de colunas entre as 3 edições
│   ├── cronograma_tech_challenge.md       # checklist e cronograma do desafio
│   └── roteiro_video.md                   # roteiro do vídeo executivo
│
├── Material_Executivo_State_of_Data.pptx
├── Relatorio_Executivo_State_of_Data.docx
├── Video_Apresentacao_Executiva.txt
├── requirements.txt
└── README.md
```

---

## 📥 Como Reproduzir a Análise

### 1. Baixar as 3 edições da pesquisa

🔗 [State of Data Brazil — Kaggle](https://www.kaggle.com/datahackers/datasets)

Baixe as edições 2023-2024, 2024-2025 e 2025-2026, e salve os CSVs em `data/` (ver `data/README.md`).

### 2. Ambiente AWS Academy Lab

Este projeto foi executado no **AWS Academy Learner Lab** (S3, Glue, Athena). Para reproduzir:

1. Suba os 3 CSVs para `s3://data-aws-s3-postech-fiap-3/bronze/`.
2. Crie um Glue Crawler para catalogar a Bronze.
3. Rode `glue_jobs/bronze_to_silver.py` como Glue Job (Spark), ajustando os paths de entrada/saída para o seu bucket.
4. Catalogue a Silver com um crawler.
5. Rode `glue_jobs/silver_to_gold.py` e `glue_jobs/tecnologias_unpivot.py`.
6. Catalogue a Gold e execute as consultas de `sql/athena_queries.sql` no Athena.

### 3. Validação local (opcional)

As bibliotecas usadas na análise exploratória local (`notebooks/analise_state_of_data.ipynb`):

```bash
pip install -r requirements.txt
jupyter notebook notebooks/analise_state_of_data.ipynb
```

---

## Metodologia

1. **Ingestão** — os 3 CSVs brutos do Kaggle sobem para o S3 (Bronze), sem tratamento.
2. **Padronização de schema** — cada edição nomeia colunas de forma diferente (2023 usa tuplas Python; 2024/2025 usam `codigo_snake_case`, e até entre 2024 e 2025 alguns códigos de pergunta mudam de número). A padronização foi feita por **tema da pergunta**, não por posição/código — detalhes em `docs/mapeamento_schema.md`.
3. **Agregação (Gold)** — tabelas por tema de negócio (cargos, senioridade, gênero, tecnologias, IA, região, modelo de trabalho), prontas para consulta.
4. **Consulta analítica** — as 7 perguntas de negócio respondidas via Amazon Athena sobre o Data Catalog.
5. **Storytelling** — gráficos e material executivo (PPT + relatório em Word) com a narrativa dos achados.

---

## 📊 Principais Insights

* **Estrutura do mercado**: Analista de Dados (24%), Cientista de Dados (17%) e Engenheiro de Dados (16,1%) somam mais da metade do mercado em 2025.
* **Novo topo de carreira**: a categoria "Especialista/Staff+" surgiu em 2025 (14% dos respondentes), com faixa salarial de R$ 12.001 a R$ 16.000/mês — sinal de trilhas técnicas sênior se formalizando.
* **Diversidade de gênero em queda**: participação feminina caiu em 3 edições seguidas — 24,4% (2023) → 23,5% (2024) → 22,0% (2025).
* **Mercado bilíngue**: Python (55,2%) e SQL (50,5%) dominam disparado como tecnologias do dia a dia; nenhuma outra linguagem passa de 10%.
* **Adoção de IA — o achado mais forte**: de 80,5% (2023) para 98% (2025) dos profissionais já usam alguma solução de IA generativa no trabalho.
* **Concentração regional**: 64,4% dos profissionais de dados estão no Sudeste; o Norte tem apenas 1,4%.
* **Reversão do modelo de trabalho**: o modelo 100% presencial cresceu de 16,3% (2024) para 20,8% (2025), na contramão da narrativa de home office definitivo.

Detalhamento completo em `docs/insights_principais.md`.

---

## Conclusão

O mercado brasileiro de Dados amadureceu de forma visível entre 2023 e 2025: criou uma trilha de carreira sênior formal, tornou o uso de IA generativa praticamente universal e se consolidou em torno de duas tecnologias centrais (Python e SQL). Ao mesmo tempo, mantém desafios estruturais que não se resolveram sozinhos — concentração regional extrema e diversidade de gênero em queda.

Como próximos passos, recomenda-se:

* aprofundar a análise de tecnologias com o bloco completo de ferramentas (cloud, BI, orquestração);
* cruzar região e senioridade para recomendações de contratação mais específicas por praça;
* acompanhar a edição 2026-2027 para confirmar se a tendência de queda de diversidade se mantém.

---

## 📌 Entregáveis

* Pipeline de dados completo em AWS (S3, Glue, Athena), com camadas Bronze/Silver/Gold;
* Glue Jobs em PySpark para padronização e agregação;
* Consultas analíticas no Athena para as 7 perguntas de negócio;
* Diagrama de arquitetura da solução (Draw.io);
* Notebook de análise exploratória e validação;
* Material executivo com DataViz e Storytelling (PowerPoint);
* Relatório executivo (Word).

---

## 🧑‍💻 Tecnologias Utilizadas

* AWS S3, AWS Glue (Jobs + Crawler + Data Catalog), Amazon Athena;
* Python (Pandas, Matplotlib, Seaborn) para validação local;
* Draw.io para o diagrama de arquitetura;
* AWS Academy Learner Lab.

---

## 📚 Referências

* State of Data Brazil — Data Hackers, em parceria com a Bain (Kaggle).
* Documentação oficial da AWS (S3, Glue, Athena).
* Materiais da Pós Tech FIAP — Data Analytics.

---

## 👥 Integrantes do Grupo

| Nome                             | RM     |
| -------------------------------- | ------ |
| Emerson Henrique de Lima e Sousa | 373751 |
| Moacyr Souza Barros              | 373412 |
