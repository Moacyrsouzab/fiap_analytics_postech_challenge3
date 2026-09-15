# Mapeamento de Schema — State of Data Brazil (2023-2024, 2024-2025, 2025-2026)

## Padrão geral encontrado

- **2023**: cabeçalho vem como string de tupla Python, ex: `('P2_f ', 'Cargo Atual')` — precisa parsear o código (`P2_f`) e a descrição separadamente.
- **2024 e 2025**: já usam convenção `codigo_descricao_em_snake_case`, ex: `2.f_cargo_atual`. Muito mais fácil de trabalhar.
- **Atenção:** mesmo entre 2024 e 2025, alguns **códigos de pergunta mudaram de número** porque perguntas foram adicionadas/removidas de um ano pro outro (ex: a pergunta sobre layoff existia em 2023/2024 e não existe em 2025, empurrando os códigos seguintes uma letra pra trás). **Não dá pra padronizar só pelo código — é preciso mapear pela descrição/tema da pergunta.**

## Regra de padronização para o Glue Job (2023 → padrão 2024/2025)

Para o arquivo de 2023, extrair de cada cabeçalho `('CODIGO ', 'DESCRICAO')`:
1. `CODIGO.strip()` → converter para minúsculo e trocar `_` por `.` a partir do segundo caractere (ex: `P2_f` → `2.f`)
2. `DESCRICAO` → normalizar para snake_case (minúsculo, sem acento, espaços viram `_`)
3. Resultado final: `2.f_cargo_atual` (mesmo padrão de 2024/2025)

## Colunas-chave já mapeadas (suficientes para as 7 perguntas de negócio)

| Tema | 2023 | 2024 | 2025 |
|---|---|---|---|
| ID / token | `('P0', 'id')` | `0.a_token` | `0.a_token` |
| Data de envio | *(não presente)* | `0.d_data/hora_envio` | `0.d_data/hora_envio` |
| Idade | `('P1_a ', 'Idade')` | `1.a_idade` | `1.a_idade` |
| Faixa de idade | `('P1_a_1 ', 'Faixa idade')` | `1.a.1_faixa_idade` | `1.a.1_faixa_idade` |
| Gênero | `('P1_b ', 'Genero')` | `1.b_genero` | `1.b_genero` |
| Cor/raça/etnia | `('P1_c ', 'Cor/raca/etnia')` | `1.c_cor/raca/etnia` | `1.c_cor/raca/etnia` |
| PCD | `('P1_d ', 'PCD')` | `1.d_pcd` | `1.d_pcd` |
| UF onde mora | `('P1_i_1 ', 'uf onde mora')` | `1.i.1_uf_onde_mora` | `1.i.1_uf_onde_mora` |
| Região onde mora | `('P1_i_2 ', 'Regiao onde mora')` | `1.i.2_regiao_onde_mora` | `1.i.2_regiao_onde_mora` |
| Nível de ensino | `('P1_l ', 'Nivel de Ensino')` | `1.l_nivel_de_ensino` | `1.l_nivel_de_ensino` |
| Cargo atual | `('P2_f ', 'Cargo Atual')` | `2.f_cargo_atual` | `2.f_cargo_atual` |
| Senioridade (nível) | `('P2_g ', 'Nivel')` | `2.g_nivel` | `2.g_nivel` |
| Faixa salarial | `('P2_h ', 'Faixa salarial')` | `2.h_faixa_salarial` | `2.h_faixa_salarial` |
| **Modelo de trabalho atual** | `('P2_r ', 'Atualmente qual a sua forma de trabalho?')` | `2.r_modelo_de_trabalho_atual` | `2.q_modelo_de_trabalho_atual` ⚠️ código mudou |
| Cargos no time de dados | `('P3_b ', '...')` | `3.b_cargos_no_time_de_dados_da_empresa` | `3.b_cargos_no_time_de_dados_da_empresa` |
| Linguagem mais usada | `('P4_d_1 ', 'SQL')` / `('P4_d_3 ', 'Python')` | `4.d_linguagem_de_programacao_(dia_a_dia)` | `4.c_linguagem_preferida` ⚠️ código mudou |
| Usa ChatGPT/Copilot no trabalho | `('P4_m ', 'Utiliza ChatGPT ou LLMs no trabalho?')` | `4.m_usa_chatgpt_ou_copilot_no_trabalho?` | `4.j_usa_chatgpt_ou_copilot_no_trabalho?` ⚠️ código mudou |

⚠️ = confirma que a padronização **precisa ser feita por nome/tema da pergunta, não por código de posição** — o mesmo tema muda de número de ano pra ano.

## O que ainda falta mapear

Essa tabela cobre as colunas essenciais para as 7 perguntas do desafio. Cada pesquisa tem 388 a 403 colunas no total (muitas são sub-perguntas tipo checkbox — ex: cada tecnologia/ferramenta é uma coluna binária própria). Não é necessário nem recomendado mapear as 400 colunas uma a uma — o pipeline deve:
1. Padronizar as colunas-chave acima (perfil, cargo, senioridade, salário, região, uso de IA) → essas viram a base da camada Silver
2. Para os blocos de tecnologias/ferramentas (múltiplas colunas binárias por pergunta), manter o prefixo comum (`4.d.*`, `4.g.*` etc.) e tratar como grupo, sem precisar renomear individualmente cada tecnologia

## Aprendizados da execução real no AWS (pós-implementação)

Depois de rodar o pipeline de ponta a ponta no AWS Academy Lab, dois pontos que não eram óbvios na fase de mapeamento local:

1. **O filtro de qualidade `dropna(how='all', subset=['cargo_atual','senioridade','faixa_salarial'])`, usado no Glue Job para limpar linhas totalmente vazias, tem um efeito colateral nas tabelas puramente demográficas.** Ele remove ~10% dos respondentes por ano (gente que não preencheu nenhuma das 3 perguntas profissionais) — o que é correto para as tabelas de cargo/senioridade/salário, mas reduz sem necessidade a base usada em `genero_por_ano`, `distribuicao_regiao` e `modelo_trabalho_por_ano`, que deveriam considerar todo mundo que respondeu a pergunta demográfica em si, independente de ter respondido sobre emprego. Na prática, o efeito foi pequeno (~1 ponto percentual na maioria dos casos, mas mudou a leitura da tendência de gênero — ver `insights_principais.md`).

---
*Mapeamento gerado a partir da inspeção real dos 3 arquivos enviados (colunas + datas de coleta), com aprendizados adicionados após a execução real no AWS.*
