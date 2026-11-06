# Protocolo de revisão sistemática: defesas de aprendizado federado baseadas em RL e bandits, e o que o aprendizado de fato contribui

**Versão:** 1.1
**Data:** 2026-09-27
**Status:** a congelar e registrar no OSF **antes da primeira busca**. Mudanças posteriores entram só como adendo datado no §15. _Situação real: não registrado no OSF; busca executada em 2026-09-28; ver adendos no §15.3._
**Autor e revisor 1:** Vanderson S. de O. L. Sampaio (doutorando)
**Revisor 2:** identidade não divulgada. Participa desde 05/10/2026: calibração e amostra cega de 20% da etapa 1, com κ entre avaliadores (A12–A13); conferência das exclusões da etapa 2, de 20% das inclusões, da QP2 e de 20% da qualidade, com consenso (A16). Antes disso não havia revisor 2 (A1).
**Diretrizes:** Kitchenham e Charters (2007), para revisões sistemáticas em computação; PRISMA 2020, para fluxo e relato; Wohlin (2014), para snowballing.
**Autossuficiência:** este documento basta para executar a revisão inteira. Não depende de nenhum outro arquivo.

---

## 1. Contexto e justificativa

### 1.1 Justificativa (texto para o artigo)

Defesas de aprendizado federado (FL) contra clientes bizantinos e envenenadores passaram a usar aprendizado por reforço (RL) e bandits para decidir a agregação:
- escolher a regra robusta de cada rodada;
- atribuir pesos por cliente;
- selecionar ou excluir clientes;
- ajustar parâmetros da defesa.

Essas defesas são apresentadas como "adaptativas" e comparadas, em geral, com regras estáticas (Krum, Mediana, Trimmed Mean, FLTrust). Falta, porém, um mapeamento de **quanto do ganho é atribuível ao componente aprendido**, e não aos demais componentes que acompanham o agente: o sinal de detecção, a granularidade da decisão e a memória entre rodadas.

Outras áreas mostraram que baselines simples igualam agentes de deep RL (busca aleatória simples, políticas lineares) e que a variância entre sementes compromete conclusões com poucas execuções. Esta revisão verifica se a literatura de defesas de FL baseadas em RL isola a contribuição do aprendizado, com que orçamento de treino os agentes operam, que custo e que exposição de privacidade seus sinais impõem, e com que rigor são avaliadas.

### 1.2 Motivação interna (não entra no artigo)

A revisão é o capítulo de estado da arte da tese e serve a duas decisões internas:
- **(a)** posicionar um artigo de auditoria. Numa reprodução do AdaAggRL (TD3), substituir o agente por uma ação fixa não piorou o resultado. No código oficial, com 500 rodadas, a política do agente não se afastou da inicialização e não variou com o ataque.
- **(b)** derivar requisitos para uma nova defesa (GRADF-v2).

**A revisão precisa ser neutra quanto ao desfecho.** A hipótese interna é conhecida pelo revisor 1, e as mitigações de viés estão no §14.

## 2. Objetivo e decisões que a revisão alimenta

**Objetivo:** mapear as defesas de FL contra clientes adversários que usam RL ou bandits para decidir a agregação. Caracterizar, para cada uma:
- sua decomposição em sinal, granularidade, memória e aprendizado;
- seu orçamento de aprendizado;
- o custo e a exposição de privacidade de seu sinal;
- o rigor de sua avaliação;
- **se e como isola a contribuição do aprendizado** frente a políticas não aprendidas.

**Portão N (novidade do artigo de auditoria), aplicado ao final da síntese:**
- **Já mostrado:** pelo menos um estudo incluído reporta, para uma defesa de FL baseada em RL, uma comparação controlada em que uma política **não aprendida com o mesmo sinal** (ação fixa ou heurística) iguala ou supera o agente, e apresenta isso como achado. → Reposicionar a contribuição (generalização entre métodos, novos eixos de decomposição, mecanismo, custo e privacidade).
- **Parcialmente mostrado:** existe comparação, mas só contra política aleatória, contra heurística com **outro** sinal, ou como detalhe sem discussão. → A novidade se mantém; citar e diferenciar.
- **Não mostrado:** nenhum estudo faz essa comparação. → A novidade fica ancorada.

**Portão R (requisitos do GRADF-v2):** das QP4–QP6 e da lista de defesas adaptativas não-RL (§9.2), derivar:
- as lacunas que uma defesa nova precisa cobrir (ataques em que os sinais falham, ataques adaptativos, custo, privacidade);
- os baselines obrigatórios (os mais fortes de cada família).

## 3. Perguntas de pesquisa

| id | pergunta | papel |
|---|---|---|
| **QP1** | Quais defesas de FL contra clientes bizantinos ou envenenadores usam RL ou bandits para decidir pesos, seleção de clientes, regra de agregação ou parâmetros da defesa? Qual é o sinal, o estado, a ação e a recompensa de cada uma, e em que domínio de aplicação são avaliadas? | mapeamento |
| **QP2** | Quais delas comparam o agente com políticas **não aprendidas** (ação fixa, aleatória, heurística com o mesmo sinal, oráculo)? Com que resultado? | **central** |
| **QP3** | Qual é o **orçamento de aprendizado** de cada uma (rodadas, passos de gradiente, taxa de aprendizado, aquecimento, pré-treino offline ou aprendizado online)? Alguma analisa o ganho em função do horizonte? | central |
| **QP4** | Que componentes são ablados, nos eixos **sinal**, **granularidade** (uma regra por rodada contra decisão por cliente), **memória** (confiança ou penalidade persistente entre rodadas) e **aprendizado**? | decomposição |
| **QP5** | Que **custo** e que **exposição de privacidade** o sinal impõe? Exige reconstrução de dados do cliente (inversão de gradiente), dataset raiz no servidor, conjunto de validação, ou só os updates? Que custo computacional ou de tempo é reportado? | custo e privacidade |
| **QP6** | Qual é a qualidade da avaliação: vazamento de teste na recompensa, fidelidade dos ataques, **ataques adaptativos** (que conhecem a defesa), número de sementes, estatística, baselines estáticos fortes, código disponível? | qualidade |
| **QP7** | Que trabalhos de auditoria ou reprodutibilidade (em RL em geral e em FL robusto) mostram baselines simples igualando agentes aprendidos? | posicionamento |

## 4. Escopo (PICOC)

- **População:** sistemas de aprendizado federado (horizontal ou vertical, cross-device ou cross-silo) com clientes adversários.
- **Intervenção:** mecanismo de defesa com componente de decisão aprendido por RL (inclusive deep RL) ou por bandits (contextuais ou não).
- **Comparação:** políticas não aprendidas (fixa, aleatória, heurística, oráculo) e defesas estáticas (FedAvg, Krum, Mediana, Trimmed Mean, FLTrust etc.).
- **Resultados:** acurácia e robustez sob ataque, taxa de detecção, ablações, custo computacional, exposição de privacidade do sinal.
- **Contexto:** qualquer domínio de aplicação (o domínio é extraído, não filtrado); estudos empíricos, com simulação ou sistema real.

## 5. Fontes de busca

| fonte | papel | observação |
|---|---|---|
| Scopus | principal | cobre boa parte de IEEE, ACM, Springer e Elsevier |
| IEEE Xplore | principal | conferências IEEE que o Scopus indexa com atraso |
| ACM Digital Library | principal | CCS, KDD, WWW, AsiaCCS |
| Web of Science | complementar | usar se houver acesso institucional (CAPES) |
| arXiv | principal (preprints) | a área publica muito em preprint; marcar o status de revisão por pares |
| Google Scholar / Semantic Scholar | só snowballing | citações para frente e para trás; não usar como busca primária (não é reprodutível) |

**Período:** 2017-01-01 até a data da busca. O marco de 2017 é o Krum (Blanchard et al.), início da literatura de agregação robusta.
**Idioma:** inglês. Trabalhos relevantes em outros idiomas são registrados à parte, sem inclusão.

## 6. Strings de busca

### 6.1 Blocos conceituais

- **A (FL):** `"federated learning" OR "federated optimization" OR "federated averaging"`
- **B (RL e bandits):** `"reinforcement learning" OR "Q-learning" OR "deep Q" OR DQN OR "policy gradient" OR "actor-critic" OR DDPG OR TD3 OR PPO OR "soft actor-critic" OR "multi-armed bandit" OR "contextual bandit" OR LinUCB OR "Markov decision process"`
- **C (adversário e defesa):** `byzantine OR poisoning OR backdoor OR malicious OR adversar* OR "robust aggregation" OR attack*`

**String primária (S1):** A AND B AND C, em título, resumo e palavras-chave.

### 6.2 Sintaxe por base

Conferir a sintaxe no dia da busca e copiar para o log (§11.2) **o texto exato** executado.

**Scopus:**
```
TITLE-ABS-KEY ( ( "federated learning" OR "federated optimization" OR "federated averaging" )
AND ( "reinforcement learning" OR "Q-learning" OR "deep Q" OR dqn OR "policy gradient" OR "actor-critic"
      OR ddpg OR td3 OR ppo OR "soft actor-critic" OR "multi-armed bandit" OR "contextual bandit"
      OR linucb OR "Markov decision process" )
AND ( byzantine OR poisoning OR backdoor OR malicious OR adversar* OR "robust aggregation" OR attack* ) )
AND PUBYEAR > 2016
```

**IEEE Xplore** (Command Search, campo "All Metadata"):
- mesma estrutura, com cada termo prefixado por `"All Metadata":`;
- se exceder o limite de termos, dividir o bloco B em:
  - B1: `"reinforcement learning"` … `"soft actor-critic"`;
  - B2: `bandit` … `"Markov decision process"`;
- rodar A∧B1∧C e A∧B2∧C e unir os resultados.

**ACM DL** (Advanced Search, campos Title + Abstract + Keywords): mesma lógica booleana; o ACM trata frases entre aspas corretamente. Se houver limite de termos, aplicar a mesma divisão do bloco B.

**arXiv** (API ou busca avançada, campo `abs`; categorias cs.LG, cs.CR, cs.DC, cs.AI, stat.ML):
```
abs:"federated learning" AND (abs:"reinforcement learning" OR abs:bandit OR abs:"Q-learning"
  OR abs:DQN OR abs:DDPG OR abs:TD3 OR abs:PPO OR abs:"actor-critic")
AND (abs:byzantine OR abs:poisoning OR abs:backdoor OR abs:malicious OR abs:"robust aggregation")
```

**Web of Science:** `TS=((A) AND (B) AND (C))`, com os blocos do §6.1 e PY=2017–atual.

### 6.3 String secundária (S2, para QP7)

```
( "reinforcement learning" OR bandit )
AND ( ablation OR "random policy" OR "fixed policy" OR "heuristic baseline" OR "simple baseline"
      OR reproducib* OR "sanity check" )
AND ( "federated learning" OR "robust aggregation" OR "Byzantine" )
```
Rodar no Scopus e no arXiv. Complementar com as leituras canônicas do §13, incluídas diretamente e não pela busca.

### 6.4 Validação da string (quasi-gold standard, QGS)

Antes da busca definitiva, rodar S1 e verificar se ela recupera o QGS. Os trabalhos abaixo foram verificados na web em 2026-09-25; **reconfirmar as citações completas (autores, venue, DOI) antes da extração**.

| # | trabalho | agente | deve ser |
|---|---|---|---|
| Q1 | Wang et al., *Defending Against Sophisticated Poisoning Attacks with RL-based Aggregation in Federated Learning* (AdaAggRL), AAAI 2025, arXiv:2406.14217 | TD3 | recuperado e incluído |
| Q2 | *FedAA: A Reinforcement Learning Perspective on Adaptive Aggregation for Fair and Robust Federated Learning*, AAAI 2025, arXiv:2402.05541 | DDPG | recuperado e incluído |
| Q3 | *FedDRLPD: Deep Reinforcement Learning-Based Defense Mechanism against Poisoning Attacks in Federated Learning*, Knowledge-Based Systems (ScienceDirect), 2026 | DQN | recuperado e incluído |
| Q4 | Ahmed et al., *Trust-Aware Reinforcement Selection for Robust FL under Adaptive Adversaries* (TARS), IEEE Xplore doc. 11215089, 2025 | Q-learning | recuperado e incluído |
| Q5 | Haque, Kamal e Hossain, *FedStrategist: A Meta-Learning Framework for Adaptive and Robust Aggregation in Federated Learning*, arXiv:2507.14322, 2025 | bandit contextual | recuperado e incluído |
| B1 | Tang et al., *AdaBFL: Multi-Layer Defensive Adaptive Aggregation for Byzantine-Robust FL*, arXiv:2604.27434, 2026 | não é RL (adaptativo heurístico) | **controle de fronteira:** se aparecer, é excluído por EC2 e entra na lista do §9.2 |
| B2 | Li, Sun e Zheng, *Learning to Attack Federated Learning*, NeurIPS 2022 | RL do **atacante** | **controle de fronteira:** excluído por EC1 |

**Critério de aceitação da string:** Q1–Q5 recuperados na **união** das bases (sensibilidade esperada 5/5). Se algum faltar, identificar o termo ausente, revisar a string, registrar no §15 e repetir.

**Candidatos vistos durante a preparação** (fora do QGS; passam pela triagem normal, sem inclusão automática):
- arXiv:2510.01261, *Adaptive FL Defences via Trust-Aware Deep Q-Networks*;
- arXiv:2507.23638, *OptiGradTrust*;
- Springer, ISBN 978-981-97-7241-4, cap. 10, *Byzantine-Robust Aggregation for FL with RL*;
- Springer, cap. 40, *Adaptive Robust Client Selection in FL: A Two-Stage RL Approach*;
- arXiv:2603.16846, *Dynamic Meta-Layer Aggregation for Byzantine-Robust FL*;
- IACR ePrint 2025/510, *Adaptive Adversaries in Byzantine-Robust FL: A Survey* (só para snowballing).

## 7. Critérios de inclusão e exclusão

**Inclusão (todos):**
- **IC1:** o sistema é de aprendizado federado.
- **IC2:** o trabalho propõe ou avalia uma **defesa** contra clientes adversários (bizantinos, envenenamento de dados ou de modelo, backdoor, free-riding malicioso).
- **IC3:** a defesa tem um componente de decisão **aprendido por RL ou bandit** que afeta pesos de agregação, seleção ou exclusão de clientes, escolha da regra de agregação ou parâmetros da defesa (limiares, clipping etc.).
- **IC4:** há avaliação empírica (simulação ou sistema real).
- **IC5:** é artigo completo revisado por pares, ou preprint (arXiv) com texto completo. Preprints são marcados no campo `revisado_por_pares`.

**Exclusão (qualquer um):**
- **EC1:** o RL é usado só pelo **atacante**. Pode servir de contexto para QP7 e para ataques adaptativos, mas não é incluído.
- **EC2:** a defesa é adaptativa sem componente de RL ou bandit (heurística, meta-regra fixa, otimização de uma única etapa). **Não é incluído na síntese principal, mas vai para a lista de defesas adaptativas não-RL (§9.2)**, com ficha reduzida.
- **EC3:** o RL é usado em FL só para eficiência, energia, justiça ou comunicação, **sem** adversários.
- **EC4:** RL federado (FL para treinar agentes de RL) em que a robustez é do treino do RL, e não uma defesa da agregação de um modelo supervisionado.
- **EC5:** revisão ou survey. Não é incluído, mas é usado no snowballing.
- **EC6:** resumo estendido, pôster, artigo com menos de 4 páginas, sem texto completo, ou fora do inglês.
- **EC7:** duplicata ou versão anterior. Mantém-se a versão mais completa (em geral a publicada) e registram-se as demais.

**Casos de dúvida:** incluir na etapa 1 e decidir no texto completo. Nunca excluir por dúvida na primeira etapa.

## 8. Processo de seleção

1. **Registro:** registrar este protocolo no OSF (§15.1) antes de qualquer busca definitiva.
2. **Validação da string:** executar o §6.4 e registrar o resultado no log.
3. **Busca:** executar S1 em cada base e exportar (RIS, BibTeX ou CSV) com a data. Registrar no log de buscas (§11.2).
4. **Deduplicação:** por DOI, depois por título normalizado (Zotero, Rayyan ou script). Registrar o número de duplicatas removidas.
5. **Calibração entre revisores (antes da etapa 1):** os dois revisores triam, de forma independente, os mesmos 20 registros sorteados. Depois discutem as divergências e ajustam a redação dos critérios, se necessário (a mudança vai para o §15). Esses 20 registros não entram no cálculo do κ.
6. **Etapa 1 (título e resumo):** o revisor 1 tria todos os registros. Códigos de decisão:
   - `I`: inclui;
   - `E-ECn`: exclui, com o critério;
   - `D`: dúvida, segue para a etapa 2.
7. **Confiabilidade da etapa 1:** o revisor 2 tria às cegas uma amostra aleatória de **20% dos registros (mínimo de 30)**, sem ver as decisões do revisor 1.
   - Calcular o **κ de Cohen entre revisores** (`I` e `D` contam juntos como "segue"; `E-*` como "exclui").
   - Se κ < 0,6: revisar os critérios, registrar no §15 e retriar todos os registros.
   - As divergências da amostra são resolvidas por consenso e, se persistirem, pelo orientador.
8. **Etapa 2 (texto completo):** o revisor 1 aplica os critérios de novo e registra o motivo de cada exclusão. O revisor 2 confere **todas as exclusões por IC3/EC2** (a fronteira "RL contra adaptativo não-RL" é a decisão mais sujeita a erro) e uma amostra de 20% das inclusões. Reportar a concordância.
9. **Snowballing (Wohlin 2014):** sobre o conjunto incluído, busca **para trás** (referências) e **para frente** (citações, via Google Scholar ou Semantic Scholar), com os mesmos critérios. Iterar até uma rodada não trazer nenhum novo incluído. Prioridade de busca para frente: AdaAggRL, FedAA, TARS e FedStrategist.
10. **Sem revisor 2 disponível (alternativa declarada):** o revisor 1 retria às cegas a mesma amostra de 20% depois de pelo menos 7 dias e reporta o κ **intra-avaliador**. Isso deve ser declarado como limitação no artigo (§14).

## 9. Extração de dados

### 9.1 Ficha principal (estudos incluídos)

Uma linha por estudo incluído.

| grupo | campo | valores ou observação |
|---|---|---|
| bibliográfico | `id`, `titulo`, `autores`, `ano`, `venue`, `doi_arxiv`, `revisado_por_pares` | |
| contexto | `dominio` | geral/benchmark, saúde, IoT/IoMT, finanças, veicular, outro |
| | `cenario_fl` | cross-device ou cross-silo; horizontal ou vertical |
| agente | `algoritmo` | Q-learning, DQN, DDPG, TD3, PPO, SAC, bandit (LinUCB, UCB, TS), outro |
| | `estado` | o que o agente observa; dimensão; invariante a permutação dos clientes? |
| | `acao` | espaço (discreto ou contínuo) e dimensão |
| | `granularidade` | `regra/rodada` (escolhe a regra), `peso/cliente`, `selecao/cliente`, `parametro` (limiar etc.) |
| | `recompensa` | definição; **dado usado** (validação, root, teste, treino) |
| | `vazamento_teste` | S/N/?: a recompensa ou a seleção de modelo usam o conjunto de teste? |
| aprendizado | `modo` | pré-treino offline, online durante o FL, ou ambos |
| | `orcamento` | rodadas de FL, passos de RL, atualizações de gradiente, taxa de aprendizado, aquecimento aleatório, episódios. **Calcular o nº efetivo de atualizações quando os hiperparâmetros permitirem** |
| | `analise_horizonte` | S/N: reporta o ganho em função do nº de rodadas? |
| decomposição | `sinal` | detector ou métrica que alimenta o agente (cosseno, norma, perda, reconstrução, MMD etc.) |
| | `memoria` | S/N; forma e força (penalidade, reputação, decaimento, perdão) |
| | `ablacoes` | lista dos componentes removidos e resultado de cada |
| custo e privacidade (QP5) | `privacidade_sinal` | só updates / dataset raiz no servidor / conjunto de validação no servidor / **reconstrução de dados do cliente** / outro |
| | `custo` | custo computacional ou tempo por rodada reportado (S/N e valor); overhead relativo ao FedAvg |
| QP2 | `comparacao_nao_aprendida` | nenhuma / aleatória / fixa / heurística com **mesmo** sinal / heurística com **outro** sinal / oráculo |
| | `resultado_comparacao` | Δ reportado e direção; o agente vence? por quanto? com significância? |
| | `discutido_como_achado` | S/N |
| avaliação | `ataques` | lista; implementação conferível? (S/N/código) |
| | `ataque_adaptativo` | S/N: há atacante que conhece a defesa (on-off, evasão de limiar, otimização contra o agente)? Qual? |
| | `datasets_modelos` | |
| | `clientes` | nº total, participação por rodada, % de adversários, IID ou não-IID (e grau) |
| | `baselines_estaticos` | quais (FedAvg, Krum, Mediana, Trimmed Mean, FLTrust, …) |
| | `sementes_estatistica` | nº de sementes; variância reportada; teste estatístico |
| | `codigo` | URL, se houver; S/N |
| notas | `notas` | texto livre |

### 9.2 Ficha reduzida: defesas adaptativas não-RL (excluídas por EC2)

Serve ao Portão R (concorrentes sem aprendizado e baselines para o GRADF-v2). Não entra na síntese principal.

`id, titulo, ano, venue, doi_arxiv, mecanismo_adaptativo (resumo em 1 linha), granularidade, sinal, memoria (S/N), privacidade_sinal, ataques, ataque_adaptativo (S/N), codigo (S/N), resultado_principal (1 linha)`

## 10. Avaliação de qualidade

Serve para **caracterizar**, não para excluir. Pontuação: S = 1, P (parcial) = 0,5, N = 0. Máximo 9.

| id | critério |
|---|---|
| QA1 | A recompensa e a seleção de modelo não usam o conjunto de teste. |
| QA2 | Há ≥ 3 sementes e a variabilidade é reportada. |
| QA3 | Há teste estatístico ou IC nas comparações principais. |
| QA4 | O código está disponível. |
| QA5 | Há ablação do **aprendizado** (comparação com política não aprendida). |
| QA6 | Os ataques são implementados conforme a definição original (conferir no código quando houver). |
| QA7 | Os hiperparâmetros do agente bastam para calcular o orçamento de aprendizado. |
| QA8 | Há comparação com defesas estáticas fortes (pelo menos FLTrust ou equivalente com dado de servidor, e uma regra estatística robusta). |
| QA9 | Há avaliação contra pelo menos um **ataque adaptativo** que conhece a defesa. |

O revisor 2 pontua de forma independente pelo menos 20% dos estudos incluídos. Reportar a concordância (κ ponderado ou % de acordo por critério).

## 11. Registros

### 11.1 Planilha de triagem (CSV)
`id, fonte, titulo, ano, doi_arxiv, etapa1_decisao_r1, etapa1_motivo_r1, etapa1_decisao_r2 (se amostrado), etapa1_consenso, etapa2_decisao, etapa2_motivo, conferido_r2 (S/N), via_snowballing (S/N), origem_snowballing`

### 11.2 Log de buscas (CSV)
`data, base, string (texto exato), campos, filtros, n_resultados, arquivo_exportado`

Incluir também uma linha por execução da validação do QGS (§6.4), com o resultado Q1–Q5.

### 11.3 Fichas
- `extracao_principal.csv` (§9.1)
- `extracao_adaptativo_nao_rl.csv` (§9.2)
- `qualidade.csv` (§10), com as colunas de r1 e r2

### 11.4 Fluxo PRISMA 2020
Registrar:
- identificados por base;
- duplicatas removidas;
- triados na etapa 1;
- excluídos na etapa 1 (por motivo);
- texto completo avaliado;
- excluídos na etapa 2 (por motivo, separando EC2 → lista §9.2);
- incluídos via busca;
- incluídos via snowballing;
- total incluído.

### 11.5 Material suplementar do artigo
Publicar junto com o artigo: strings exatas por base com as datas, planilhas de triagem e extração, cálculos de κ e checklist PRISMA 2020 preenchido.

## 12. Síntese

1. **Mapeamento (QP1, QP4):** tabela com todos os incluídos nos 4 eixos (sinal × granularidade × memória × aprendizado) e contagens por categoria; distribuição por domínio e por cenário de FL.
2. **QP2 (central):** tabela com todos os estudos que têm alguma comparação não aprendida, sua natureza e seu resultado, mais contagem de votos descritiva. **Não fazer meta-análise:** métricas, ataques e regimes são heterogêneos demais.
3. **QP3:** distribuição do orçamento de aprendizado efetivo; quais estudos analisam horizonte.
4. **QP5:** distribuição dos sinais por exposição de privacidade e custo; quantas defesas exigem reconstrução de dados ou dataset raiz no servidor.
5. **QP6:** mapa de qualidade (QA1–QA9) por estudo; frequência de vazamento de teste e de avaliação com ataque adaptativo.
6. **QP7:** síntese narrativa das auditorias e dos baselines simples em RL e em FL robusto.
7. **Agenda de lacunas:** o que a literatura não avalia ou não isola.
8. **Decisões internas (fora do artigo):**
   - **Portão N:** aplicar o critério do §2 e registrar o veredito com os estudos que o sustentam.
   - **Portão R:** listar os requisitos e os baselines obrigatórios para o GRADF-v2, a partir das QP4–QP6 e do §9.2.

## 13. Leituras canônicas para QP7 (inclusão direta, fora da busca)

Conferir as citações completas antes de usar:
- Henderson et al., *Deep Reinforcement Learning that Matters*, AAAI 2018 (variância entre sementes e reprodutibilidade em deep RL).
- Agarwal et al., *Deep Reinforcement Learning at the Edge of the Statistical Precipice*, NeurIPS 2021 (estatística com poucas sementes).
- Mania, Guy e Recht, *Simple Random Search Provides a Competitive Approach to Reinforcement Learning*, NeurIPS 2018 (baseline simples iguala deep RL).
- Rajeswaran et al., *Towards Generalization and Simplicity in Continuous Control*, NeurIPS 2017 (políticas lineares competitivas).
- *Adaptive Adversaries in Byzantine-Robust Federated Learning: A Survey*, IACR ePrint 2025/510 (ponto de partida do snowballing em FL robusto).

## 14. Ameaças à validade

- **Construção:** termos como "adaptive aggregation" sem "reinforcement" ficam fora de S1 por desenho. O snowballing e a lista de adaptativos não-RL (EC2, §9.2) mitigam isso.
- **Seleção:** a triagem principal é feita por um revisor. Mitigações: calibração prévia, amostra de 20% triada às cegas pelo revisor 2 com κ inter-avaliador, e conferência de todas as exclusões na fronteira IC3/EC2. Se o revisor 2 não estiver disponível, o κ será intra-avaliador, e isso será declarado.
- **Extração:** campos que exigem cálculo (orçamento efetivo) ou inferência (vazamento de teste, fidelidade dos ataques) são marcados `?` quando o texto e o código não permitem decidir. Nunca são inferidos.
- **Publicação:** estudos com resultado "o RL não ajudou" tendem a não ser publicados. Preprints são incluídos, e a ausência é registrada como achado possível, não como prova.
- **Temporal:** a área muda rápido. Registrar a data da busca e repetir S1 (só registros novos) antes da submissão do artigo.
- **Viés de confirmação:** a hipótese interna (§1.2) é conhecida pelo revisor 1. Mitigações:
  - o critério do Portão N foi fixado antes da busca (§2);
  - a extração de QP2 registra também os estudos em que o agente vence;
  - o revisor 2 confere as fichas QP2 de todos os estudos em que `comparacao_nao_aprendida ≠ nenhuma`.

## 15. Registro, versões e adendos

### 15.1 Registro
- Plataforma: OSF (projeto novo, registro do tipo "Preregistration" ou "Open-Ended Registration").
- DOI ou link do registro: não realizado (adendo A2).
- Data do registro: não realizado (adendo A2). A busca definitiva foi executada em 2026-09-28 sem registro prévio.

### 15.2 Histórico de versões
- **1.1 (2026-09-27):** versão consolidada para registro. É o único documento de referência.

### 15.3 Adendos após o registro

| data | seção | mudança | motivo |
|---|---|---|---|
| 2026-09-28 | cabeçalho, §8.5–8.8, §10, §14 | (A1) Não há revisor 2. Calibração, κ, conferência das exclusões IC3/EC2, 20% das inclusões e 20% da qualidade são feitos pelo revisor 1 na forma do §8.10 (retriagem às cegas após ≥ 7 dias, κ intra-avaliador). | Indisponibilidade de segundo revisor; declarado como limitação |
| 2026-09-28 | §15.1 | (A2) O protocolo não foi registrado no OSF antes da busca. | Decisão do autor; declarar no artigo como protocolo não pré-registrado |
| 2026-09-28 | §6.1, §6.2 | (A3) Bloco B ampliado (reinforcement, bandit*, multiarmed, RL, DRL, MARL, "Q learning", DDQN, "actor critic", "policy learning", "policy optimization", "upper confidence bound", UCB, "Thompson sampling", MDP) e bloco C ampliado (untrust*, sybil, "free-rid*", selfish). No arXiv, campo `all`. Strings exatas em `buscas_strings_S1_S2.md`. | Validação §6.4 da S1 original reprovou (4/5 no QGS); a revisada recuperou 5/5 |
| 2026-09-28 | §6.3 | (A4) S2 dividida em S2a (RL ∧ auditoria ∧ FL) e S2b (FL robusto ∧ auditoria/avaliação, sem bloco de RL), executadas no Scopus, IEEE, ACM e arXiv. | A S2 original retornou 4 registros no arXiv, nenhum útil à QP7 |
| 2026-09-28 | §6.2, §11.2 | (A5) ACM: a ferramenta não aceitou OR entre campos; foram feitas duas consultas (Abstract; Title), sem Keywords. IEEE: B1 e B2 numa única consulta. Scopus: exportação em 3 lotes (mais recentes, mais antigos, só 2024) por limite de 2.000 registros. Web of Science não executado. | Limitações das interfaces; WoS é complementar (§5) |
| 2026-09-28 | §8.6, §11.1 | (A6) Códigos de decisão adicionais: E-ICn (falha em critério de inclusão), E-PER (anterior a 2017), E-IC5 (tese), Q7-I/Q7-D/Q7-E (fluxo QP7), `nao_recuperado`; métodos de decisão `leitura_manual`, `herdado:<id>` e `regra` na etapa 1. | Rastreabilidade de exclusões que não se encaixam em EC1–EC7 |
| 2026-09-28 | §3 (QP7), §8 | (A7) Critério operacional da QP7: incluem-se auditorias, avaliações, benchmarks ou SoKs de defesas de FL robusto ou de defesas por RL em FL, com prioridade para os que tratam de prática de avaliação ou baselines simples; surveys só se tiverem estudo experimental. Leituras do §13 incluídas diretamente. | O protocolo não definia critério de elegibilidade para a QP7 |
| 2026-09-28 | §8.9 | (A8) Registros achados no snowballing e ausentes da base recebem ids SB-xx. FedDive (KAIS 2025) e Zhang et al. (Neurocomputing 2024) não foram recuperados. | Rastreabilidade |
| 2026-09-28 | §7 (IC4), §9.1 | (A9) Um PDF corrompido (HICSS 2023) teve o texto recuperado por leitura direta dos streams; o livro de anais do V2-3494 foi lido só no capítulo 37. | Recuperação do texto completo |
| 2026-09-28 | §9.1, §10, §14 | (A10) Triagem, leitura e extração foram feitas com assistência de IA (Claude), sob supervisão e validação do revisor 1. O QA1–QA9 (exceto QA6) é derivado por regra explícita dos campos da extração; campos que o texto não informa são codificados como "não reportado" (N) e "?" fica reservado a ambiguidades reais. | Transparência e reprodutibilidade |
| 2026-09-28 | §14 (temporal) | (A11) A repetição da S1 antes da submissão fica dispensada se a submissão ocorrer poucas semanas após a busca (2026-09-28); a data da busca será declarada. | Intervalo curto entre a busca e a submissão |
| 2026-10-05 | §8.5 | (A12) Calibração com o revisor 2 estratificada pela decisão do revisor 1: 10 registros "segue" (I/D) e 10 "exclui", em ordem aleatória (semente 20261005; `scripts/amostra_revisor2.py`). A amostra do κ (§8.7) continua sendo sorteio simples de 20% dos registros restantes. | O sorteio simples resultou em 20 exclusões, inútil para discutir a fronteira dos critérios |
| 2026-10-06 | cabeçalho, §8.5–8.7, §14 | (A13) Um revisor 2 passou a participar, o que substitui o A1 na confiabilidade da etapa 1. **Calibração:** 20 registros (A12); depois dela, o revisor 2 recebeu regras de precedência entre os códigos de exclusão (E-PER → IC1 → EC5 → EC1 → EC4 → EC3 → IC2 → EC2 → IC3 → demais), com a fronteira EC2/IC3 explicitada: EC2 só para defesa que se adapta ao longo das rodadas sem RL; defesa estática é IC3. **Amostra cega:** 811 registros (20% dos 4.054 da S1). *Nota (2026-10-22):* o tamanho foi calculado sobre os 4.054 registros da S1, arredondado para cima, e não sobre os registros restantes, como o A12 sugere; o sorteio, com semente fixa, foi feito entre os 4.034 que restaram depois de retirar os 20 de calibração (`scripts/amostra_revisor2.py`). Nas linhas 106–250, as decisões do revisor 2 estavam deslocadas uma linha (a avaliação pulou a linha 106); elas foram realinhadas com a anuência do autor, e o revisor 2 decidiu a linha 106 de novo (original preservado em `revisor2/triagem_cega_revisor2_antes_realinhamento.xlsx`). **Resultado:** κ entre avaliadores = 0,737; concordância de 98,6%; PABAK = 0,973 (`scripts/kappa_revisor2.py`). **Consenso** das 11 divergências (aba Consenso): o corpus não mudou (V2-1103 e V2-0590 continuam I); V2-1180 teve o código da etapa 2 alterado de E-IC3 para E-IC2; V2-1031 e V2-0083 seguem como D para o texto completo. A conferência das exclusões IC3/EC2 e de 20% das inclusões (§8.8) e a pontuação de 20% da qualidade (§10) continuam pendentes. | Entrada de um segundo revisor |
| 2026-10-09 | §3 (QP2, QP3), §9.1, §10, §14 | (A14) **Conciliação da extração.** O revisor 1 fichou de forma independente 77 dos 78 estudos da S1 (QP1–QP6; falta o V2-3494) (`selecionados/Fechamento - PDF/`), e o fichamento foi comparado campo a campo com a extração assistida por IA (`validacao/comparacao_fichamento_autor_vs_claude.md`). A concordância foi alta nos campos factuais (código 97%, modo 93%, vazamento 90% quando ambos decidem, sementes 88%) e baixa na QP2 (52%; κ ≈ 0,41), no horizonte e no orçamento, sobretudo porque a extração assistida estava incompleta. As divergências relevantes foram conferidas no texto completo e aplicadas em `revisao_extracao.tsv`. **Critérios operacionais fixados:** (i) **política não aprendida** (QP2) é uma política dentro do espaço de ação do próprio agente (ação fixa, aleatória, regra sobre o mesmo sinal ou oráculo); agregadores robustos externos, algoritmos de FL e treino centralizado não contam; uma ação fixa que equivale a não defender (aceitar todos, pesos iguais) é registrada como fixa, mas analisada à parte. (ii) **Análise de horizonte** (QP3) é a medida do ganho do agente sobre a política não aprendida em função do número de rodadas; curvas de convergência, sensibilidade de γ e limites teóricos não contam. (iii) **Orçamento calculável** (QA7) exige parâmetros do agente (passos, episódios, lr, γ etc.); os do treino local dos clientes não bastam. (iv) **Código** em material suplementar do periódico conta como P. (v) Conjunto do servidor amostrado do pool de teste conta como vazamento parcial (P) quando a recompensa não o usa diretamente ou quando é disjunto da avaliação final. **Efeito:** sem comparação não aprendida 35 → 26; mesmo sinal 5 → 7; QA médio 2,83 → 3,28; Portão N mantido ("parcialmente mostrado"). | Validação da extração pelo revisor 1 |
| 2026-10-13 | §3 (QP7), §7, §8, §9 | (A15) **Conciliação da QP7.** O revisor 1 fichou os 37 estudos da QP7 (`selecionados/Fechamento_QP7 - PDF/`), e o fichamento foi comparado com a análise assistida (`validacao/comparacao_QP7_autor_vs_claude.md`). Decisões por consenso: **V2-0870** sai por EC7 (versão anterior de V2-4764); **V2-0988** sai pelo A7 (pesquisa original, não avaliação); **SB-06** sai pelo A7 (survey sem experimento próprio). A QP7 passa a 34 estudos (25 pela busca, 4 pelo snowballing, 5 canônicas). As leituras por estudo foram registradas numa ficha própria, `triagem_v2/extracao_qp7.csv` (tipo, escopo, baseline simples, padrão, armadilhas, menção a defesa por RL, sementes, teste estatístico, achado), com a classificação de armadilhas do revisor 1 (várias por estudo). **V2-1301 (Justinian's GAAvernor)**, defesa por RL citada por três incluídos da S1 e auditada em V2-4764, entrou só pela S2a e não fora avaliado para a S1: é **excluído da S1 por IC1** (sistema de aprendizado distribuído com servidor de parâmetros, não federado), decisão do revisor 1. | Validação da QP7 pelo revisor 1 |
| 2026-10-13 | §8.8, §10, §14 | (A16) **Conferência do revisor 2 na etapa 2.** O R2 conferiu, às cegas, as 36 exclusões da etapa 2, 16 inclusões (20%), a QP2 dos 52 estudos com comparação e a qualidade de 16 estudos (`revisor2/validacao_cega_revisor2_v4.xlsx`). Parte foi feita sem o texto completo (dois casos declarados "PDF ausente", decisões que reproduzem o resumo). **Concordância antes do consenso:** inclusão/exclusão (n = 52) 65,4%, κ = 0,35, PABAK = 0,31 (exclusões: 20/36 na decisão binária, 15/36 no código exato; inclusões: 14/16); QP2, categoria da comparação (n = 52) 34,6%, κ = 0,14; qualidade (16 × 9) 43%, κ = 0,15. **Consenso** (`revisor2/consenso_etapa2.csv`): V2-1215 e V2-1239 revistos pelo R2 com o PDF (E-EC2 e E-IC3); nos demais, o R2 aceitou as decisões do R1 com base no texto completo. O corpus não mudou (78 estudos; nenhuma exclusão revertida; V2-1041 e V2-1483 mantidos). | Conferência do §8.8 e do §10 |
| 2026-10-13 | §8.8, §11.4 | (A17) **Texto completo de V2-1031 e V2-0083** (enviados à etapa 2 pelo consenso do A13). Na etapa 1 passam de E-IC2 a D (decisão manual de consenso, `decisoes_s1_manuais.tsv`). Na etapa 2: **V2-1031 → E-EC1** (o agente RDPG é o atacante; a defesa é um detector GRU federado com atenção e DP, sem RL); **V2-0083 → E-IC3** (o protótipo só implementa top-k por cosseno + quarentena; o agente de RL é conceitual, sem avaliação). PRISMA da S1: textos completos buscados 122 → 124, avaliados 118 → 120, excluídos na etapa 2 42 → 44; E-IC2 na etapa 1 224 → 222; incluídos 78 (sem mudança). | Conclusão das pendências do A13 |
| 2026-10-16 | §9.1, §10 | (A18) **Fichamento do V2-3494.** O revisor 1 fichou o único estudo da S1 que faltava no A14 (`Wen-Et-Al-2025 ... TD3.pdf`), e a conciliação seguiu os critérios do A14. Corrigidos: nº de clientes (100) e exigência do sinal ("só updates" → dados no servidor não especificados, pois a recompensa é a acurácia do modelo global calculada no servidor); acrescentado o DOI. Mantidos: QP2 "nenhuma" (FedAvg, Krum e MKrum rodam sem o filtro por distância que precede o agente, fora do espaço de ação), sinal = distâncias euclidiana e cosseno (a acurácia é a recompensa), estado "?" (não definido no texto) e memória N (o replay pool é do TD3). Efeito: QP5 só updates 28 → 27, dados no servidor 45 → 46 (teste 17 inalterado); QP2, qualidade e média do QA (3,26) inalterados. Registro em `revisao_extracao.tsv`. |
| 2026-10-17 | §10, §8.8, §14 | (A19) **Regra do QA8 e reclassificação pelo R2.** (i) A família "defesa com dados no servidor" do QA8 passa a incluir só defesas que usam dados no servidor (FLTrust, Zeno, dataset raiz ou validação do servidor); FLAME, FLDetector e FLGuard, que a regra contava por engano, saem. Efeito: V2-1178 e V2-1327 passam de QA8 = S para P; QA8 com as duas famílias 13 → 11; QA médio 3,26 → 3,25. (ii) Em resposta ao parecer sobre a baixa concordância na QP2 e na qualidade, as regras aplicadas pelo R1 foram escritas num livro de códigos (`validacao/livro_codigos_v2.md`), sem criar regras novas, e o R2 refaz às cegas, com os textos completos, a classificação da QP2 dos 52 estudos com comparação e a qualidade de 26 estudos (os 16 da amostra anterior e 10 novos, estratificados pela categoria da QP2). As classificações do R1 são as já existentes; a concordância é medida contra elas, antes do consenso. (iii) Análise de sensibilidade das contagens centrais em `validacao/sensibilidade_qp2_qa.md` (`scripts/sensibilidade.py`). | Resposta ao parecer (confiabilidade) |
| 2026-10-19 | §9.1, §10, §12 | (A20) **Consenso após a qualidade do R2 (livro de códigos v2).** (i) **QA7:** o S passa a exigir o volume de treino do agente (passos, episódios, iterações ou rodadas) e ao menos um parâmetro de otimização (taxa de aprendizado, γ, replay ou batch), como o livro de códigos já descrevia. A regra derivada do R1 aceitava uma única palavra-chave. A extração do V2-0351 foi completada (λ = 0,2, ζ = 0,85, ε decrescente; Sec. V-C). Efeito: 18 estudos passam de S para P, e o QA7 fica com 22 S, 48 P e 8 N. (ii) **Referências sem ação defensiva:** FedAvg, média simples e aceitar ou selecionar todos os clientes não são políticas de defesa, nem dentro do espaço de ação do agente. A exceção "não defender" do livro de códigos é revogada. V2-1178, V2-0945, V2-1030 e V2-3265 passam de fixa para nenhuma, e V2-0837 e V2-0940 passam de fixa para aleatória. V2-0350 (λ fixo do Ditto e local-only) e V2-1130 (auditoria fixa) seguem como fixa e entram nas comparações mais próximas. No V2-0350, o local-only supera o agente em F1 nos três cenários (Tab. 1), o que conta como empate ou derrota. Efeito de (ii) na QP2: sem comparação 26 → 30, aleatória 14 → 16, fixa 16 → 10, referência forte 34 → 28, comparações mais próximas 15 → 17, empates 5 → 6. As conclusões A–E da sensibilidade se mantêm. (iv) **QA1:** se a recompensa e a seleção não usam nenhum dado de avaliação do modelo, e isso está escrito, o critério é S. É o caso do V2-1041, que usa métricas de infraestrutura e votos com os modelos locais e fica com S. O V2-1294 fica com P, porque a Sec. 3.1.3 fala em proxy e a Sec. 5 em teste. O V2-2573 passa de S para P, porque o conjunto de Δacc e Δloss da recompensa não é declarado; nas notas, registra-se que a recompensa usa o rótulo verdadeiro dos maliciosos. (v) **QA6:** avaliam-se os ataques contra os quais a decisão do agente é testada. S exige parâmetros, fração e momento verificáveis em todos eles, e um ataque próprio ou genérico precisa ter os três documentados. Os "?" do R2 ficam com P, como no R1. No V2-1041, o agente (MTD) só enfrenta o ATTS1, que é um ataque próprio sem fração nem momento. No V2-0160, o LBR segue Yao et al., mas sem fração clara nem rodadas de injeção. No V2-0351, o ataque bizantino é genérico, sem a distribuição dos dados falsificados. No V2-1229, a fração é 20% (variada de 0,1 a 0,48), mas o LIE usa z = 0,3 fixo, fora da regra original, e o momento não é declarado. (vi) **Ablações:** uma ablação que remove o agente sem pôr no lugar uma decisão defensiva é "nenhuma". A "ablação parcial" fica para quando outra decisão ocupa o lugar do agente sem ser descrita. O V2-1041 fica com nenhuma: a Tab. XII só desliga a MTD, e os autores deixam a comparação com mutação não aprendida para trabalho futuro. O V2-2890 vai de parcial para nenhuma, porque o BlockFL é um baseline externo sem decisão substituta. O V2-4233 vai de parcial para aleatória, porque o HSFL original seleciona ao acaso. O V2-1105 (variante sem agendamento) e o V2-3555 (seleção heurística) continuam como parcial. Efeito na QP2 somando (ii) e (vi): sem comparação 26 → 31, aleatória 14 → 17, parcial 4 → 2. (vii) **QA9:** S quando o adversário usa o conhecimento da defesa avaliada para ajustar o ataque contra pelo menos um componente dela, mesmo sem mirar o pipeline completo. O V2-4339 passa de P para S, porque o adversário divide os maliciosos para escapar do ISA (Sec. 5.1), e o QA9 = S passa de 4 para 5. Com (iv)–(vii), os 11 "?" do R2 ficam resolvidos. Efeito de (i)–(vii) na qualidade: média 3,25 → 3,06, e estudos com ≥ 5 pontos 12 → 11. (iii) A concordância R1 × R2 é reportada contra a classificação anterior ao consenso (`validacao/reclassificacao_R2/qualidade_R1_antes_A20.csv` e `extracao_principal_R1_antes_A20.csv`). Qualidade: 79,4%, κ = 0,67, κ ponderado = 0,72 (26 × 9). | Consenso R1 × R2 (qualidade) |
| 2026-10-21 | §9.1, §12 | (A21) **Consenso da QP2 após a reclassificação cega do R2** (`validacao/reclassificacao_R2/analise_qp2_R2v2.md`; concordância calculada contra a extração do R1 antes do A20: categoria κ = 0,49, discutido κ = 0,00). Regras fixadas no livro de códigos (cópia do R1; a do R2 fica como estava): (i) **texto × números:** no critério de empate, os números prevalecem, e a descrição dos autores só decide sem números legíveis ou dentro do erro de leitura da figura; (ii) **métrica principal:** a utilidade do modelo global sob ataque, salvo no ataque dirigido (ASR ou acurácia na classe atacada) e quando não há comparação em utilidade (métrica da decisão do agente); custo, tempo e convergência são secundários; (iii) **discutido como achado (§2.5):** leitura literal, isto é, os autores comentam o resultado e tiram dele uma conclusão em qualquer direção, e sem comparação o código é N; a pergunta do Portão N (os autores reconhecem que a política não aprendida iguala ou supera o agente, e o que concluem disso) passa a ser registrada à parte, nos empates contra o mesmo sinal ou a ação fixa. **Efeito:** V2-4540 de vitória clara para empate; V2-1102 de empate para vitória estreita; V2-0351 de vitória clara para vitória estreita, medida contra a seleção direta; discutido = S em quase todos os estudos com comparação; categorias revistas a favor do R2 em V2-2188 (nenhuma: método de outro artigo sem ação defensiva), V2-4266 (aleatória: o secure-UCB ideal é aprendido), V2-3243 e V2-3331 (ablação parcial: a regra substituta não é descrita); nas outras divergências o R1 se mantém pelo livro de códigos. Com o A22, a QP2 fica com 32 sem comparação, 45 com, 23 com referência forte, 6 com o mesmo sinal e 6 empates em 14 comparações mais próximas; conclusões A–E mantidas em todos os cenários, inclusive o do R2; Portão N mantido ("parcialmente mostrado"). | Reclassificação cega do R2 |
| 2026-10-21 | §7 (IC4), §11.4 | (A22) **V2-1120 (TARS) excluído por IC4 na extração.** Os autores declaram que os números das tabelas de resultado são "consistent with cited literature or derived by careful synthesis of referenced figures" e "validated against published references", inclusive na linha do próprio método; não há hiperparâmetros do agente, número de execuções, modelo nem framework, e os valores atribuídos ao SARA divergem do artigo original (V2-0111). Não há avaliação empírica verificável, e a comparação com as regras fixas não é controlada. A ficha fica nos dados e o estudo sai da síntese. **Efeito:** S1 de 78 para 77 estudos; com comparação não aprendida 47 → 46; referência forte 28 → 27; comparações mais próximas 17 → 16 (sai uma vitória estreita); empates (6) e mesmo sinal (7) inalterados; conclusões A–E da sensibilidade mantidas. A concordância R1 × R2 já calculada continua com o estudo, porque mede a codificação antes do consenso. | Achado na conciliação do §2.5 (A21) |
| 2026-10-22 | §10 (QA5) | (A23) **QA5 graduado pela força da referência, em resposta à Q15 da revisão.** O oráculo usa informação indisponível ao agente, fica fora de Π0 (seção 2.4 do paper) e não estima Δ_L, e por isso passa de S para P. Uma ação fixa sem ação defensiva não conta para o S (A20). S fica com a ação fixa que é uma defesa e a heurística sobre o mesmo sinal; P, com aleatória, outro sinal, oráculo e ablação parcial. Efeito: V2-0383 e V2-1275 passam de S para P (o V2-0111 continua S pela comparação com cada regra fixa); QA5 17/28/32 → 15/30/32; média de qualidade 3,01 → 3,00. As categorias da QP2 não mudam. O κ da qualidade (0,67) é calculado contra o R1 antes do consenso e não muda. Na mesma data, na conferência da Q16, o QA2 do SB-03 foi corrigido de S para P pela regra já vigente: há média ± dp entre sementes, mas o número de sementes não é informado, como no V2-1327 (P). Efeito: QA2 14/11/52 → 13/12/52; média 3,00 → 2,99; estudos com ≥ 5 pontos 10 → 9; no funil, mesmo sinal com ≥ 3 sementes 2 → 1 (só o V2-2103). | Q15 da revisão do paper; incoerência entre a rubrica e a definição de Π0 (Q14) |
| 2026-10-22 | §10 (QA4) | (A24) **QA4 pontua acessibilidade e suficiência do código, e não o local de hospedagem** (Q18 da revisão do paper). S: código acessível sem intermediação, em repositório público ou no suplemento do periódico, com o agente e o experimento (ataques e configuração); P: acessível mas incompleto, ou declarado sem acesso direto (pedido, sem link, link quebrado); N: sem código declarado. Os 14 estudos que declaravam código foram conferidos abrindo os links em 22/10/2026 (`validacao/conferencia_codigo_QA4.md`). V2-1042 S→P (sem a simulação dos clientes maliciosos), V2-0987 S→P (repositório inexistente), V2-0688 e V2-1057 P→N (o suplemento IEEE é de apêndices, e o artigo não declara código; se o suplemento tiver o código completo, passam a S). QA4 11/3/63 → 9/3/65; média 2,99 → 2,97; estudos com ≥ 5 pontos 9 → 8. O κ da qualidade é calculado contra o R1 antes do consenso e não muda. | Q18 da revisão do paper; o local de hospedagem não mede reprodutibilidade |
| 2026-10-22 | §3 (QP7), §8, §13 | (A25) **Grupos da QP7 explicitados nos critérios** (Q20 da revisão do paper). Q7a: auditorias, avaliações e benchmarks de defesas em FL robusto ou de defesas por RL em FL (critério do A7), recuperados pela S2 e pelo snowballing; surveys só com estudo experimental. Q7b: exceção para trabalho fora de FL que avalia um método aprendido sob adversários bizantinos com um protocolo que o corpus não aplica, incluído só como exemplo metodológico; aplica-se ao V2-3771 (recuperado pela S2 no Scopus), que na conciliação da QP7 (A15) estava contado entre os trabalhos de FL e foi reclassificado como exceção na resposta à Q10, sem adendo até esta data. Q7c: leituras canônicas do §13. Composição inalterada: 28 + 1 + 5 = 34. Nenhum grupo conta nas QP1–QP6. | A exceção do V2-3771 era aplicada sem estar nos critérios |
| 2026-10-22 | §8.9 | (A26) **Segunda iteração do snowballing completada para a síntese principal** (Q21 da revisão do paper). A segunda iteração, para trás, tinha partido só dos 29 trabalhos da QP7 (25 da busca secundária e 4 do snowballing). Os dois incluídos na síntese principal pela primeira iteração, R2Fed (V2-0945) e FedCHO (SB-03), passaram pelo mesmo procedimento em 22/10/2026: 94 referências (27 e 67), triadas por título com os critérios da S1; nenhuma é candidata nova (a única defesa por RL citada, FedAA, já é o V2-1254). Registro em `validacao/snowballing_iteracao2_R2Fed_FedCHO.csv`. O corpus não muda. | Wohlin exige iterar a partir de todos os novos incluídos |
| 2026-10-22 | §9.1, §12 | (A27) **O oráculo sai da precedência das referências admissíveis** (revisão do paper, coerência com Π0). O oráculo usa informação indisponível ao agente, fica fora de Π0 e não estima Δ_L, e por isso não pode deslocar uma referência admissível na categoria da QP2. Nova precedência: mesmo sinal → fixa → outro sinal → aleatória → parcial → oráculo → nenhuma (`scripts/sintese.py`, `fig_funil.py`). A comparação com oráculo continua registrada no campo da extração e na Tab. QP2. **Releitura do V2-0111 (SARA):** as regras fixas (Krum, TrimmedMean, Median, cada uma sozinha) são braços do próprio bandit e constituem defesa; o SARA é "comparable" à Median no ataque periódico (MNIST e CIFAR-10) e fica próximo do Krum no ataque de fingimento no MNIST, superando-o no CIFAR-10 só em figura → **empate** pelo critério do A21 (não vence em todos os regimes). **Efeito:** V2-0111 oráculo → fixa (empate); V2-1275 oráculo → aleatória; V2-0383 continua oráculo. Categorias: fixa 8 → 9, aleatória 18 → 19, oráculo 3 → 1. Comparações mais próximas 14 → 15 (6 mesmo sinal + 9 fixa), empates 6 → 7, vitórias 8. Inalterados: 45 com comparação, 23 com ação fixa, heurística ou oráculo (etapa 3 do funil passa a contar qualquer comparação com oráculo), QA5 (o V2-0111 já era S pela ação fixa) e demais QA. A concordância R1 × R2 reportada continua calculada com a regra vigente na época (A21). | Coerência entre a categoria da QP2 e a definição de Π0 |

---

## Anexo: roteiro operacional

**Antes da busca**
1. [ ] Definir o revisor 2 e preencher o cabeçalho.
2. [ ] Rodar S1 no Scopus e checar Q1–Q5 (§6.4). Ajustar a string se preciso.
3. [ ] Registrar o protocolo no OSF (§15.1).

**Busca e triagem**
4. [ ] Rodar S1 em todas as bases; exportar tudo; preencher o log (§11.2).
5. [ ] Deduplicar (§8.4).
6. [ ] Calibrar com o revisor 2 em 20 registros (§8.5).
7. [ ] Etapa 1 pelo revisor 1; amostra de 20% às cegas pelo revisor 2; calcular o κ (§8.6–8.7).
8. [ ] Etapa 2; o revisor 2 confere as exclusões IC3/EC2 e 20% das inclusões (§8.8).
9. [ ] Snowballing, começando pela busca para frente de AdaAggRL, FedAA, TARS e FedStrategist (§8.9).

**Extração e síntese**
10. [ ] Extrair (§9.1) e preencher a ficha reduzida dos não-RL (§9.2).
11. [ ] Avaliar a qualidade (§10); o revisor 2 pontua 20%.
12. [ ] Rodar S2 e incluir as leituras canônicas (§13) para QP7.
13. [ ] Sintetizar (§12); registrar os vereditos dos Portões N e R.
14. [ ] Antes da submissão: repetir S1 com os registros novos (§14, temporal).

**Entregáveis:** `slr_resultado.md`, as planilhas (§11.1, §11.3), o log (§11.2), o fluxo PRISMA (§11.4) e o pacote suplementar (§11.5).
