"""
Glue Job — Bronze para Silver
State of Data Brazil (2023-2024, 2024-2025, 2025-2026)

O que este job faz:
1. Lê os 3 CSVs brutos da camada Bronze (S3)
2. Padroniza os nomes de coluna (2023 usa um formato de cabeçalho diferente de 2024/2025)
3. Seleciona e renomeia as colunas-chave necessárias para responder as 7 perguntas de negócio
4. Une os 3 anos em uma única tabela, com coluna `ano_pesquisa`
5. Salva o resultado em Parquet na camada Silver

Testado localmente com pandas contra os 3 arquivos reais antes de virar este Glue Job —
a lógica de mapeamento foi validada (ver mapeamento_schema.md).
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, IntegerType

# ----------------------------------------------------------------------------
# Setup padrão do Glue Job
#
# Os caminhos do S3 estão fixos direto no código abaixo (BRONZE_PATH / SILVER_PATH),
# em vez de vir como Job parameter — isso evita depender de permissão pra editar
# parâmetros do Job no console (comum estar bloqueado no AWS Academy Lab).
# Se o nome do seu bucket for diferente, ajuste as 2 linhas abaixo antes de rodar.
# ----------------------------------------------------------------------------
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

BRONZE_PATH = "s3://data-aws-s3-postech-fiap-3/bronze/"
SILVER_PATH = "s3://data-aws-s3-postech-fiap-3/silver/"

# ----------------------------------------------------------------------------
# Mapeamento de colunas-chave por ano (validado contra os dados reais)
# ----------------------------------------------------------------------------

# 2023: cabeçalho vem como string de tupla Python -> "('P2_f ', 'Cargo Atual')"
COLS_2023 = {
    'id':               "('P0', 'id')",
    'idade':            "('P1_a ', 'Idade')",
    'genero':           "('P1_b ', 'Genero')",
    'cor_raca':         "('P1_c ', 'Cor/raca/etnia')",
    'pcd':              "('P1_d ', 'PCD')",
    'uf':               "('P1_i_1 ', 'uf onde mora')",
    'regiao':           "('P1_i_2 ', 'Regiao onde mora')",
    'nivel_ensino':     "('P1_l ', 'Nivel de Ensino')",
    'cargo_atual':      "('P2_f ', 'Cargo Atual')",
    'senioridade':      "('P2_g ', 'Nivel')",
    'faixa_salarial':   "('P2_h ', 'Faixa salarial')",
    'modelo_trabalho':  "('P2_r ', 'Atualmente qual a sua forma de trabalho?')",
    'usa_ia_trabalho':  "('P4_m ', 'Utiliza ChatGPT ou LLMs no trabalho?')",
}

COLS_2024 = {
    'id': '0.a_token', 'idade': '1.a_idade', 'genero': '1.b_genero',
    'cor_raca': '1.c_cor/raca/etnia', 'pcd': '1.d_pcd', 'uf': '1.i.1_uf_onde_mora',
    'regiao': '1.i.2_regiao_onde_mora', 'nivel_ensino': '1.l_nivel_de_ensino',
    'cargo_atual': '2.f_cargo_atual', 'senioridade': '2.g_nivel',
    'faixa_salarial': '2.h_faixa_salarial', 'modelo_trabalho': '2.r_modelo_de_trabalho_atual',
    'usa_ia_trabalho': '4.m_usa_chatgpt_ou_copilot_no_trabalho?',
}

# 2025: atenção, alguns códigos de pergunta mudaram de número em relação a 2024
# (ex: modelo_trabalho era 2.r em 2024 e virou 2.q em 2025 — mapeado por tema, não por código)
COLS_2025 = {
    'id': '0.a_token', 'idade': '1.a_idade', 'genero': '1.b_genero',
    'cor_raca': '1.c_cor/raca/etnia', 'pcd': '1.d_pcd', 'uf': '1.i.1_uf_onde_mora',
    'regiao': '1.i.2_regiao_onde_mora', 'nivel_ensino': '1.l_nivel_de_ensino',
    'cargo_atual': '2.f_cargo_atual', 'senioridade': '2.g_nivel',
    'faixa_salarial': '2.h_faixa_salarial', 'modelo_trabalho': '2.q_modelo_de_trabalho_atual',
    'usa_ia_trabalho': '4.j_usa_chatgpt_ou_copilot_no_trabalho?',
}


def load_and_standardize(path, col_map, ano):
    """Lê um CSV bruto e retorna um DataFrame Spark só com as colunas padronizadas."""
    df = spark.read.option("header", True).option("multiLine", True).option("escape", '"').csv(path)

    select_exprs = []
    for novo_nome, nome_original in col_map.items():
        # Colchetes no nome da coluna (formato 2023) precisam de escape com backtick
        select_exprs.append(F.col(f"`{nome_original}`").alias(novo_nome))

    df_std = df.select(*select_exprs)
    df_std = df_std.withColumn("ano_pesquisa", F.lit(ano).cast(IntegerType()))
    return df_std


# ----------------------------------------------------------------------------
# Carrega e padroniza os 3 anos
# Nomes de arquivo exatamente como estão no bucket (sem renomear) — ajuste aqui
# caso o nome do arquivo no S3 seja diferente do que está abaixo.
# ----------------------------------------------------------------------------
df_2023 = load_and_standardize(
    f"{BRONZE_PATH}State_of_data_BR_2023_Kaggle - df_survey_2023.csv", COLS_2023, 2023
)
df_2024 = load_and_standardize(
    f"{BRONZE_PATH}Final Dataset - State of Data 2024 - Kaggle - df_survey_2024.csv", COLS_2024, 2024
)
df_2025 = load_and_standardize(
    f"{BRONZE_PATH}Final Dataset - State of Data 2025-2026 - Kaggle.csv", COLS_2025, 2025
)

# ----------------------------------------------------------------------------
# Une os 3 anos em uma única tabela Silver
# ----------------------------------------------------------------------------
silver_df = df_2023.unionByName(df_2024).unionByName(df_2025)

# Limpeza leve: remove linhas totalmente vazias nas colunas-chave de perfil
silver_df = silver_df.dropna(how="all", subset=["cargo_atual", "senioridade", "faixa_salarial"])

# Padroniza tipo da idade (vem como string em alguns anos)
silver_df = silver_df.withColumn("idade", F.col("idade").cast(IntegerType()))

# Flag binária de uso de IA (usada nas agregações da camada Gold)
silver_df = silver_df.withColumn(
    "usa_ia_flag",
    F.when(F.col("usa_ia_trabalho").startswith("Não utilizo"), F.lit("Não usa"))
     .when(F.col("usa_ia_trabalho").isNotNull(), F.lit("Usa"))
     .otherwise(F.lit(None))
)

# ----------------------------------------------------------------------------
# Grava a camada Silver em Parquet, particionada por ano
# ----------------------------------------------------------------------------
silver_df.write.mode("overwrite").partitionBy("ano_pesquisa").parquet(SILVER_PATH)

print(f"Silver gravada com sucesso em {SILVER_PATH}")
print(f"Total de linhas: {silver_df.count()}")

job.commit()
