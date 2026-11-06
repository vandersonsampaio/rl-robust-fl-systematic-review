# Livro de códigos: QP2 e qualidade metodológica (v2)

**Data:** 2026-10-16
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

**Exceção:** uma ação fixa que equivale a não defender (aceitar todos os clientes com pesos iguais) **conta como ação fixa** quando está no espaço de ação do agente. Ela é registrada como "fixa" e analisada à parte, porque só mostra se a defesa ajuda, e não se o aprendizado é necessário.

### 2.2 Categorias

| categoria | critério | exemplos genéricos |
|---|---|---|
| **heurística sobre o mesmo sinal** | regra fixa (limiar, top-k, ranking, ponderação) aplicada ao **mesmo sinal ou escore** que o agente observa, produzindo ações no mesmo espaço | limiar estático sobre o escore de reputação que o agente recebe; seleção dos k clientes de maior escore; pesos iguais sobre os mesmos sinais que compõem o estado |
| **oráculo** | política que usa informação indisponível ao agente | regra que sabe quais clientes são maliciosos; melhor regra escolhida *a posteriori*; retreino do zero sem os clientes removidos |
| **ação fixa** | a mesma ação mantida em todas as rodadas, **sem depender do sinal** | uma regra de agregação fixa quando o agente escolhe a regra; um parâmetro fixo quando o agente ajusta o parâmetro; pesos fixos quando o agente atribui pesos; um operador fixo (por exemplo, trimmed mean) no lugar do módulo de RL |
| — subtipo **não defender** | ação fixa que aceita todos os clientes com pesos iguais, ou mantém uma estrutura fixa sem defesa | média simples 1/N; todos os clientes selecionados, sem detecção |
| **heurística sobre outro sinal** | regra fixa que usa informação que o agente **não** recebe | seleção pela perda local (Power-of-Choice) quando o agente usa outro escore; pesos estáticos sobre só parte dos sinais do estado; seleção pela capacidade de computação |
| **aleatória** | seleção ou pesos sorteados no mesmo espaço de ação | seleção uniforme de clientes; pesos aleatórios |
| **ablação parcial** | variante sem o agente em que a decisão substituta não é descrita ou não está no espaço de ação do agente | "sem o agente", sem dizer o que o substitui |
| **nenhuma** | o agente só é comparado com agregadores externos, outros algoritmos de FL ou métodos aprendidos | comparação apenas com Krum, mediana, FLTrust ou FedAvg rodando fora do pipeline do agente |

**Distinção mais frequente:**
- *ação fixa × heurística do mesmo sinal*: a ação fixa **não usa** o sinal, e a heurística **usa**. Um limiar estático aplicado ao escore que o agente observa é heurística do mesmo sinal, mesmo que o valor do limiar seja fixo.
- *heurística do mesmo sinal × de outro sinal*: compare a entrada da heurística com o estado do agente. Se falta à heurística alguma informação que o agente recebe (ou ela usa outra), é de outro sinal.
- *ablação parcial × ação fixa*: se o artigo diz qual ação substitui o agente e ela está no espaço de ação, é ação fixa. Se só diz "sem o agente", é ablação parcial.

### 2.3 Precedência (referência mais forte)

Quando o estudo tem mais de uma comparação, registre todas, mas a categoria do estudo é a mais forte, nesta ordem:

**mesmo sinal → oráculo → ação fixa → outro sinal → aleatória → ablação parcial → nenhuma**

### 2.4 Resultado da comparação

Classifique pelo **sentido de melhora de cada métrica**: maior acurácia é melhor, e menor ASR, perda ou taxa de falsos positivos também é melhor. Se as métricas levam a conclusões diferentes, registre cada uma separadamente.

| resultado | critério |
|---|---|
| **empate** | diferença de até cerca de 1 p.p. na métrica principal, os autores descrevem os resultados como semelhantes, ou o agente não supera a referência em todos os regimes |
| **vitória estreita** | vantagem do agente acima de cerca de 1 e até cerca de 6 p.p. |
| **vitória clara** | vantagem acima de cerca de 6 p.p., ou diferença grande em outra métrica |
| **derrota** | a referência supera o agente |

Registre também se o estudo relata a **variabilidade da própria comparação** (várias sementes com desvio ou intervalo) e se aplica um **teste estatístico à própria comparação**. Um teste aplicado a outras comparações do mesmo estudo não conta.

### 2.5 Discutido como achado

- **S:** os autores discutem o resultado dessa comparação no texto e tiram dele uma conclusão.
- **P:** a comparação é mencionada de passagem ou só aparece na tabela.
- **N:** não há discussão.

## 3. Qualidade metodológica (QA1–QA9)

Cada critério vale **S = 1**, **P = 0,5** ou **N = 0**. Pela convenção conservadora, o que o artigo não documenta é pontuado como N, exceto nos casos em que a regra abaixo diz o contrário.

| critério | S | P | N |
|---|---|---|---|
| **QA1.** Recompensa e seleção de modelo sem o conjunto de teste | a recompensa e a seleção usam dados de treino, de validação disjunta ou de raiz no servidor, e isso está escrito | dados do servidor amostrados do conjunto de teste, mas disjuntos da avaliação final, ou informação insuficiente sobre os dados da recompensa | o artigo mostra o uso do conjunto de teste na recompensa, no estado, na seleção do modelo ou na verificação das atualizações |
| **QA2.** Três ou mais sementes com variabilidade | ≥ 3 execuções independentes e desvio-padrão, intervalo ou barras de erro | duas ou mais execuções sem medida de variabilidade, ou variabilidade com menos de três execuções | uma execução ou número de execuções não informado |
| **QA3.** Teste estatístico ou intervalo de confiança nas comparações principais | teste t, ANOVA, Wilcoxon, Tukey, IC 95% ou valor-p nas comparações principais | — | ausente |
| **QA4.** Código disponível | repositório público citado no artigo | só no material suplementar do periódico ou mediante pedido | indisponível |
| **QA5.** Comparação com política não aprendida (seção 2) | ação fixa, heurística do mesmo sinal ou oráculo | aleatória, heurística de outro sinal ou ablação parcial | nenhuma |
| **QA6.** Ataques fiéis às definições originais | a descrição permite confirmar que o ataque segue a definição original (parâmetros, fração e momento) | descrição insuficiente para verificar | o ataque implementado diverge da definição original |
| **QA7.** Hiperparâmetros do agente suficientes para calcular o orçamento | parâmetros do **agente**: passos, episódios, taxa de aprendizado, γ, tamanho do replay, batch, cronograma de ε | só alguns parâmetros, por exemplo só o número de rodadas de FL | nenhum parâmetro do agente (os do treino local dos clientes não contam) |
| **QA8.** Comparação com defesas estáticas fortes das duas famílias | uma defesa que usa dados no servidor (FLTrust, Zeno, dataset raiz ou conjunto de validação do servidor) **e** uma regra estatística robusta (Krum, mediana, trimmed mean, Bulyan, RFA, clipping, SignGuard) | só uma das duas famílias | nenhuma |
| **QA9.** Ataque adaptativo que conhece a defesa | o adversário conhece a defesa e ajusta o ataque a ela | o ataque é descrito como adaptativo, mas não usa conhecimento da defesa | ausente |

**QA8:** defesas de detecção ou filtragem que não usam dados no servidor, como FLAME, FLDetector e FLGuard, não contam em nenhuma das duas famílias.

**Pré-treino offline:** no QA1, avalie os dados da recompensa no pré-treino; no QA7, avalie o orçamento em episódios ou passos.

## 4. Procedimento para o R2

1. Use a planilha cega e os PDFs do pacote. Se faltar algum PDF, avise antes de classificar o estudo.
2. Preencha todos os campos. Em cada decisão, informe a seção, a tabela ou a figura.
3. Não consulte a extração do R1 nem as notas da conciliação.
4. Ao terminar, envie a planilha sem alterações posteriores. A concordância é calculada sobre essa versão, **antes** de qualquer consenso.
