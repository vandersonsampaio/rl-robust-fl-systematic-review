# Livro de códigos: QP2 e qualidade metodológica (v2)

**Data:** 2026-10-16; revisto em 2026-10-19 (adendo A20: FedAvg e QA7)
**Uso:** reclassificação cega e independente pelo revisor 2 (R2), com o texto completo de cada estudo.
**Base:** as regras que o revisor 1 (R1) já aplicou na classificação final (protocolo §9.1 e §10; definições operacionais do adendo A14; regras de `scripts/sintese.py` e `scripts/etapa2_lote2.py`). Este documento **não cria regras novas**. Ele as escreve de forma explícita, com exemplos e casos-limite.

## 1. Regras gerais

1. Leia o **texto completo**. Não decida pelo resumo.
2. Decida pelos **números das tabelas e figuras**, e não pela conclusão que os autores do artigo tiram deles. Se o texto diz "o agente supera" e a tabela mostra empate, vale a tabela.
3. Para cada decisão, registre **onde** está a evidência (seção, tabela ou figura).
4. Se o artigo não traz a informação, registre "não documentado". Use "?" só quando o texto permite mais de uma leitura, e explique a dúvida na coluna de notas.
5. Não consulte a extração nem as decisões do R1.

## 2. QP2: comparação com políticas não aprendidas

### 2.1 O que é uma política não aprendida

É uma política **dentro do espaço de ação do próprio agente**, cuja regra de decisão é fixada antes da execução. Ela escolhe o mesmo tipo de ação que o agente (a regra de agregação da rodada, os pesos por cliente, os clientes selecionados ou os parâmetros da defesa), mas sem aprender.

**Não contam** como política não aprendida:
- agregadores robustos externos que substituem a defesa inteira (Krum, Multi-Krum, mediana, trimmed mean, FLTrust etc.) quando rodam fora do pipeline do agente;
- outros algoritmos de FL (FedAvg puro, FedProx, MFL etc.) usados como comparação externa;
- treino centralizado (é um limite superior do modelo, e não uma política);
- baselines aprendidos (outros agentes de RL, bandits, redes treinadas);
- métodos de outros artigos.

- referências **sem nenhuma ação defensiva**, mesmo quando rodam dentro do espaço de ação do agente. É o caso do FedAvg, da média simples e de aceitar ou selecionar todos os clientes sem detecção. "Não defender" e "não ter ação defensiva" são a mesma coisa, e uma referência assim não é uma política de defesa, nem aprendida nem não aprendida. Se o estudo só tem esse tipo de comparação, a categoria é **nenhuma** (consenso de 19/10/2026, adendo A20, que substitui a exceção "não defender" da versão de 16/10).

Não confundir o FedAvg com uma regra de pesos. O FedAvg pondera os clientes pelo tamanho dos dados por construção do algoritmo, e não por uma decisão de defesa. Uma regra fixa de pesos que usa o sinal do agente, como pesos iguais sobre os mesmos sinais seguidos de um limiar, é outra coisa e se classifica pelas categorias abaixo.

A **seleção aleatória** de clientes continua sendo "aleatória", porque a política sorteada está no espaço de ação do agente. Uma ação fixa que defende, como um parâmetro fixo da defesa ou a auditoria de todos os clientes com um só método, continua sendo "ação fixa".

### 2.2 Categorias

| categoria | critério | exemplos genéricos |
|---|---|---|
| **heurística sobre o mesmo sinal** | regra fixa (limiar, top-k, ranking, ponderação) aplicada ao **mesmo sinal ou escore** que o agente observa, produzindo ações no mesmo espaço | limiar estático sobre o escore de reputação que o agente recebe; seleção dos k clientes de maior escore; pesos iguais sobre os mesmos sinais que compõem o estado |
| **oráculo** | política que usa informação indisponível ao agente | regra que sabe quais clientes são maliciosos; melhor regra escolhida *a posteriori*; retreino do zero sem os clientes removidos |
| **ação fixa** | a mesma ação mantida em todas as rodadas, **sem depender do sinal** | uma regra de agregação fixa quando o agente escolhe a regra; um parâmetro fixo quando o agente ajusta o parâmetro; pesos fixos quando o agente atribui pesos; um operador fixo (por exemplo, trimmed mean) no lugar do módulo de RL |
| **heurística sobre outro sinal** | regra fixa que usa informação que o agente **não** recebe | seleção pela perda local (Power-of-Choice) quando o agente usa outro escore; pesos estáticos sobre só parte dos sinais do estado; seleção pela capacidade de computação |
| **aleatória** | seleção ou pesos sorteados no mesmo espaço de ação | seleção uniforme de clientes; pesos aleatórios |
| **ablação parcial** | variante sem o agente em que a decisão substituta não é descrita ou não está no espaço de ação do agente | "sem o agente", sem dizer o que o substitui |
| **nenhuma** | o agente só é comparado com agregadores externos, outros algoritmos de FL ou métodos aprendidos | comparação apenas com Krum, mediana, FLTrust ou outros métodos externos, ou com referências sem ação defensiva (FedAvg, todos os clientes sem detecção) |

**Distinção mais frequente:**
- *ação fixa × heurística do mesmo sinal*: a ação fixa **não usa** o sinal, e a heurística **usa**. Um limiar estático aplicado ao escore que o agente observa é heurística do mesmo sinal, mesmo que o valor do limiar seja fixo.
- *heurística do mesmo sinal × de outro sinal*: compare a entrada da heurística com o estado do agente. Se falta à heurística alguma informação que o agente recebe (ou ela usa outra), é de outro sinal.
- *ablação parcial × ação fixa*: se o artigo diz qual ação substitui o agente e ela está no espaço de ação, é ação fixa. Se só diz "sem o agente", é ablação parcial.
- *ablação parcial × nenhuma*: uma ablação que remove o agente sem pôr no lugar nenhuma decisão defensiva (desligar o módulo, voltar ao mapeamento estático padrão) é **nenhuma**, pela mesma lógica das referências sem ação defensiva. A ablação parcial fica só para quando o texto indica que outra decisão ocupa o lugar do agente (por exemplo, "seleção heurística" ou "variante sem agendamento" em que a defesa continua agindo), mas não a descreve. Um framework externo "sem o agente" segue a regra dos baselines externos (A20).

### 2.3 Precedência (referência mais forte)

Quando o estudo tem mais de uma comparação, registre todas, mas a categoria do estudo é a mais forte, nesta ordem:

**mesmo sinal → ação fixa → outro sinal → aleatória → ablação parcial → oráculo → nenhuma**

*Atualização (A27, 22/10/2026):* o oráculo usa informação indisponível ao agente e fica fora de Π0, por isso não desloca uma referência admissível. Ele só define a categoria quando é a única referência, e a comparação com ele continua registrada. A ordem anterior era mesmo sinal → oráculo → ação fixa → outro sinal → aleatória → ablação parcial → nenhuma, e é a que vale para a concordância com o R2.

### 2.4 Resultado da comparação

Classifique pelo **sentido de melhora de cada métrica**: maior acurácia é melhor, e menor ASR, perda ou taxa de falsos positivos também é melhor. Se as métricas levam a conclusões diferentes, registre cada uma separadamente.

| resultado | critério |
|---|---|
| **empate** | diferença de até cerca de 1 p.p. na métrica principal em algum regime, ou o agente não supera a referência em todos os regimes. A descrição dos autores ("semelhante", "quase igual") só decide quando não há números legíveis ou quando a diferença está dentro do erro de leitura da figura (A21) |
| **vitória estreita** | vantagem do agente acima de cerca de 1 e até cerca de 6 p.p. |
| **vitória clara** | vantagem acima de cerca de 6 p.p., ou diferença grande em outra métrica |
| **derrota** | a referência supera o agente |

**Métrica principal (A21).** É a utilidade do modelo global sob ataque, no conjunto de teste completo (acurácia, AUC, F1 da tarefa, MSE). Há duas exceções:
- **ataque dirigido:** em backdoor ou troca de rótulo para uma classe-alvo, se o estudo mede o efeito do ataque (ASR, acurácia na classe atacada), essa métrica é a principal, porque a acurácia geral dilui o efeito;
- **sem comparação em utilidade:** se o estudo não compara o agente e a referência na utilidade, vale a métrica da própria decisão do agente (F1 de detecção, CJR, fração de maliciosos selecionados).

Custo, tempo, latência e convergência são secundários, salvo quando são o único resultado comparado. As métricas secundárias vão para notas, com valores.

Registre também se o estudo relata a **variabilidade da própria comparação** (várias sementes com desvio ou intervalo) e se aplica um **teste estatístico à própria comparação**. Um teste aplicado a outras comparações do mesmo estudo não conta.

### 2.5 Discutido como achado

- **S:** os autores comentam no texto o resultado da comparação com a referência mais forte e tiram dele uma conclusão, em qualquer direção. "Supera a seleção aleatória, o que mostra a eficácia da seleção" é S.
- **P:** a comparação é só mencionada de passagem, ou o resultado aparece só na tabela ou na figura.
- **N:** a comparação não aparece no texto. Sem comparação não aprendida (categoria nenhuma), o código é N.

Esta pergunta não é o critério do Portão N (A21). Para o Portão N, nos empates e nas derrotas contra o mesmo sinal ou a ação fixa, registre nas notas do campo se os autores **reconhecem** que a política não aprendida iguala ou supera o agente e que conclusão tiram disso sobre o papel do aprendizado. Um estudo que reconhece a igualdade, mas a enquadra como virtude do agente (adaptabilidade, estabilidade da detecção), não a apresenta como achado contra o aprendizado.

## 3. Qualidade metodológica (QA1–QA9)

Cada critério vale **S = 1**, **P = 0,5** ou **N = 0**. Pela convenção conservadora, o que o artigo não documenta é pontuado como N, exceto nos casos em que a regra abaixo diz o contrário.

| critério | S | P | N |
|---|---|---|---|
| **QA1.** Recompensa e seleção de modelo sem o conjunto de teste | a recompensa e a seleção usam dados de treino, de validação disjunta ou de raiz no servidor, e isso está escrito | dados do servidor amostrados do conjunto de teste, mas disjuntos da avaliação final, ou informação insuficiente sobre os dados da recompensa | o artigo mostra o uso do conjunto de teste na recompensa, no estado, na seleção do modelo ou na verificação das atualizações |
| **QA2.** Três ou mais sementes com variabilidade | ≥ 3 execuções independentes e desvio-padrão, intervalo ou barras de erro | duas ou mais execuções sem medida de variabilidade, ou variabilidade com menos de três execuções | uma execução ou número de execuções não informado |
| **QA3.** Teste estatístico ou intervalo de confiança nas comparações principais | teste t, ANOVA, Wilcoxon, Tukey, IC 95% ou valor-p nas comparações principais | — | ausente |
| **QA4.** Código acessível e suficiente (A24) | código acessível sem intermediação (repositório público ou suplemento do periódico) com o agente e o experimento (ataques e configuração ou scripts), conferido abrindo o link | acessível mas incompleto, ou declarado sem acesso direto (mediante pedido, sem link, link quebrado) | sem código declarado |
| **QA5.** Comparação com política não aprendida (seção 2) | ação fixa que é uma defesa ou heurística do mesmo sinal | aleatória, heurística de outro sinal, oráculo (informação indisponível ao agente, fora de Π0) ou ablação parcial (A23) | nenhuma, ou só referências sem ação defensiva (A20) |
| **QA6.** Ataques fiéis às definições originais | a descrição permite confirmar que o ataque segue a definição original (parâmetros, fração e momento) | descrição insuficiente para verificar | o ataque implementado diverge da definição original |
| **QA7.** Hiperparâmetros do agente suficientes para calcular o orçamento | o **volume** de treino do agente (passos, episódios, iterações ou rodadas) **e** ao menos um parâmetro de otimização do agente (taxa de aprendizado, γ, tamanho do replay ou batch) | só o volume, só parâmetros sem volume, ou só o cronograma de ε | nenhum parâmetro do agente (os do treino local dos clientes não contam) |
| **QA8.** Comparação com defesas estáticas fortes das duas famílias | uma defesa que usa dados no servidor (FLTrust, Zeno, dataset raiz ou conjunto de validação do servidor) **e** uma regra estatística robusta (Krum, mediana, trimmed mean, Bulyan, RFA, clipping, SignGuard) | só uma das duas famílias | nenhuma |
| **QA9.** Ataque adaptativo que conhece a defesa | o adversário conhece a defesa e ajusta o ataque a ela | o ataque é descrito como adaptativo, mas não usa conhecimento da defesa | ausente |

**QA1:** se a recompensa e a seleção não usam nenhum dado de avaliação do modelo (por exemplo, só métricas de infraestrutura ou votos dos participantes com os próprios modelos locais), e isso está escrito, o critério é S. Se o artigo usa um conjunto declarado em uma parte do ciclo (por exemplo, L_val no contrafactual) mas não diz de onde vêm as métricas da recompensa, o critério é P (A20).

**QA6:** avalie os ataques contra os quais a **decisão do agente** é testada, e não todos os ataques do artigo. Se houver mais de um, S só quando todos permitem verificar parâmetros, fração de atacantes e momento da ativação. Para um ataque proposto pelo próprio artigo, ou definido de forma genérica ("bizantino arbitrário"), S exige que esses três itens estejam documentados. Um ataque consagrado com um parâmetro escolhido fora da regra original (por exemplo, z fixo no LIE em vez do z calculado por n e pelo número de atacantes) não permite confirmar a fidelidade e fica com P (A20).

**QA9:** S quando o adversário usa o conhecimento da defesa avaliada para ajustar o ataque contra pelo menos um componente dela, seja por otimização ou por estratégia (por exemplo, dividir os clientes maliciosos para escapar de um detector). Não é preciso mirar o pipeline completo. P quando o ataque é adaptativo ou otimizado só contra outra regra (por exemplo, o AGRT contra o Krum) sem ajuste à defesa avaliada. Atacar a política do agente, envenenando a recompensa ou o estado, é analisado à parte na síntese e não muda o QA9 (A20).

**QA8:** defesas de detecção ou filtragem que não usam dados no servidor, como FLAME, FLDetector e FLGuard, não contam em nenhuma das duas famílias.

**Pré-treino offline:** no QA1, avalie os dados da recompensa no pré-treino; no QA7, avalie o orçamento em episódios ou passos.

## 4. Procedimento para o R2

1. Use a planilha cega e os PDFs do pacote. Se faltar algum PDF, avise antes de classificar o estudo.
2. Preencha todos os campos. Em cada decisão, informe a seção, a tabela ou a figura.
3. Não consulte a extração do R1 nem as notas da conciliação.
4. Ao terminar, envie a planilha sem alterações posteriores. A concordância é calculada sobre essa versão, **antes** de qualquer consenso.
