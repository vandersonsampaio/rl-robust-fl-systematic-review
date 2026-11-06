# Análise de sensibilidade: QP2 e qualidade

Gerado por `scripts/sensibilidade.py`. Cada cenário altera só os itens indicados; o resto segue a classificação final do R1.

## QP2: contagens centrais por cenário

| cenário | sem comparação | com comparação | referência forte | mesmo sinal | mesmo sinal com ≥3 sementes e variab. | teste na comparação | comparações mais próximas | empates | sem resultado classificado |
|---|---|---|---|---|---|---|---|---|---|
| S0. Classificação final do R1 (paper) | 32 | 45 | 23 | 6 | 1 | 0 | 14 | 6 | 0 |
| F1. V2-1102 e V2-0973: limiar estático 0,5 tratado como ação fixa | 32 | 45 | 23 | 4 | 1 | 0 | 14 | 6 | 0 |
| F2. V2-3243: trimmed mean sobre os mesmos sinais tratado como heurística do mesmo sinal | 32 | 45 | 24 | 7 | 2 | 0 | 15 | 6 | 0 |
| F3. V2-4059 e V2-0835: heurísticas tratadas como do mesmo sinal | 32 | 45 | 23 | 8 | 2 | 0 | 16 | 6 | 2 |
| F4. Pow-d (V2-0542, 1140, 1199, 3215) não conta como heurística (fica a aleatória) | 32 | 45 | 19 | 6 | 1 | 0 | 14 | 6 | 0 |
| F5. Definição ampla: agregadores externos contam como política não aprendida (grupo C do A14) | 24 | 53 | 31 | 6 | 1 | 0 | 22 | 6 | 8 |
| F6. Comparações rejeitadas na reconciliação aceitas (V2-0922, V2-1229) | 30 | 47 | 23 | 6 | 1 | 0 | 14 | 6 | 0 |
| O1. Vitórias estreitas (≤ ~6 p.p., sem variabilidade) tratadas como empate | 32 | 45 | 23 | 6 | 1 | 0 | 14 | 10 | 0 |
| O2. Empates em que alguma métrica favorece o agente tratados como vitória | 32 | 45 | 23 | 6 | 1 | 0 | 14 | 3 | 0 |
| R2. Categorias e resultados do R2 (livro v2) antes do consenso | 39 | 38 | 17 | 6 | 1 | 0 | 13 | 3 | 0 |
| X1. Mais favorável ao aprendizado (F2 + F3 + O2) | 32 | 45 | 24 | 9 | 3 | 0 | 17 | 3 | 2 |
| X2. Menos favorável ao aprendizado (F1 + O1) | 32 | 45 | 23 | 4 | 1 | 0 | 14 | 10 | 0 |

## QP2: as conclusões se mantêm?

| cenário | A | B | C | D | E |
|---|---|---|---|---|---|
| S0. Classificação final do R1 (paper) | sim | sim | sim | sim | sim |
| F1. V2-1102 e V2-0973: limiar estático 0,5 tratado como ação fixa | sim | sim | sim | sim | sim |
| F2. V2-3243: trimmed mean sobre os mesmos sinais tratado como heurística do mesmo sinal | sim | sim | sim | sim | sim |
| F3. V2-4059 e V2-0835: heurísticas tratadas como do mesmo sinal | sim | sim | sim | sim | sim |
| F4. Pow-d (V2-0542, 1140, 1199, 3215) não conta como heurística (fica a aleatória) | sim | sim | sim | sim | sim |
| F5. Definição ampla: agregadores externos contam como política não aprendida (grupo C do A14) | sim | sim | sim | sim | sim |
| F6. Comparações rejeitadas na reconciliação aceitas (V2-0922, V2-1229) | sim | sim | sim | sim | sim |
| O1. Vitórias estreitas (≤ ~6 p.p., sem variabilidade) tratadas como empate | sim | sim | sim | sim | sim |
| O2. Empates em que alguma métrica favorece o agente tratados como vitória | sim | sim | sim | sim | sim |
| R2. Categorias e resultados do R2 (livro v2) antes do consenso | sim | sim | sim | sim | sim |
| X1. Mais favorável ao aprendizado (F2 + F3 + O2) | sim | sim | sim | sim | sim |
| X2. Menos favorável ao aprendizado (F1 + O1) | sim | sim | sim | sim | sim |

- **A. a maioria não compara com heurística do mesmo sinal**
- **B. menos de 1/4 dos estudos usa heurística do mesmo sinal**
- **C. nenhuma comparação com o mesmo sinal tem teste estatístico**
- **D. há empates entre as comparações mais próximas**
- **E. menos de 10% dos estudos comparam com o mesmo sinal usando ≥3 sementes e variabilidade**

## Qualidade

| cenário | média | mediana | ≥ 5 pontos | QA2 = S (≥3 sementes) | QA3 = S (teste) | QA1 = N (usa teste) |
|---|---|---|---|---|---|---|
| Q0. Pontuação final do R1 (paper) | 2.97 | 3.0 | 8 | 13 | 7 | 19 |
| Q1. Pontuação do R2 (livro v2) nos 26 estudos da amostra, antes do consenso | 3.08 | 3.0 | 10 | 13 | 6 | 17 |
| Q2. Convenção generosa: "não documentado" vale 0,5 em QA2, QA3, QA7 e QA9 | 4.18 | 4.0 | 20 | 13 | 7 | 19 |

Q2 é um limite superior: trata como parcialmente atendido tudo o que o artigo não documenta.
