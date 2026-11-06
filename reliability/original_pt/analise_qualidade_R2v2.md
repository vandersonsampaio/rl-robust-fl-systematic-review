# Reclassificação cega do R2: qualidade (QA1–QA9)

**Data:** 2026-10-19
**Fonte:** `planilha_cega_R2_Qualidade.xlsx`, aba Qualidade, com 26 estudos: os 16 da amostra anterior e 10 novos. A aba QP2 ainda não foi devolvida.
**Números:** `concordancia_qualidade_R2v2.md` e `.csv`, gerados por `scripts/concordancia_qualidade_R2v2.py`. O R1 é a pontuação final de `triagem_v2/qualidade.csv`.

## Integridade

As 234 decisões estão preenchidas e todas têm a coluna "onde". O R2 usou "?" em 11 delas, sempre com nota que explica as duas leituras, como pede o livro de códigos. Desta vez não há sinal de leitura só do resumo, porque as remissões citam seção, tabela, equação e página.

## Resultado

| conjunto | concordância | κ | κ ponderado |
|---|---|---|---|
| 26 estudos (223 decisões sem "?") | 79,4% | **0,67** | 0,72 |
| os 16 da amostra anterior | 77,9% | 0,65 | 0,72 |
| os 10 novos | 81,9% | 0,70 | 0,72 |
| rodada anterior (A16), mesmos 16 | 43,1% | 0,15 | 0,27 |

Tratar o "?" como P praticamente não muda nada (κ = 0,66). A concordância passa de fraca para substancial. Nos 16 estudos repetidos, o R2 mudou 70 das 144 decisões: 55 passaram a coincidir com o R1 e 8 deixaram de coincidir. A melhora aparece também nos 10 estudos novos, que o R2 nunca tinha visto, e por isso não se explica por memória da conversa de consenso.

A pontuação total quase não muda. A média é 3,46 no R1 e 3,54 no R2, com ρ de Spearman = 0,86. Em 23 dos 26 estudos a diferença fica dentro de 1 ponto, e os limites de Bland-Altman vão de −1,3 a +1,5. As divergências por critério se compensam, porque o R2 dá mais pontos no QA5 e menos no QA7.

## Por critério

| critério | κ | leitura |
|---|---|---|
| QA1, QA2, QA3, QA4, QA8 | 0,76 a 1,00 | concordância alta. São os critérios factuais |
| QA9 | 0,45 | o R2 é mais rigoroso, com 4 P do R1 rebaixados para N |
| **QA5** | 0,31 | o R2 dá S onde o R1 deu N (11 acima, 0 abaixo) |
| **QA6** | 0,03 | κ baixo por prevalência. O R1 deu P em 24 dos 26 estudos, e a concordância bruta é de 68% |
| **QA7** | 0,07 | o R2 é mais rigoroso, com 12 S do R1 rebaixados para P |

### QA7: a regra do R1 é mais branda que o livro de códigos

O R1 derivou o QA7 por regra no `scripts/etapa2_lote2.py`. Basta uma palavra-chave no campo `orcamento` ("episódios", "ε", "passos", "lr") para o critério virar S. O livro de códigos, porém, pede parâmetros suficientes para calcular o orçamento e reserva o P para "só alguns parâmetros". Em parte dos casos, o R2 aplicou o texto do livro e o R1 não:

| estudo | o que o R1 tem em `orcamento` | leitura pelo livro |
|---|---|---|
| V2-0391 | ~3600 episódios | P (R2) |
| V2-3265 | 200–1300 episódios | P (R2) |
| V2-0351 | ~1500 episódios, ε com decaimento | P (o R2 deu "?") |
| V2-2573 | 12 rodadas = ~12 passos de PPO | P (R2) |
| V2-1105 | ε = 0,3, rede-alvo a cada C rodadas | P (R2) |
| V2-1483 | T de 50 a 200 rodadas, ε de 0,25 a 0,05 | P (R2) |
| V2-0987 | 50 rodadas, RL a cada 5ª, ε com decaimento | P (R2) |
| V2-2891 | 8.000 a 25.000 passos do RL | P (R2) |
| V2-0835 | 80 rodadas, lr, γ, batch, ε | S (R1) |
| V2-3830 | 1.000 passos, lr, replay, rede-alvo, γ | S (R1) |
| V2-3243 | 300 rodadas, lr, γ, pré-treino | S (R1) |
| V2-1041 | ~100 iterações, lr, γ, arquitetura | S (R1) |
| V2-1294 | o próprio R1 anota "hiperparâmetros do agente não reportados" | P (R2) |

A regra do R1 deveria exigir o volume (passos ou episódios) **e** pelo menos um parâmetro de otimização (lr, γ, batch ou replay). O problema não fica restrito à amostra, porque a mesma regra valeu para os 78 estudos. Isso afeta o QA7 = S do paper e o achado sobre orçamento da QP3.

### QA5: a exceção "não defender" está mal resolvida no livro de códigos

Em 9 dos 13 casos de divergência no QA5, o R1 registrou "nenhuma" e o R2 deu S ou "?". Nos textos, a referência que sobra nesses estudos é quase sempre o FedAvg ou a média simples:

- **V2-1254** (o agente define os pesos de agregação), **V2-2891** (seleção + pesos), **V2-1294** (descartar nós; o "Average" não descarta nenhum), **V2-3830** (seleção; o HierFAVG seleciona todos) e **V2-0987**. Nestes, o FedAvg é uma ação do próprio espaço do agente com todos aceitos e pesos fixos. O §2.1 do livro diz que isso **conta como ação fixa**, no subtipo "não defender". O R2 seguiu essa exceção.
- **V2-1231** e **V2-4339**. Os baselines registrados são Krum, mediana, FLTrust e semelhantes, que o livro exclui. Aqui o R2 parece ter contado agregadores externos, como no grupo C do A14.

O livro tem duas frases em tensão. Uma exclui o "FedAvg puro usado como comparação externa", e a outra aceita o "não defender" dentro do espaço de ação. O próprio R1 aplicou a exceção no V2-0351, onde "todos os colaboradores" (FedAvg) conta como fixa, mas não no V2-1254 nem no V2-2891. Isso é inconsistência do R1, não erro do R2.

Há também uma consequência para a QP2. Os estudos "nenhuma" não estão na aba QP2 do R2. Se a exceção valer de forma consistente, parte dos 26 "sem comparação" passa a "fixa (não defender)". A conclusão A da sensibilidade continua de pé, porque "não defender" não é heurística do mesmo sinal. Muda o número que o paper reporta como "sem nenhuma comparação".

### QA6

O R1 deu P em 24 dos 26 estudos. Com uma categoria tão dominante, o κ perde o sentido, e a divergência real são 7 casos espalhados, além de 4 "?". Convém reportar a concordância bruta (68%) junto com o κ e explicar a prevalência.

## O que reportar e o que decidir

**Para o paper e o adendo:** concordância na qualidade antes do consenso de 79,4%, κ = 0,67 e κ ponderado = 0,72 (26 × 9), contra κ = 0,15 na rodada sem livro de códigos. Pontuação total com ρ = 0,86 e diferença média de +0,08.

**Decisões do autor antes do consenso com o R2:**
1. **QA7.** Endurecer a regra conforme o livro e repontuar os 78 estudos. Isso exige rodar de novo a síntese e a sensibilidade. A alternativa é manter a regra e reescrever o critério S do livro para "algum parâmetro do agente" (não recomendo, porque fica fraco para o orçamento).
2. **QA5 e QP2.** Decidir se o FedAvg dentro do espaço de ação conta como "fixa (não defender)". Se contar, revisar os "nenhuma" do R1 com esse critério, começando por V2-1254, V2-2891, V2-1294, V2-3830 e V2-0987.
3. **Os 11 "?"** vão para a reunião de consenso com o PDF aberto.

## Decisões do autor (19/10/2026, adendo A20)

1. **QA7.** A regra foi endurecida no `scripts/etapa2_lote2.py`, e agora o S exige volume e um parâmetro de otimização do agente. A extração do V2-0351 foi completada com λ = 0,2, ζ = 0,85 e ε decrescente da Sec. V-C, que o R2 apontou. Na repontuação dos 78 estudos, 18 passaram de S para P. O QA7 ficou com 22 S, 48 P e 8 N, a média da qualidade caiu de 3,25 para 3,13 e os estudos com ≥ 5 pontos caíram de 12 para 11. A pontuação anterior ficou em `qualidade_R1_antes_A20.csv`, e a concordância reportada continua sendo calculada contra ela.
2. **Referências sem ação defensiva.** O FedAvg, a média simples e aceitar ou selecionar todos não são políticas de defesa. "Não defender" e "não ter ação defensiva" são a mesma coisa, e por isso a categoria é "nenhuma", mesmo dentro do espaço de ação do agente. Com essa regra, V2-1178, V2-0945, V2-1030 e V2-3265 passam a "nenhuma", e V2-0837 e V2-0940 passam a "aleatória". V2-0350 e V2-1130 continuam como fixa e entram nas comparações mais próximas. No V2-0350, o local-only, com λ = 0 fixo, supera o agente em F1 nos três cenários (Tab. 1), e o resultado conta como empate. O `livro_codigos_v2.md` foi revisto, e a cópia enviada ao R2 fica como estava. A extração anterior ao consenso foi guardada em `extracao_principal_R1_antes_A20.csv`, para o κ da QP2.
3. **QA1 dos "?".** Se a recompensa e a seleção não usam nenhum dado de avaliação do modelo, e isso está escrito, o critério é S. O V2-1041 ficou com S, o que o comentário do R2 confirmou. O V2-1294 ficou com P. O V2-2573 passou de S para P e ganhou uma nota sobre o rótulo verdadeiro na recompensa. A média da qualidade ficou em 3,06.
4. **QA6 dos "?".** Avaliam-se os ataques contra os quais a decisão do agente é testada, com a regra registrada no livro de códigos. Os quatro casos ficaram com P, igual ao R1, e a pontuação não mudou.
   - **V2-1041:** o agente só enfrenta o ATTS1, um ataque próprio sem fração nem momento. Os ataques de participante, de que trata a Leitura B do R2, testam outros componentes.
   - **V2-0160:** o LBR segue Yao et al. [9], mas a fração não fica clara ("a malicious client" ou "malicious clients") e a injeção ocorre só "during the first phase".
   - **V2-0351:** o ataque bizantino é genérico (θ arbitrário) e falta a distribuição dos dados falsificados.
   - **V2-1229:** a fração Br é de 20% e varia de 0,1 a 0,48, o LF segue a definição original e o Sybil é descrito. O LIE, porém, usa z = 0,3 fixo, enquanto a regra original daria cerca de 0,35 numa vizinhança de 11 nós com 20% de bizantinos e cerca de 0,47 com os 50 clientes. O momento da ativação também não é declarado.
5. **QA5 do V2-1041 e ablações.** Uma ablação que remove o agente sem pôr no lugar uma decisão defensiva é "nenhuma". O V2-1041 ficou com N, igual ao R1. A Tab. XII só desliga a MTD, e os autores deixam para trabalho futuro a comparação com mutação aleatória, round-robin ou gulosa, como na Leitura B do R2. Revisão das outras ablações parciais: o V2-2890 foi para nenhuma (BlockFL externo), o V2-4233 foi para aleatória (HSFL original com seleção ao acaso), e o V2-1105 e o V2-3555 continuam como parcial. A média da qualidade continua em 3,06.
6. **QA9 do V2-4339.** O critério fica S quando o adversário usa o conhecimento da defesa avaliada para ajustar o ataque contra pelo menos um componente dela. Aqui, ele divide os maliciosos para escapar do ISA. O R1 passou de P para S.

**Fechamento dos 11 "?":** QA1 com S, P e P (V2-1041, V2-1294, V2-2573); QA5 com N no V2-1041 e no V2-1229; QA7 com S no V2-0351; QA6 com P nos quatro casos; QA9 com S (V2-4339). Pontuação do R1 alterada: V2-2573 (QA1, S → P) e V2-4339 (QA9, P → S). A média da qualidade ficou em 3,06.

A QP2 do R2 ainda está pendente. Quando ela chegar, convém conferir se o QA5 do R2 bate com a categoria que ele mesmo der na QP2.
