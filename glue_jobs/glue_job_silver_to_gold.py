"""
Glue Job — Silver para Gold
State of Data Brazil — tabelas agregadas para as 7 perguntas de negócio

Gera uma tabela Gold por pergunta de negócio, já pronta para consumo no
Athena ou para gerar gráfico direto (sem precisar reprocessar a Silver toda vez).
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

SILVER_PATH = "s3://data-aws-s3-postech-fiap-3/silver/"
GOLD_PATH = "s3://data-aws-s3-postech-fiap-3/gold/"

silver = spark.read.parquet(SILVER_PATH)

# 1) Estrutura do mercado — distribuição de cargos por ano
gold_cargos = (
    silver.groupBy("ano_pesquisa", "cargo_atual")
    .agg(F.count("*").alias("total"))
    .withColumn("pct", F.col("total") / F.sum("total").over(
        __import__("pyspark.sql.window", fromlist=["Window"]).Window.partitionBy("ano_pesquisa")
    ) * 100)
)
gold_cargos.write.mode("overwrite").parquet(f"{GOLD_PATH}cargos_por_ano/")

# 2) Perfis valorizados — senioridade x faixa salarial
gold_senioridade_salario = (
    silver.groupBy("ano_pesquisa", "senioridade", "faixa_salarial")
    .agg(F.count("*").alias("total"))
)
gold_senioridade_salario.write.mode("overwrite").parquet(f"{GOLD_PATH}senioridade_salario/")

# 3) Diversidade de gênero — evolução por ano e por cargo
gold_genero = (
    silver.groupBy("ano_pesquisa", "genero")
    .agg(F.count("*").alias("total"))
)
gold_genero.write.mode("overwrite").parquet(f"{GOLD_PATH}genero_por_ano/")

gold_genero_cargo = (
    silver.groupBy("ano_pesquisa", "cargo_atual", "genero")
    .agg(F.count("*").alias("total"))
)
gold_genero_cargo.write.mode("overwrite").parquet(f"{GOLD_PATH}genero_por_cargo/")

# 4) Adoção de IA — evolução por ano
gold_ia = (
    silver.groupBy("ano_pesquisa", "usa_ia_flag")
    .agg(F.count("*").alias("total"))
)
gold_ia.write.mode("overwrite").parquet(f"{GOLD_PATH}adocao_ia_por_ano/")

# 5) Diferenças regionais / modelo de trabalho
gold_regiao = (
    silver.groupBy("ano_pesquisa", "regiao")
    .agg(F.count("*").alias("total"))
)
gold_regiao.write.mode("overwrite").parquet(f"{GOLD_PATH}distribuicao_regiao/")

gold_modelo_trabalho = (
    silver.groupBy("ano_pesquisa", "modelo_trabalho")
    .agg(F.count("*").alias("total"))
)
gold_modelo_trabalho.write.mode("overwrite").parquet(f"{GOLD_PATH}modelo_trabalho_por_ano/")

print("Camada Gold gerada com sucesso em:", GOLD_PATH)
job.commit()
