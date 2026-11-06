# Comparação: fichamento do autor × extração do Claude (S1, QP1–QP6)

**Data:** 2026-10-09
**Fontes:**
- `selecionados/Fechamento - PDF/` (77 fichamentos do autor);
- `triagem_v2/extracao_principal.csv` e `triagem_v2/qualidade.csv` (QA7), da extração do Claude.

**Detalhe por estudo:** `validacao/comparacao_fichamento_por_estudo.tsv`.

**Cobertura:** 77 de 78 estudos. Falta só o V2-3494 (TD3-agg), que o autor não fichou.

## Método

O fichamento do autor é texto livre, organizado pelas QP1–QP6. Para cada estudo, a resposta dele foi convertida nos mesmos códigos que a síntese usa (`cmpcat` e `priv` do `sintese.py`, `analise_horizonte`, `vazamento_teste` etc.) e comparada campo a campo com a extração do Claude.

As divergências que mudariam a síntese foram conferidas no texto dos PDFs (`triagem_v2/txt/`).

A conversão do texto do autor em códigos é uma leitura do Claude. Por isso, os κ abaixo servem para dar uma ordem de grandeza: não são um κ formal entre revisores.

## Resultado geral

| campo | n | concordância | κ | padrão da divergência |
|---|---|---|---|---|
| QP2: categoria da comparação não aprendida | 77 | 52% | 0,41 | o autor encontra mais comparações (detalhe abaixo) |
| QP2: "há alguma comparação não aprendida?" | 77 | 75% | 0,47 | autor 62 × Claude 43 |
| QP2: "há comparação forte (fixa, mesmo sinal, oráculo, outro sinal)?" | 77 | 62% | 0,31 | autor 45 × Claude 16 |
| QP3: modo (online/offline) | 75 | 93% | 0,63 | — |
| QP3: análise do ganho × horizonte | 77 | 42% | 0,00 | autor S em 45 casos em que o Claude marcou N |
| QP3: orçamento reportado (autor × QA7) | 77 | 35% | 0,09 | o autor achou orçamento completo em 42 casos em que o Claude marcou P/N |
| QP5: exigência de dados do sinal | 77 | 64% | 0,47 | o Claude marcou "só updates" onde há validação/teste no servidor (15) |
| QP6: vazamento de teste (casos em que os dois decidiram) | 30 | 90% | 0,79 | o Claude deixou "?" em 25 casos que o autor decidiu (16 N, 9 S) |
| QP6: ataque adaptativo | 77 | 86% | 0,61 | o Claude dá P com mais facilidade (8) |
| QP6: sementes/estatística | 75 | 88% | 0,74 | o Claude marcou N onde há média±dp (7) |
| QP6: código disponível | 77 | 97% | 0,91 | 2 casos em que o código está em material suplementar |

**Leitura:**
- Estamos alinhados no que é factual e binário: modo, código, sementes, ataque adaptativo e vazamento (quando os dois decidem).
- Não estamos alinhados em três pontos:
  1. a **QP2**, que é a questão central;
  2. o critério de **horizonte** na QP3;
  3. a completude do **orçamento** (QP3) e da **privacidade** (QP5).

  Nos três, a causa principal é que a extração do Claude ficou **incompleta**. Em menor grau, há **critérios diferentes**.

## QP2: onde está a divergência (37 estudos)

| grupo | nº | quem tem razão | estudos |
|---|---|---|---|
| A. Mesma evidência, rótulo ou código diferente | 8 | empate; ajustar a codificação | V2-1102 e V2-0973 (limiar estático 0,5: "fixa" × "mesmo sinal"); V2-0111 (há oráculo além das fixas); V2-0940 (o `cmpcat` lê "aleatória + fixa" como "aleatória": bug de ordem); V2-1140, V2-1199 e V2-0542 (Pow-d é heurística de **outro sinal**, mas o `cmpcat` não tem regra para isso); V2-3243 (o Claude tinha "conferir"; o autor resolveu: troca por Trimmed Mean fixo, AUC 0,7765 × 0,7051) |
| B. O autor achou uma comparação que o Claude não registrou | 20 | **autor** | conferidos no texto: V2-1275, V2-2103, V2-3331, V2-4059, V2-0350, V2-1363, V2-3215, V2-0351; plausíveis, não conferidos: V2-0837, V2-1178, V2-0945, V2-1130, V2-4233, V2-0634, V2-0688, V2-1030, V2-3265, V2-1105, V2-0922, V2-1229 |
| C. Critério: o autor conta agregadores robustos, algoritmos de FL ou treino centralizado como "política não aprendida" | 8 | **Claude**, pelo protocolo (ação fixa = ação do próprio agente mantida constante) | V2-1042, V2-1185, V2-0918, V2-1231 (Krum, Median, FedAvg etc. fora do espaço de ação do agente); V2-3175 (treino centralizado é limite superior do modelo, não oráculo da política); V2-1001 (MFL); V2-0530 (não confirmado); V2-1012 (o CBE3 é um bandit, portanto aprendido) |
| D. O autor errou | 1 | **Claude** | V2-4339: "Random sampling A/B" é um exemplo motivacional com filtragem por oráculo, não uma comparação do MAB com heurística de mesmo sinal |

**Comparações com o mesmo sinal encontradas pelo autor e confirmadas no texto:**

| estudo | o que é | resultado |
|---|---|---|
| **V2-2103** (OptiGradTrust) | regra fixa: pesos iguais 1/6 nos 6 sinais + limiar 0,5 (Tab. 14) | F1 de detecção 36,4 × 61,7. **Acurácia final idêntica: 64,35 × 64,32.** Além disso, "sem RL" dá F1 61,11, quase o mesmo do RL. Nenhum de nós registrou o empate em acurácia, que é evidência forte para o Portão N |
| **V2-3331** (LBSFL) | Shapley completo sem bandit | o bandit fica 5–6% acima |
| **V2-4059** (RL-DAA) | AMA: pesos estáticos sobre os mesmos t, q, c | 93,2% × 72,0% com 20% de envenenamento |
| **V2-0351** (CoPLA) | seleção direta por reputação + "todos os colaboradores" (FedAvg, fixa) | o RL vence |
| **V2-1275** | No Unlearning (fixa), Random e **Retrain from scratch** (≈ oráculo) | o DQN **empata** com o oráculo em acurácia |

**Correções no lado do Claude, conferidas no texto:**
- **V2-0835:** a heurística "míope" seleciona os 30% de UAVs com melhor desempenho de computação. É **outro sinal**, não o mesmo; o Claude errou.
- **V2-0350:** Ditto com λ = 0,5 fixo e local-only (λ = 0) são ações fixas do agente-cliente, e há também um oráculo centralizado.

**Impacto na síntese, se o grupo B for aceito:**
- "Sem comparação não aprendida" cai de 34–35 para cerca de 24.
- "Heurística com o mesmo sinal" passa de 5 para cerca de 8: sai o V2-0835 e entram V2-2103, V2-3331, V2-4059 e V2-0351.
- Comparações "fortes" passam de 16 para mais de 30.
- O Portão N **não se inverte**. Os novos casos de mesmo sinal trazem um empate (V2-2103, em acurácia) e três vitórias do agente. Somados ao V2-1275 (DQN ≈ oráculo), o quadro continua "parcialmente mostrado".

### Leitura do resultado: o autor segue a narrativa do artigo, o Claude segue os números

Nos estudos em que a comparação existe e os dois a registraram, o autor tende a repetir a conclusão dos autores do artigo. São justamente os casos de evidência do Portão N:

- **V2-1102:** o autor relata só k = 10 (DDPG 68 × fixo 62). Ele omite o empate com k = 5.
- **V2-1327:** o autor relata que o DRL supera o peso fixo. Com envenenamento, a diferença é de cerca de 1 p.p.; o ganho está só nos rótulos raros.
- **V2-1179:** o autor relata que o DDPG atinge a maior acurácia. Na verdade, ele iguala a melhor φ fixa de cada regime.
- **V2-4789 (FedStrategist):** o autor relata que o agente "protege onde o FedAvg falha". A Tab. 2 mostra FedAvg 39,43 × agente 38,82: **a fixa vence**. Os autores do artigo reinterpretam isso como "custo da segurança". O autor também não registra que o agente escolhe FedAvg em 92–94% das rodadas.
- **V2-4728:** o autor não registra que a recompensa usa rótulos de malicioso ("trust accuracy"), nem que o DQN tem ASR pior que a política aleatória (41 × 36).

**Sugestão:** ao consolidar, use os números das tabelas. A narrativa do artigo não deve decidir.

## QP3

### Horizonte (κ = 0)

O autor marcou S em 45 estudos. Os motivos foram estes:

- curvas de convergência ao longo das rodadas (a maioria);
- análise de sensibilidade de γ (V2-3555, V2-0530, V2-1012);
- limites teóricos de regret ou convergência (V2-0542, V2-1126, V2-1140, V2-1199, V2-4266 e outros);
- horizonte de previsão do modelo (V2-1042: 15, 30 e 45 min). Este caso não tem relação com o aprendizado do agente;
- variação real do número de rodadas T (V2-1483, T ∈ {50…200}; SB-03, T de 50 a 500).

O Claude marcou N em todos os 78, lendo a pergunta como "o ganho **do aprendizado sobre a política não aprendida** varia com o nº de rodadas?".

**É preciso fixar uma definição operacional.** Pela definição estrita, o "0/78" do `slr_resultado.md` provavelmente se sustenta. Ainda assim, convém reescrevê-lo como "nenhum estudo compara agente e política não aprendida em horizontes diferentes" e citar V2-1483 e SB-03 como os que variam T (só para o próprio método).

### Orçamento

O autor extraiu hiperparâmetros do agente em muitos estudos que o Claude marcou como "não reportado". O caso conferido é o V2-1041: ator-crítico, lr 0,005, γ 0,99, três camadas de 256. Nesse caso, o **Claude errou também o algoritmo** (registrou Q-learning).

Outros casos parecidos: V2-1102, V2-0973, V2-0835, V2-3830, V2-1001, V2-1130, V2-1450, V2-0634, V2-1294, V2-0506 e V2-0590.

O QA7, portanto, está subestimado, e a média do QA (2,83) provavelmente também.

## QP5: privacidade

Em 15 estudos, o Claude registrou "só updates" e o autor encontrou validação ou teste no servidor. Em cinco deles, a própria recompensa extraída pelo Claude já citava validação ou teste, o que é uma inconsistência interna: V2-3555, V2-3830, V2-0590, V2-1450 e V2-0351.

Outros casos: V2-1275, V2-0835, V2-0973, V2-1001, V2-0550, V2-3215, V2-0368, V2-2573, V2-1294 (proxy formado com dados brutos dos clientes) e V2-0837 (2.400 amostras no MEC).

A tabela de exigências de dados do `slr_resultado.md` (QP5) precisa ser refeita.

## QP6

- **Vazamento:** quando os dois decidem, a concordância é alta. O problema são os 25 "?" do Claude.
  - O autor marcou **S** em 9 deles, por exemplo V2-0973, V2-1275, V2-0835, V2-1001, V2-1261 e V2-1012.
  - Marcou **N** em 16, em geral porque a recompensa usa a perda de treino local, como em V2-0391, V2-0837, V2-1030 e V2-0065.
  - No V2-2475, o autor tem razão: o conjunto de validação do TBA é sorteado do "global testing pool". O vazamento, porém, está na agregação, não na recompensa do bandit.
- **Sementes:** no V2-1126, a tabela tem média ± dp, então o autor está certo e o Claude errou ao marcar N.
- **Código:** a divergência é de critério. Para o autor, material suplementar do IEEE conta como código disponível; para o Claude, não (V2-1057 e V2-0688). É preciso uniformizar.

## QP1: erros factuais do Claude conferidos

- V2-1041: o algoritmo é **ator-crítico**, não Q-learning.
- V2-0590: o algoritmo é **TD3**, não DDPG.
- Em V2-1103, V2-1294, V2-1229 e V2-3265, o Claude deixou estado, recompensa ou sinal como "?". O autor preencheu esses campos.
- V2-1483: o número da variante "sem HRL" diverge (autor 91,50 × Claude 92,60). A tabela sai embaralhada na extração do texto, então é preciso conferir no PDF.

## O que o Claude registrou e o autor não

- Rótulos de malicioso usados na recompensa: V2-4728 e V2-2103 (FPR/FNR). É informação privilegiada.
- Os empates e as derrotas do agente listados acima: V2-1102 (k = 5), V2-1327, V2-1179 e V2-4789.
- A política do V2-4789 concentrada em FedAvg.
- Orçamentos efetivos ínfimos como achado transversal (DTAG-FL com cerca de 12 passos). O autor registrou o número, mas não o tratou como achado.

## Encaminhamento sugerido

Os dados ainda não foram alterados. A decisão é do autor. Este é o caminho sugerido:

1. **Fixar dois critérios no protocolo** (adendo):
   - **"política não aprendida"**: só ações dentro do espaço de ação do próprio agente (fixa, aleatória, regra sobre o mesmo sinal, oráculo). Agregadores externos e treino centralizado não entram;
   - **"análise de horizonte"**: ganho do agente sobre a política não aprendida em função de T.
2. **Revisar, na extração, os 20 estudos do grupo B** (QP2), os 15 de QP5, os 25 "?" de vazamento e o orçamento (QA7). Depois, regenerar a síntese.
3. **Corrigir o `cmpcat`**: ordem "fixa" antes de "aleatória"; regra para Pow-d e heurística de outro sinal.
4. **Registrar o empate em acurácia do V2-2103** (Tab. 14) como evidência do Portão N.

## Conciliação aplicada (2026-10-09)

O autor autorizou a conciliação de QP1–QP6. A QP7 fica para a análise dele. As correções entraram como linhas novas no fim de `triagem_v2/revisao_extracao.tsv`, sem apagar nada: são 153 linhas, e o backup anterior está no scratchpad da sessão. Os critérios foram registrados no protocolo como **adendo A14**.

**QP2:**
- Aceitos 17 estudos do grupo B, conferidos no texto completo:
  - V2-1275, V2-2103, V2-3331, V2-0350, V2-1363, V2-3215, V2-0351;
  - V2-0837, V2-1178, V2-0945, V2-1130, V2-0634, V2-0688, V2-1030, V2-3265;
  - V2-4233, como ablação parcial;
  - V2-4059, como heurística de **outro** sinal: o AMA não recebe o indicador de falha f_i que o RL recebe.
- Rejeitados três estudos do grupo B, por não se sustentarem no texto ou por usarem método de terceiros: V2-1105, V2-0922 e V2-1229.
- Mantida a leitura do Claude nos grupos C e D.
- Ajustada a codificação do grupo A:
  - Pow-d passa a ser "outro sinal";
  - V2-0940 passa a "fixa";
  - V2-0111 passa a "oráculo";
  - V2-3243 passa a "fixa";
  - V2-0835 passa a "outro sinal".

**QP3, QP5, QP6 e QP1:**
- **Orçamento:** registrados os parâmetros do agente em 27 estudos.
- **Modo:** V2-1103 passa a offline.
- **Privacidade:** corrigida em 26 estudos.
- **Vazamento:** decidido em 27 casos ("?" → S, P ou N).
- **Sementes:** corrigidas em 7 estudos.
- **Código:** material suplementar conta como P (2 estudos).
- **QP1:** corrigidos algoritmo (V2-1041, V2-0590), estado e recompensa (V2-1103, V2-1294, V2-1229, V2-3265) e memória (V2-0590, V2-0368, V2-0987).

**Scripts:**
- `sintese.py`: a `cmpcat` reconhece "+ fixa", e a `priv` testa "só" primeiro. Também foram atualizados o texto da contagem de votos, a QP3, a agenda, o Portão N e as limitações.
- `etapa2_lote2.py`: o QA7 ignora trechos "não reportado", e o QA5 reconhece "+ fixa".

**Arquivos regenerados:** `extracao_principal.csv`, `qualidade.csv`, `slr_resultado.md` e as tabelas LaTeX. O texto de `paper_slr/main.tex` e de `tese_cap_slr/cap_slr.tex` foi atualizado.

**Números finais:**

| item | antes | depois |
|---|---|---|
| sem comparação não aprendida | 35 | 26 |
| só aleatória | 19 | 14 |
| fixa (8 delas = não defender) | 8 | 16 |
| mesmo sinal | 5 | 7 |
| outro sinal | 1 | 7 |
| oráculo | 2 | 4 |
| parcial | 8 | 4 |
| empates com política fixa razoável | 5 | 5 (V2-0383 passa para "iguala o oráculo"; entra V2-2103) |
| QA médio | 2,83 | 3,26 |
| QA7 S/P/N | 16/46/16 | 40/30/8 |
| uso do teste (QA1 = N) | 12 | 19 |
| exigem dados no servidor | 23 (6 teste) | 45 (17 teste) |

**Portão N:** continua "parcialmente mostrado". O V2-2103 reforça o argumento: uma regra fixa sobre o mesmo sinal empata em acurácia, com 3 sementes.

## Atualização (2026-10-16)

- **QA médio corrigido de 3,28 para 3,26.** A média foi recalculada a partir de `triagem_v2/qualidade.csv`: soma 254,5 / 78 = 3,263; mediana 3,0; máximo 8,5; 12 estudos com nota ≥ 5. A planilha regenerada por `scripts/etapa2_lote2.py` sai idêntica à atual. O valor 3,28 é anterior às alterações de 13/10 (A15–A17), mas não foi possível identificar qual delas moveu a média, porque não há versão anterior da planilha. Os demais números da tabela acima conferem com a planilha atual (QA7 S/P/N = 40/30/8; QA1 = N em 19).
- **Rascunhos removidos.** As pastas `selecionados/paper_slr/` e `selecionados/tese_cap_slr/`, citadas acima, foram apagadas a pedido do autor. O manuscrito vigente está em `paper_latex/`.
