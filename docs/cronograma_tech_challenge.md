# Tech Challenge — Checklist Completo por Etapa
**Prazo: 01/09 a 15/09 (14 dias)**

> **Decisão registrada (03/09):** as "3 últimas pesquisas" corretas são **2023-2024, 2024-2025 e 2025-2026** (não 2022/2023/2024). Confirmado pela data real de coleta dentro dos arquivos: a edição "2025-2026" foi coletada entre 20/out e 22/dez/2025 e já está fechada — o nome da edição só reflete que o relatório saiu no ano seguinte à coleta, não que a pesquisa está em andamento. O arquivo de 2022 fica de fora do pipeline obrigatório (guardado como possível bônus de tendência histórica).
>
> **Arquivos usados:** `State_of_data_BR_2023...csv` (5.293 respostas), `Final_Dataset_2024...csv` (5.217 respostas), `Final_Dataset_2025-2026...csv` (3.495 respostas).

---

## 0. Entregáveis finais (não perder de vista)

- [ ] **Material executivo** (PPT ou PDF) com DataViz + Storytelling, respondendo às perguntas de negócio, com o **diagrama de arquitetura incluído dentro dele**
- [ ] **Diagrama de arquitetura AWS** (Draw.io)
- [ ] **Scripts/notebooks** (PySpark e/ou SQL) organizados: ingestão → tratamento → transformação → catalogação → consultas analíticas

---

## ETAPA 1 — Setup e Ingestão (01/09 a 02/09)

- [x] Baixar as **3 últimas pesquisas** do State of Data Brasil (Kaggle / Data Hackers) — 2023-2024, 2024-2025, 2025-2026
- [ ] Testar login e sessão do **AWS Academy Lab** (confirmar limite de 4h por sessão e horas totais do curso)
- [x] Explorar os 3 arquivos localmente (Python/pandas): colunas, tipos, diferenças de schema entre os anos
- [x] Mapear quais colunas mudaram de nome/formato entre as pesquisas — ver `mapeamento_schema.md`
- [ ] Criar bucket **S3** e estrutura de pastas (ex: `/bronze`, `/silver`, `/gold`)
- [ ] Subir os 3 arquivos brutos → camada **Bronze**
- [x] Rascunho do diagrama de arquitetura feito (referência gerada no chat) — replicar essa estrutura no **Draw.io**

---

## ETAPA 2 — ETL e Catalogação (03/09 a 05/09)

- [ ] Criar bucket **S3** e subir os 3 CSVs brutos → camada **Bronze** *(feito localmente na análise; falta fazer no console AWS)*
- [ ] Criar **Glue Crawler** para catalogar a camada Bronze no Data Catalog
- [x] Escrever **Glue Job** em PySpark para tratamento e padronização → `glue_job_bronze_to_silver.py` (lógica validada localmente contra os 3 arquivos reais)
- [ ] Rodar o Glue Job de fato no AWS Academy Lab e conferir a Silver gerada
- [ ] Rodar Crawler/catalogar a Silver
- [x] Validar schema, contagem de linhas e amostra dos dados (14.005 linhas ao todo, ver `mapeamento_schema.md`)

---

## ETAPA 3 — Camada Gold e Consultas Analíticas (06/09 a 08/09)

- [x] Definir as tabelas agregadas necessárias para as 7 perguntas
- [x] Escrever o Glue Job de agregação → `glue_job_silver_to_gold.py`
- [ ] Rodar o Glue Job de agregação de fato no AWS
- [ ] Catalogar a Gold
- [x] Escrever as queries Athena → `athena_queries.sql` (todas as 7 perguntas cobertas)
- [ ] Rodar as queries de fato no Athena (AWS) e conferir os números batem com a validação local
- [x] Job de tecnologias (Python, SQL etc.) escrito → `glue_job_tecnologias_unpivot.py`

---

## ETAPA 4 — Análise e Geração dos Gráficos (09/09 a 10/09)

- [x] Responder as 7 perguntas com dado real, incluindo tecnologias (ver `insights_principais.md`)
  - [x] Como está estruturado o mercado brasileiro de Dados?
  - [x] Quais perfis profissionais são mais valorizados?
  - [x] Qual o cenário de diversidade de gênero?
  - [x] Quais tecnologias têm maior adoção? (Python 55,2% e SQL 50,5% dominam)
  - [x] Qual o índice de adoção de IA e seu impacto?
  - [x] Diferenças por região, senioridade e modelo de trabalho?
  - [x] Oportunidades e desafios para empresas que querem investir em Dados/IA?
- [x] Gerar os gráficos finais a partir dos números reais (4 gráficos prontos, estilo bordô/dourado)
- [x] Escrever os principais insights em texto corrido → `insights_principais.md`

---

## ETAPA 5 — Montagem do Material Executivo (11/09 a 12/09)

- [x] Estruturar o roteiro do PPT (contexto → metodologia → achados por pergunta → recomendações)
- [x] Montar os slides com os gráficos gerados, na paleta oficial do State of Data Brazil → `material_executivo_state_of_data.pptx`
- [x] Relatório executivo em Word, mesmo padrão estrutural da entrega anterior → `relatorio_executivo_state_of_data.docx`
- [x] Notebook consolidado com PySpark real, já executado → `analise_state_of_data.ipynb`
- [x] Diagrama de arquitetura final em formato `.drawio` (pronto pra abrir/editar em draw.io) → `arquitetura_state_of_data.drawio`
- [x] Revisar se as 7 perguntas estão todas respondidas visualmente
- [x] Nomes e RMs reais preenchidos no relatório (Emerson Henrique de Lima e Sousa — RM 373751, Moacyr Souza Barros — RM 373412)
- [x] Diagrama exportado como imagem e embutido dentro do PPT (slide de anexo)
- [x] Roteiro do vídeo executivo escrito, mesmo padrão da entrega anterior → `roteiro_video.md`
- [ ] Trocar o link do repositório GitHub (ainda placeholder no relatório)

---

## ETAPA 6 — Revisão Final e Entrega (13/09 a 15/09)

- [x] Organizar e limpar todos os notebooks/scripts (nomeação clara, comentários explicando cada etapa)
- [ ] **Rodar de fato no AWS** (S3, os 3 Glue Jobs, Crawler, catalogação, Athena) — fica por conta de vocês, código já pronto
- [ ] Conferir se todos os entregáveis estão completos e consistentes entre si (uma última revisão manual)
- [ ] Gravar o vídeo executivo (roteiro pronto em `roteiro_video.md`)
- [ ] Ensaiar a apresentação, se houver live/defesa com docentes
- [ ] Conferir o formato exato de entrega exigido pela FIAP (portal, nome de arquivo, etc.)
- [ ] Guardar um dia de folga (14/09) para imprevistos antes da entrega em **15/09**

---

## Riscos para ficar de olho

- [ ] **Budget de horas do AWS Academy Lab** — mesmo relogando sem problema, o total de horas do curso é limitado. Evitem deixar sessão aberta sem uso.
- [ ] **Schema inconsistente entre os 3 anos da pesquisa** — mapear isso cedo (Etapa 1) evita retrabalho na Etapa 2.
- [ ] Guardar **prints/logs** do Glue e Athena funcionando, como evidência do pipeline rodando.
- [ ] Não deixar a montagem do PPT para a última noite — storytelling bom exige revisão, não é só "colar gráfico".
- [ ] Aproveitar as **lives com os docentes** durante o desenvolvimento para tirar dúvidas e validar o andamento (não é obrigatório, mas ajuda a evitar retrabalho).

---

*Checklist para prazo 01/09 → 15/09/2026.*
