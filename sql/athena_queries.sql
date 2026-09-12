-- ============================================================================
-- Queries Athena — State of Data Brazil (2023-2024, 2024-2025, 2025-2026)
-- Assume que o Glue Crawler já catalogou as tabelas da camada Gold
-- (cada subpasta da Gold catalogada como uma tabela própria)
--
-- Padrão adotado em todas as queries:
--   - COALESCE(coluna, 'Não Informado') para não deixar linha em branco
--   - Percentual formatado como texto, ex: 19.08%
--   - IMPORTANTE: a ordenação (ORDER BY) é sempre feita pelo valor NUMÉRICO do
--     percentual, calculado numa CTE, e só depois formatado como texto na
--     consulta final. Ordenar direto pela coluna já formatada como texto
--     ordena por ordem alfabética, não por valor (ex: "16.10%" viria antes
--     de "5.60%", porque '1' < '5' como caractere).
-- ============================================================================

-- 1) Como está estruturado o mercado brasileiro de Dados?
-- (top cargos, e como a composição mudou ao longo dos 3 anos)
-- OBS: exclui quem não respondeu a pergunta de cargo do cálculo do percentual,
-- pra bater com a metodologia usada no relatório executivo (% de quem respondeu).
WITH calc AS (
    SELECT ano_pesquisa,
           cargo_atual AS cargo,
           total,
           total * 100.0 / SUM(total) OVER (PARTITION BY ano_pesquisa) AS pct_num
    FROM cargos_por_ano
    WHERE cargo_atual IS NOT NULL
)
SELECT ano_pesquisa,
       cargo,
       total,
       format('%.2f', pct_num) || '%' AS pct
FROM calc
ORDER BY ano_pesquisa, pct_num DESC;


-- 2) Quais perfis profissionais são mais valorizados pelo mercado?
-- (cruza senioridade com faixa salarial mais recente — sem percentual, ordena por total mesmo)
SELECT coalesce(senioridade, 'Não Informado') AS senioridade,
       coalesce(faixa_salarial, 'Não Informado') AS faixa_salarial,
       total
FROM senioridade_salario
WHERE ano_pesquisa = 2025
ORDER BY total DESC;


-- 3) Qual é o cenário de diversidade de gênero nas carreiras de dados?
-- (evolução geral)
WITH calc AS (
    SELECT ano_pesquisa,
           coalesce(genero, 'Não Informado') AS genero,
           total,
           total * 100.0 / SUM(total) OVER (PARTITION BY ano_pesquisa) AS pct_num
    FROM genero_por_ano
)
SELECT ano_pesquisa,
       genero,
       total,
       format('%.2f', pct_num) || '%' AS pct
FROM calc
ORDER BY ano_pesquisa, pct_num DESC;

-- diversidade por cargo (2025) — onde a participação feminina é maior/menor
WITH calc AS (
    SELECT coalesce(cargo_atual, 'Não Informado') AS cargo,
           coalesce(genero, 'Não Informado') AS genero,
           total,
           total * 100.0 / SUM(total) OVER (PARTITION BY cargo_atual) AS pct_num
    FROM genero_por_cargo
    WHERE ano_pesquisa = 2025
)
SELECT cargo,
       genero,
       total,
       format('%.2f', pct_num) || '%' AS pct
FROM calc
ORDER BY cargo, pct_num DESC;


-- 4) Quais tecnologias apresentam maior adoção entre os profissionais?
WITH calc AS (
    SELECT ano_pesquisa,
           coalesce(tecnologia, 'Não Informado') AS tecnologia,
           total,
           total * 100.0 / SUM(total) OVER (PARTITION BY ano_pesquisa) AS pct_num
    FROM tecnologias_por_ano
)
SELECT ano_pesquisa,
       tecnologia,
       total,
       format('%.2f', pct_num) || '%' AS pct
FROM calc
ORDER BY ano_pesquisa, pct_num DESC;


-- 5) Qual é o índice de adoção de Inteligência Artificial e seu impacto?
-- OBS: exclui quem não respondeu a pergunta do cálculo do percentual, pra bater
-- com os números do relatório executivo (80,5% / 93,5% / 98,0%). A taxa de
-- não-resposta em si (relevante, 29% a 40% dependendo do ano) fica documentada
-- à parte no relatório, não neste percentual.
WITH calc AS (
    SELECT ano_pesquisa,
           usa_ia_flag AS uso_de_ia,
           total,
           total * 100.0 / SUM(total) OVER (PARTITION BY ano_pesquisa) AS pct_num
    FROM adocao_ia_por_ano
    WHERE usa_ia_flag IS NOT NULL
)
SELECT ano_pesquisa,
       uso_de_ia,
       total,
       format('%.2f', pct_num) || '%' AS pct
FROM calc
ORDER BY ano_pesquisa, uso_de_ia;


-- 6) Existem diferenças relevantes entre regiões, senioridades ou modelos de trabalho?
-- distribuição regional
WITH calc AS (
    SELECT ano_pesquisa,
           coalesce(regiao, 'Não Informado') AS regiao,
           total,
           total * 100.0 / SUM(total) OVER (PARTITION BY ano_pesquisa) AS pct_num
    FROM distribuicao_regiao
)
SELECT ano_pesquisa,
       regiao,
       total,
       format('%.2f', pct_num) || '%' AS pct
FROM calc
ORDER BY ano_pesquisa, pct_num DESC;

-- modelo de trabalho, evolução (note a volta do presencial em 2025)
WITH calc AS (
    SELECT ano_pesquisa,
           coalesce(modelo_trabalho, 'Não Informado') AS modelo_trabalho,
           total,
           total * 100.0 / SUM(total) OVER (PARTITION BY ano_pesquisa) AS pct_num
    FROM modelo_trabalho_por_ano
)
SELECT ano_pesquisa,
       modelo_trabalho,
       total,
       format('%.2f', pct_num) || '%' AS pct
FROM calc
ORDER BY ano_pesquisa, pct_num DESC;


-- 7) Oportunidades e desafios para empresas que desejam investir em Dados e IA?
-- Esta pergunta é respondida combinando os achados das queries 1, 3, 5 e 6 no material
-- executivo (não é uma query única — é a síntese estratégica das demais).

-- ============================================================================
-- Nota: a função format('%.2f', valor) é padrão do Presto/Trino (motor do Athena).
-- Se aparecer erro de função não encontrada, confirme que o Workgroup está usando
-- Athena engine version 2 ou 3 (versões antigas podem não suportar 'format').
-- ============================================================================
