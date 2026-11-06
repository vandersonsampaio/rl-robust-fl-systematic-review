# Concordância R1 × R2 na qualidade: reclassificação cega (livro de códigos v2)

Gerado por `scripts/concordancia_qualidade_R2v2.py`. R1 = pontuação existente antes do consenso (`qualidade_R1_antes_A20.csv`); R2 = `planilha_cega_R2_Qualidade.xlsx`, antes de qualquer consenso. O "?" do R2 fica fora do κ do critério; o cenário "? = P" está na última coluna.

**Integridade:** 26 estudos, 234 decisões; células vazias = 0; decisões sem "onde" = 0; "?" = 11.

## Resultado geral

| conjunto | n decisões | concordância | κ | κ ponderado | κ com "? = P" |
|---|---|---|---|---|---|
| todos os 26 estudos | 223 | 79,4% | 0,67 | 0,72 | 0,66 |
| os 16 da amostra anterior | 140 | 77,9% | 0,65 | 0,72 | 0,63 |
| os 10 novos | 83 | 81,9% | 0,70 | 0,72 | 0,70 |
| *referência: rodada anterior (A16), mesmos 16* | 144 | 43,1% | 0,15 | 0,27 | — |

## Por critério

| critério | concordância | κ | κ ponderado | R1 S/P/N | R2 S/P/N/? | R2 acima | R2 abaixo |
|---|---|---|---|---|---|---|---|
| QA1. recompensa sem teste | 20/23 (87%) | 0,76 | 0,84 | 17/3/6 | 14/5/4/3 | 2 | 1 |
| QA2. ≥3 sementes + variab. | 24/26 (92%) | 0,85 | 0,90 | 5/4/17 | 5/4/17/0 | 1 | 1 |
| QA3. teste estatístico | 25/26 (96%) | 0,78 | 0,78 | 3/0/23 | 2/0/24/0 | 0 | 1 |
| QA4. código | 26/26 (100%) | 1,00 | 1,00 | 5/0/21 | 5/0/21/0 | 0 | 0 |
| QA5. política não aprendida | 13/24 (54%) | 0,31 | 0,18 | 8/8/10 | 18/6/0/2 | 11 | 0 |
| QA6. ataques fiéis | 15/22 (68%) | 0,03 | -0,07 | 1/24/1 | 3/16/3/4 | 4 | 3 |
| QA7. hiperparâm. do agente | 11/25 (44%) | 0,07 | 0,08 | 16/9/1 | 4/21/0/1 | 2 | 12 |
| QA8. defesas fortes | 23/26 (88%) | 0,78 | 0,84 | 4/5/17 | 4/6/16/0 | 2 | 1 |
| QA9. ataque adaptativo | 20/25 (80%) | 0,45 | 0,53 | 1/7/18 | 1/3/21/1 | 1 | 4 |

*Depois da regra do QA7 do A20 (só como referência, não é a concordância reportada):* geral 81,6%, κ = 0,71; QA7 19/25, κ = 0,38.

## Pontuação total (0–9; "?" = 0,5)

| medida | R1 | R2 |
|---|---|---|
| média | 3,46 | 3,54 |
| mediana | 3,5 | 3,2 |
| ≥ 5 pontos | 4 | 5 |

Diferença R2 − R1: média 0,08, dp 0,72, limites de concordância (Bland-Altman) -1,33 a 1,48; |diferença| ≤ 1 em 23/26; Spearman ρ = 0,86.

| estudo | origem | R1 | R2 | R2 − R1 | critérios divergentes |
|---|---|---|---|---|---|
| V2-2573 | amostra anterior | 4,5 | 3,0 | -1,5 | QA1 (S→?), QA6 (P→N), QA7 (S→P) |
| V2-3243 | amostra anterior | 6,5 | 5,0 | -1,5 | QA3 (S→N), QA7 (S→P) |
| V2-1105 | amostra anterior | 5,0 | 4,0 | -1,0 | QA1 (S→P), QA7 (S→P) |
| V2-0160 | nova | 4,0 | 3,5 | -0,5 | QA6 (P→?), QA9 (P→N) |
| V2-0351 | nova | 3,5 | 3,0 | -0,5 | QA6 (P→?), QA7 (S→?) |
| V2-1483 | amostra anterior | 5,5 | 5,0 | -0,5 | QA7 (S→P) |
| V2-3265 | amostra anterior | 3,5 | 3,0 | -0,5 | QA7 (S→P) |
| V2-0391 | amostra anterior | 3,5 | 3,5 | 0,0 | QA5 (P→S), QA7 (S→P) |
| V2-1041 | amostra anterior | 4,0 | 4,0 | 0,0 | QA1 (S→?), QA5 (N→?), QA6 (P→?), QA7 (S→P), QA8 (N→P) |
| V2-1126 | nova | 3,5 | 3,5 | 0,0 |  |
| V2-1140 | amostra anterior | 2,5 | 2,5 | 0,0 | QA6 (P→N), QA7 (P→S) |
| V2-1229 | nova | 3,0 | 3,0 | 0,0 | QA5 (N→?), QA6 (P→?), QA9 (P→N) |
| V2-3830 | amostra anterior | 2,0 | 2,0 | 0,0 | QA5 (N→S), QA7 (S→P), QA8 (P→N) |
| V2-4266 | amostra anterior | 3,0 | 3,0 | 0,0 |  |
| V2-0350 | amostra anterior | 4,5 | 5,0 | 0,5 | QA6 (P→S) |
| V2-0506 | nova | 2,5 | 3,0 | 0,5 | QA5 (N→P) |
| V2-0835 | amostra anterior | 2,0 | 2,5 | 0,5 | QA1 (N→P), QA5 (P→S), QA7 (S→P) |
| V2-1102 | nova | 3,0 | 3,5 | 0,5 | QA6 (P→S) |
| V2-1231 | nova | 5,0 | 5,5 | 0,5 | QA5 (N→S), QA9 (S→P) |
| V2-1254 | amostra anterior | 3,5 | 4,0 | 0,5 | QA2 (P→N), QA5 (N→S) |
| V2-1294 | nova | 2,5 | 3,0 | 0,5 | QA1 (P→?), QA5 (N→S), QA7 (S→P) |
| V2-2891 | nova | 2,5 | 3,0 | 0,5 | QA5 (N→S), QA6 (N→P), QA7 (S→P), QA9 (P→N) |
| V2-4339 | nova | 3,0 | 3,5 | 0,5 | QA5 (N→S), QA6 (S→N), QA7 (N→P), QA9 (P→?) |
| V2-1261 | amostra anterior | 1,5 | 2,5 | 1,0 | QA1 (N→P), QA5 (P→S) |
| V2-1363 | amostra anterior | 1,5 | 2,5 | 1,0 | QA2 (N→P), QA8 (N→P) |
| V2-0987 | amostra anterior | 4,5 | 6,0 | 1,5 | QA5 (N→S), QA6 (P→S), QA7 (S→P), QA9 (P→S) |

## R2: rodada anterior × atual (16 estudos)

O R2 mudou 70 de 144 decisões. Em 55 passou a concordar com o R1; em 8 deixou de concordar.

| critério | mudanças | rumo ao R1 | afastou do R1 |
|---|---|---|---|
| QA1 | 10 | 5 | 3 |
| QA2 | 15 | 13 | 2 |
| QA3 | 2 | 2 | 0 |
| QA4 | 2 | 2 | 0 |
| QA5 | 5 | 4 | 0 |
| QA6 | 14 | 11 | 0 |
| QA7 | 4 | 2 | 1 |
| QA8 | 9 | 8 | 1 |
| QA9 | 9 | 8 | 1 |

## Decisões "?" do R2

| estudo | critério | R1 | onde (R2) |
|---|---|---|---|
| V2-0160 | QA6 | P | Seção EXPERIMENTAL SETUP; Seção THREAT MODEL |
| V2-0351 | QA6 | P | Seção III-B (Equação 1), Seção V-C (Figuras 7, 8b, 10) e Seção VI-B (Figuras 14b, 15, 16c) |
| V2-0351 | QA7 | S | Seção IV-D (Equações 21–24, Algoritmo 2), Seção V-C e Figuras 8, 16 |
| V2-1041 | QA1 | S | Seções VI-A, VI-C, VI-G (Alg. 2), XI-B, XII-A, XII-C (Tabelas VIII, IX, X, XVIII). |
| V2-1041 | QA5 | N | Tabela XII (p. 10031), Seções VI-A (p. 10019), XI-B (p. 10026) e XII-H (p. 10031). |
| V2-1041 | QA6 | P | Seções IV-A, IV-B, XII-A, XII-B, XII-E, Tabelas II, VII, VIII e IX. |
| V2-1229 | QA5 | N | Seções 4.3, 5.2, 6.1 e 6.2, Tabelas 1, 2 e 3 |
| V2-1229 | QA6 | P | Seções 5.3, 5.4 e 6.2, Figura 7 |
| V2-1294 | QA1 | P | eção 3.1.3 (pág. 11:9) e Seção 5 (pág. 11:13) |
| V2-2573 | QA1 | S | Seção 3.1.6, Seção 3.1.8, Seção 3.3, Figuras 2 e 6, Figura 3, Tabela II |
| V2-4339 | QA9 | P | Seção 3.1, 5.1 |
