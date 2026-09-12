"""
Glue Job — Unpivot de Tecnologias (Linguagens de Programação)
State of Data Brazil — resolve a Pergunta 4 do desafio

Cada linguagem é uma coluna binária própria na pesquisa (ex: uma coluna só
pra "usa Python", outra só pra "usa SQL"). Este job transforma esse bloco
de colunas largas em um formato longo (tecnologia | usa), pronto pra agregar.

Rode depois do glue_job_bronze_to_silver.py — lê direto da Bronze porque as
colunas de tecnologia não fazem parte do recorte de colunas-chave da Silver.
"""

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

BRONZE_PATH = "s3://data-aws-s3-postech-fiap-3/bronze/"
GOLD_PATH = "s3://data-aws-s3-postech-fiap-3/gold/"

# Bloco de colunas de linguagem por ano (validado contra os dados reais).
# O prefixo muda de ano pra ano porque a pergunta foi renumerada em 2025.
LINGUAGENS_2023 = {  # formato tupla-string
    "('P4_d_1 ', 'SQL')": "SQL", "('P4_d_2 ', 'R ')": "R",
    "('P4_d_3 ', 'Python')": "Python", "('P4_d_4 ', 'C/C++/C#')": "C/C++/C#",
    "('P4_d_6 ', 'Java')": "Java", "('P4_d_10 ', 'Scala')": "Scala",
    "('P4_d_12 ', 'Rust')": "Rust", "('P4_d_14 ', 'JavaScript')": "JavaScript",
}
LINGUAGENS_2024 = {
    "4.d.1_SQL": "SQL", "4.d.2_R": "R", "4.d.3_Python": "Python",
    "4.d.4_C/C++/C#": "C/C++/C#", "4.d.6_Java": "Java", "4.d.10_Scala": "Scala",
    "4.d.12_Rust": "Rust", "4.d.14_JavaScript": "JavaScript",
}
LINGUAGENS_2025 = {
    "4.c.1_SQL": "SQL", "4.c.2_R": "R", "4.c.3_Python": "Python",
    "4.c.4_C/C++/C#": "C/C++/C#", "4.c.7_Scala": "Scala", "4.c.9_Rust": "Rust",
}


def unpivot_linguagens(path, col_map, ano):
    df = spark.read.option("header", True).csv(path)
    stacks = []
    for col_original, nome_tech in col_map.items():
        if col_original not in df.columns:
            continue
        stacks.append(
            df.select(
                F.lit(ano).alias("ano_pesquisa"),
                F.lit(nome_tech).alias("tecnologia"),
                F.col(f"`{col_original}`").cast("double").alias("flag"),
            )
        )
    unioned = stacks[0]
    for s in stacks[1:]:
        unioned = unioned.unionByName(s)
    return unioned.filter(F.col("flag") == 1.0)


ling_2023 = unpivot_linguagens(f"{BRONZE_PATH}State_of_data_BR_2023_Kaggle - df_survey_2023.csv", LINGUAGENS_2023, 2023)
ling_2024 = unpivot_linguagens(f"{BRONZE_PATH}Final Dataset - State of Data 2024 - Kaggle - df_survey_2024.csv", LINGUAGENS_2024, 2024)
ling_2025 = unpivot_linguagens(f"{BRONZE_PATH}Final Dataset - State of Data 2025-2026 - Kaggle.csv", LINGUAGENS_2025, 2025)

todas_linguagens = ling_2023.unionByName(ling_2024).unionByName(ling_2025)

gold_tecnologias = (
    todas_linguagens.groupBy("ano_pesquisa", "tecnologia")
    .agg(F.count("*").alias("total"))
)

gold_tecnologias.write.mode("overwrite").parquet(f"{GOLD_PATH}tecnologias_por_ano/")

print("Tabela Gold de tecnologias gerada com sucesso.")
job.commit()
