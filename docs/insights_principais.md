# Insights Principais — State of Data Brazil (2023, 2024, 2025)
### Extraídos com dado real, validando a lógica que vai para o Glue Job

Base: 14.005 respostas ao todo (5.293 em 2023, 5.217 em 2024, 3.495 em 2025).

## 1. Estrutura do mercado
Em 2025, os 3 cargos mais comuns são: **Analista de Dados (23,95%)**, **Cientista de Dados (16,95%)** e **Engenheiro de Dados (16,07%)** — juntos, mais da metade do mercado. (Percentual calculado sobre quem respondeu a pergunta de cargo.)

## 2. Perfis mais valorizados
Faixa salarial mais comum por senioridade (2025):
- Júnior: R$ 4.001 a R$ 6.000/mês
- Pleno: R$ 8.001 a R$ 12.000/mês
- Sênior: R$ 8.001 a R$ 12.000/mês
- **Especialista/Staff+** (categoria nova em 2025): R$ 12.001 a R$ 16.000/mês

O mercado amadureceu a ponto de criar um novo nível acima de Sênior — sinal de que empresas estão formalizando trilhas de especialista técnico, não só gestão.

## 3. Diversidade de gênero
A participação feminina caiu no saldo entre 2023 e 2025, mas não de forma estritamente linear: **23,37% (2023) → 23,48% (2024) → 21,75% (2025)**. Houve uma leve estabilidade entre 2023 e 2024 (variação dentro da margem de ruído), seguida de uma queda real e maior em 2025. O saldo do período (-1,6 p.p. em 2 anos) ainda é uma tendência que merece atenção — não é um problema resolvido — mas a queda não foi consistente ano a ano como uma primeira leitura poderia sugerir.

*(Números confirmados na execução real do pipeline no AWS via Athena — ligeiramente diferentes de uma validação preliminar feita antes da execução, que não aplicava o mesmo filtro de qualidade de dados usado no Glue Job.)*

## 4. Tecnologias com maior adoção — achado real (2025)
**Python (55,2%)** e **SQL (50,5%)** dominam disparado como linguagens do dia a dia — mais da metade dos profissionais usa cada uma. R vem bem atrás (9,4%), e todo o resto (Scala, C/C++/C#, Rust, Julia) fica abaixo de 2%. O mercado brasileiro de dados é, na prática, bilíngue: Python + SQL, sem disputa relevante de um terceiro competidor.

## 5. Adoção de Inteligência Artificial — o achado mais forte da base
Disparada na adoção de IA generativa no trabalho (percentual entre quem respondeu à pergunta):
- 2023: 80,49% já usavam alguma solução
- 2024: 93,53%
- **2025: 98,01%** — só 1,99% dos profissionais não usam nenhuma ferramenta de IA no dia a dia

Em 2 anos, o "não uso IA" praticamente desapareceu do mercado (de 19,51% para 1,99%). *(Números confirmados na execução real do Athena.)*

## 6. Diferenças regionais
Concentração forte no Sudeste: **64,4%** dos profissionais de dados estão lá. Sul vem em segundo (16%), e o Norte tem apenas **1,4%** — uma disparidade regional que vale destacar nas recomendações estratégicas.

## 7. Modelo de trabalho — uma reversão de tendência
O modelo 100% presencial **cresceu** de 16,3% (2024) para **20,8% (2025)** — contrário à narrativa de "home office definitivo" que dominou os anos anteriores. Vale investigar se isso reflete políticas de retorno ao escritório das grandes empresas.

## 8. Oportunidades e desafios (síntese)
- **Oportunidade**: com 98% de adoção de IA, empresas que não capacitarem seus times em ferramentas de IA generativa ficam para trás rapidamente.
- **Desafio**: concentração regional extrema — empresas fora do Sudeste competem por um pool de talento muito menor.
- **Desafio**: diversidade de gênero estagnada/piorando — não é um problema resolvido, é uma tendência ativa que precisa de ação.
- **Oportunidade**: a criação do nível Especialista/Staff+ mostra espaço para trilhas técnicas sênior, atrativo para reter talento sem forçar caminho de gestão.

---
*Números confirmados na execução real do pipeline no AWS (Athena), com pequenos ajustes de precisão em relação à validação preliminar local — ver nota metodológica na Seção 3 sobre o efeito do filtro de qualidade de dados na diversidade de gênero.*
