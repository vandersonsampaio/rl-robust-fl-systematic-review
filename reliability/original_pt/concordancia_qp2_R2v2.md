# Concordância R1 × R2 na QP2: reclassificação cega (livro de códigos v2)

Gerado por `scripts/concordancia_qp2_R2v2.py`. R1 = extração antes do consenso (`extracao_principal_R1_antes_A20.csv`); R2 = `planilha_cega_R2_QP2.xlsx`, antes de qualquer consenso. O subtipo "não defender" do R2 conta como ação fixa, como no livro que ele recebeu. O "?" fica fora do κ.

**Integridade:** 52 estudos; categoria vazia = 0; "?" na categoria = 1; "não defender" = 7.

## Categoria da referência mais forte

| agregação | n | concordância | κ |
|---|---|---|---|
| 7 categorias | 51 | 30/51 (58,8%) | 0,49 |
| referência forte (mesmo sinal, oráculo, fixa, outro sinal) × fraca | 51 | 35/51 (68,6%) | 0,39 |
| com × sem comparação não aprendida | 51 | 44/51 (86,3%) | 0,00 |
| 7 categorias, só "amostra anterior" | 12 | 6/12 (50,0%) | 0,36 |
| 7 categorias, só "nova" | 4 | 4/4 (100,0%) | 1,00 |
| 7 categorias, só "só QP2" | 35 | 20/35 (57,1%) | 0,47 |
| *referência: rodada anterior (A16), mesmos estudos* | 52 | 18/52 (34,6%) | 0,14 |

*Depois do consenso (A20–A22; só como referência, não é a concordância reportada): R1 atual × R2 com "não defender" = nenhuma:* 35/51, κ = 0,61.

### Matriz (linhas R1, colunas R2)

| R1 \ R2 | mesmo sinal | oráculo | ação fixa | outro sinal | aleatória | ablação parcial | nenhuma | ? | total |
|---|---|---|---|---|---|---|---|---|---|
| mesmo sinal | 6 | · | · | · | · | 1 | · | · | 7 |
| oráculo | · | 2 | 1 | · | 1 | · | · | · | 4 |
| ação fixa | · | · | 8 | · | 2 | 1 | 4 | 1 | 16 |
| outro sinal | · | · | 1 | 2 | 3 | · | 1 | · | 7 |
| aleatória | · | · | 3 | · | 10 | · | 1 | · | 14 |
| ablação parcial | · | · | · | · | 1 | 2 | 1 | · | 4 |
| nenhuma | · | · | · | · | · | · | · | · | 0 |
| total | 6 | 2 | 13 | 2 | 17 | 4 | 7 | 1 | 52 |

### Divergências

| estudo | origem | R1 | R2 (texto) |
|---|---|---|---|
| V2-0111 | só QP2 | oráculo | ação fixa |
| V2-0350 | amostra anterior | ação fixa | nenhuma |
| V2-0391 | amostra anterior | aleatória | ação fixa (não defender) |
| V2-0542 | só QP2 | outro sinal | aleatória |
| V2-0634 | só QP2 | aleatória | nenhuma |
| V2-0835 | amostra anterior | outro sinal | ação fixa |
| V2-0837 | só QP2 | ação fixa | aleatória |
| V2-1120 | só QP2 | ação fixa | nenhuma |
| V2-1130 | só QP2 | ação fixa | ? |
| V2-1179 | só QP2 | ação fixa | aleatória |
| V2-1199 | só QP2 | outro sinal | aleatória |
| V2-1450 | só QP2 | aleatória | ação fixa (não defender) |
| V2-2188 | só QP2 | outro sinal | nenhuma |
| V2-2573 | amostra anterior | ação fixa | nenhuma |
| V2-2890 | só QP2 | ablação parcial | nenhuma |
| V2-3215 | só QP2 | outro sinal | aleatória |
| V2-3243 | amostra anterior | ação fixa | ablação parcial |
| V2-3331 | só QP2 | mesmo sinal | ablação parcial |
| V2-4233 | só QP2 | ablação parcial | aleatória |
| V2-4266 | amostra anterior | oráculo | aleatória |
| V2-4727 | só QP2 | aleatória | ação fixa (não defender) |
| V2-4812 | só QP2 | ação fixa | nenhuma |

## Resultado da comparação

O R1 só classificou o resultado das comparações mais próximas (15 estudos antes do A20). Destes, 12 têm resultado do R2 e 9 têm também a mesma categoria nos dois revisores.

| conjunto | n | concordância | κ |
|---|---|---|---|
| resultado, todos com resultado nos dois | 12 | 5/12 (41,7%) | 0,15 |
| resultado, mesma categoria | 9 | 4/9 (44,4%) | 0,20 |
| empate × vitória, mesma categoria | 9 | 5/9 (55,6%) | 0,05 |

| estudo | categoria R1 | categoria R2 | R1 | R2 | métrica principal (R2) |
|---|---|---|---|---|---|
| V2-0351 | mesmo sinal | mesmo sinal | clara | estreita | Taxa de Erro (Error rate – $Err$) |
| V2-1102 | mesmo sinal | mesmo sinal | empate | estreita | Acurácia do Modelo Global (FL Global Model Accuracy) |
| V2-1120 | ação fixa | nenhuma | estreita | — |  |
| V2-1130 | ação fixa | ? | clara (A20) | clara | CJR / Overhead de Computação (para AL) ou Global Model Accuracy (para  |
| V2-1179 | ação fixa | aleatória | empate | estreita | Test Accuracy (Acurácia de classificação do modelo global ao longo das |
| V2-1327 | ação fixa | ação fixa | empate | clara | Acurácia de Teste do Modelo Global |
| V2-2103 | mesmo sinal | mesmo sinal | empate | clara | Det-F1 post-attack |
| V2-2573 | ação fixa | nenhuma | clara | — |  |
| V2-3331 | mesmo sinal | ablação parcial | estreita | clara | Tempo de Treinamento (Time in ms) e Acurácia de Teste (Test Accuracy) |
| V2-4540 | mesmo sinal | mesmo sinal | clara | empate | Acurácia do modelo global (Global model accuracy) ao longo das rodadas |
| V2-4812 | ação fixa | nenhuma | clara | — |  |
| SB-03 | mesmo sinal | mesmo sinal | estreita | estreita | Acurácia de Teste |
| V2-0160 | ação fixa | ação fixa | clara | clara | ASR (Attack Success Rate / Taxa de Sucesso do Ataque) | Accuracy (Acur |
| V2-0350 | ação fixa | nenhuma | empate (A20) | — |  |
| V2-0973 | mesmo sinal | mesmo sinal | estreita | estreita | Acurácia Média do Modelo Global (Average Accuracy) |
| V2-3243 | ação fixa | ablação parcial | clara | clara | Test AUC |
| V2-4789 | ação fixa | ação fixa | empate | empate | Acurácia Final do Modelo Global (%) |

Distribuição do resultado do R2 nos 52: clara 30, estreita 9, — 7, empate 5, ? 1.

## Discutido como achado

| n | concordância | κ | R1 S/P/N | R2 S/P/N |
|---|---|---|---|---|
| 51 | 11/51 (21,6%) | 0,00 | 7/4/40 | 44/1/6 |

## Variabilidade e teste estatístico na própria comparação

O R1 não registrou esses dois campos por comparação (só o de sementes do estudo e, no caso do mesmo sinal, o QA2). R2, variabilidade: N 31, S 13, — 7, ? 1. R2, teste: N 44, — 7, S 1 (V2-4059).

## Coerência interna do R2: QA5 × categoria da QP2

11 de 16 estudos coerentes. Divergências:

| estudo | categoria R2 | QA5 esperado | QA5 do R2 |
|---|---|---|---|
| V2-0350 | nenhuma | N | S |
| V2-1261 | aleatória | P | S |
| V2-2573 | nenhuma | N | S |
| V2-3243 | ablação parcial | P | S |
| V2-4266 | aleatória | P | S |
