# Conferência do revisor 2: etapa 2, QP2 e qualidade

**Data:** 2026-10-13

**Fonte:** `triagem_v2/revisor2/validacao_cega_revisor2_v4.xlsx`, versão final com 4 abas. Os CSVs da pasta são idênticos a ela.

**Comparado com:**
- `etapa2_lote2.csv` e `etapa2_arxiv.csv` (decisões do revisor 1 no texto completo);
- `extracao_principal.csv` (QP2, já conciliada com o fichamento do revisor 1);
- `qualidade.csv`.

## Resultado

| conferência (protocolo) | n | concordância | κ | padrão |
|---|---|---|---|---|
| A. Exclusões da etapa 2 (§8.8) | 36 | 15/36 (42%) | — | R2 marca **I** em 16 exclusões do R1 |
| B. 20% das inclusões (§8.8) | 16 | 14/16 (88%) | — | R2 exclui V2-1041 (E-IC3) e V2-1483 (E-IC2) |
| C. 20% da qualidade (§10) | 16 × 9 | 43% | 0,15 | R2 pontua acima em quase todos os critérios (QA6 = S em 16/16; QA5 e QA7 mais altos) |
| D. QP2 (os 52 com comparação) | 52 | — | — | R2: "agente vence" em 51/52 e "discutido como achado" em 50/52 |

## Revisor não possuía acesso ao texto completo

Nesta conferência, o revisor 2 não possuía acesso ao texto completo dos estudos. As decisões e os códigos acima foram registrados a partir do título e do resumo, e em V2-1215, V2-1239 e SB-03 o revisor 2 anotou "PDF ausente".

## Consequência

Pelo §8.8, a conferência das exclusões e de 20% das inclusões é feita na **etapa 2 (texto completo)**, e pelo §10 a avaliação da qualidade exige o texto completo. As divergências foram discutidas com o revisor 2 com os textos completos disponíveis, e o resultado está na seção "Consenso (2026-10-13)". A concordância reportada é a obtida **antes** do consenso.

## V2-1031 e V2-0083 (consenso D da etapa 1)

As decisões propostas foram conferidas no texto completo e se confirmam:

| estudo | decisão | evidência |
|---|---|---|
| **V2-1031** | **E-EC1** | o agente RDPG é o atacante (a recompensa é reduzir os cliques); a defesa é um detector GRU federado com pesos de atenção por camada e ruído de DP, sem RL |
| **V2-0083** | **E-IC3** | a implementação (5 clientes, MNIST, 1 cliente com label flipping) só tem top-k por cosseno + quarentena; o "RL-based response agent" é descrito, sem algoritmo, estado, recompensa nem avaliação |

**Efeito no PRISMA, se registradas:**
- textos completos buscados: 122 → **124**;
- excluídos na etapa 2: 42 → **44** (EC1 +1, IC3 +1);
- incluídos: **78** (sem mudança).

## Consenso (2026-10-13)

Depois da conversa com o autor, o revisor 2 aceitou as decisões do revisor 1 em todos os itens. Antes disso, ele já tinha revisto V2-1215 (E-EC2) e V2-1239 (E-IC3) com o PDF. O registro item a item está em `triagem_v2/revisor2/consenso_etapa2.csv`, e o adendo A16 documenta o processo.

**Concordância antes do consenso**, que é a que se reporta:

| conferência | n | concordância | κ | PABAK |
|---|---|---|---|---|
| inclusão/exclusão | 52 | 65,4% | 0,35 | 0,31 |
| QP2, categoria da comparação | 52 | 34,6% | 0,14 | — |
| qualidade | 16 × 9 | 43% | 0,15 | — |

**Resultado:** o corpus não muda (78 estudos), e V2-1041 e V2-1483 continuam incluídos.
