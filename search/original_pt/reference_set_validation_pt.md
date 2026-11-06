# Validação da string S1 contra o QGS (§6.4)

**Data:** 2026-09-28 · **Executor:** revisor 1 (assistido) · **Scripts:** `scripts/validar_qgs.py`, `scripts/busca_arxiv.py`

## 1. Resultado

**Critério:** Q1–Q5 recuperados na união das bases (sensibilidade 5/5).

| # | trabalho | ACM | IEEE | Scopus | arXiv (S1 atual) | arXiv (S1 revisada) |
|---|---|---|---|---|---|---|
| Q1 | AdaAggRL (2406.14217) | — | — | — | **não** | sim |
| Q2 | FedAA (2402.05541) | ACM-024 | — | SCO-0388 | **não** | sim |
| Q3 | FedDRLPD (KBS 2026) | ACM-002 | — | SCO-0071 | (não está no arXiv) | — |
| Q4 | TARS (IEEE 11215089) | — | IEEE-003 | SCO-0629 | (não está no arXiv) | — |
| Q5 | FedStrategist (2507.14322) | — | — | — | sim | sim |
| B1 | AdaBFL (controle, não-RL) | — | — | — | não | não |
| B2 | Learning to Attack FL (controle, RL do atacante) | ACM-016 (E-EC1) | — | SCO-2242 (E-EC1) | — | — |

**S1 atual: 4/5 (Q1 ausente em todas as bases) → REPROVADA.**
**S1 revisada (proposta abaixo): 5/5 na união → aprovada no arXiv;** ainda precisa ser reexecutada em ACM, IEEE e Scopus.

Os controles se comportaram como esperado: B2 aparece e cai por EC1; B1 (defesa adaptativa sem RL) não é recuperado. Isso é
coerente com o desenho da string e deve ser coberto pelo snowballing e pela lista §9.2.

## 2. Diagnóstico

### 2.1 Q1 (AdaAggRL) não contém nenhum termo do bloco B
O resumo diz apenas "**RL-based** Adaptive Aggregation" e "**policy learning**". O bloco B exige "reinforcement learning",
siglas de algoritmos (DQN, TD3…) ou "multi-armed/contextual bandit". A falha é de **sensibilidade da string**, e se
repete em qualquer base.

### 2.2 Variações de termo nos incluídos (8 de 65 incluídos únicos não casariam com a S1 pelo título + resumo)
Entraram nos exports por metadados extras (IEEE Terms, palavras-chave indexadas), não pela string:

| registro | termo usado | termo da S1 que falhou |
|---|---|---|
| IEEE-003 (TARS, Q4) | "Q learning" (sem hífen) | "Q-learning" |
| IEEE-026 (SARA) | "Upper Confidence Bound (UCB)" | — (não há) |
| SCO-0001 | "UCB" | — |
| IEEE-138 | "multiarmed bandits", "Thompson Sampling" | "multi-armed bandit" |
| IEEE-093 | "deep reinforcement algorithm" | "reinforcement learning" |
| IEEE-206 | "actor–critic" (meia-risca) | "actor-critic" |
| SCO-1466 | "DRL" | — |
| SCO-1308 | "untrusted nodes" (bloco C) | — |

### 2.3 Limitação específica do arXiv
Na API do arXiv, `abs:"reinforcement learning"` **não recupera Q1 nem Q2**, embora ambos tenham o termo no título/resumo
(testado por interseção `id_list` + `search_query`). A frase exata no campo `abs` é pouco confiável; termos não
aspeados (`abs:reinforcement`) e o campo `all:` funcionam.

## 3. String revisada (proposta)

Blocos em notação genérica (adaptar a sintaxe por base, como no §6.2):

- **A (FL):** inalterado — `"federated learning" OR "federated optimization" OR "federated averaging"`
- **B (RL e bandits):** `reinforcement OR bandit* OR multiarmed OR RL OR DRL OR MARL OR "Q-learning" OR "Q learning" OR DQN
  OR DDQN OR DDPG OR TD3 OR PPO OR "actor-critic" OR "actor critic" OR "policy gradient" OR "policy learning"
  OR "policy optimization" OR "upper confidence bound" OR UCB OR "Thompson sampling" OR LinUCB OR "Markov decision process" OR MDP`
- **C (adversário e defesa):** o bloco atual + `OR untrust* OR sybil OR "free-rid*" OR selfish`

**arXiv:** usar a string revisada nos campos `abs` (resultado: 67 registros) ou `all` (68; +1 registro). Recomenda-se `all`,
pela limitação do §2.3. Strings exatas: `string_arxiv_revisada.txt` e `string_arxiv_revisada_all.txt`.

Custo estimado: no arXiv, a revisão passou de 27 para 67–68 registros. Nas outras bases, "RL", "reinforcement" e
"bandit*" devem aumentar o volume, mas o bloco A ∧ C limita o ruído.

## 4. Consequências para o protocolo (decisão do autor)

1. **Adendo no §15.3** (texto sugerido):
   > 2026-09-28 · §6.1/§6.2 · Bloco B ampliado (reinforcement, bandit*, multiarmed, RL, DRL, MARL, "Q learning", DDQN,
   > "actor critic", "policy learning", "policy optimization", "upper confidence bound", UCB, "Thompson sampling", MDP)
   > e bloco C ampliado (untrust*, sybil, "free-rid*", selfish). No arXiv, busca no campo `all`. · Validação §6.4 da S1
   > original recuperou 4/5 do QGS (Q1/AdaAggRL não contém termos do bloco B; usa "RL-based" e "policy learning").
2. **Reexecutar a S1 revisada** no Scopus, no IEEE e na ACM, e depois triar apenas os registros novos. As decisões atuais
   são reaproveitadas por título.
3. **Registro OSF (§15.1):** as buscas em ACM, IEEE e Scopus foram feitas antes desta validação. Se o registro ainda não
   foi feito, a ordem correta é: aplicar o adendo → registrar → buscar novamente (definitivo). Se já foi feito, declarar
   o adendo com data.
4. **Scopus:** conferir a string executada (2.220 dos 2.978 registros não mencionam FL; há registros de 2016 apesar de
   `PUBYEAR > 2016`).
5. **Log de buscas:** `triagem/log_buscas.csv` foi criado. Faltam as strings exatas de ACM, IEEE e Scopus (colunas
   marcadas "a preencher").

---

# Validação da S2 (§6.3) — 2026-09-28

O protocolo não define QGS para a S2; o conjunto de validação abaixo foi montado nesta data e é declarado como tal.

**S2 original (RL ∧ auditoria ∧ FL):** sintaxe OK; recupera os alvos do corpus SCO-0005 (ablação do RL) e SCO-0133
(compara com UCB/Thompson). No arXiv (campo `all`), porém, retornou **4 registros, nenhum útil à QP7** (8 na forma com o
bloco de RL revisado). Diagnóstico: a interseção RL ∧ auditoria ∧ FL é quase vazia. Das leituras do §13, a S2 não recupera
nenhuma (o bloco 3 as exclui por desenho, e Mania, Agarwal e Rajeswaran nem casam com o bloco 2); elas continuam por
inclusão direta. As auditorias de **FL robusto** não mencionam RL e ficam de fora. **Veredito: REPROVADA como está.**

**S2 revisada = S2a ∪ S2b**
- **S2a** (auditoria de defesas de FL com RL): S2 original com os blocos 1 e 2 ampliados. Recupera SCO-0005, SCO-0028, SCO-0033, SCO-0133.
- **S2b** (auditoria/avaliação de FL robusto, sem exigir RL): `"federated learning" ∧ (poisoning ∨ byzantine ∨ backdoor ∨
  "robust aggregation") ∧ (reproducib* ∨ "sanity check" ∨ "simple baseline*" ∨ benchmark* ∨ "empirical evaluation" ∨
  pitfall* ∨ revisit* ∨ rethink* ∨ "fair comparison" ∨ systematization ∨ SoK)`.
  arXiv: 159 registros; recupera 6/6 alvos — Back to the Drawing Board (2108.10241), SoK Benchmarking Poisoning
  (2502.03801), Decoding FL Defenses (2502.05211), FL Attacks Revisited (2111.03363), Blades (2206.05359), BackFed
  (2507.04903). Ruído de consenso/blockchain: 2 títulos.
  *Ressalva:* os alvos foram identificados a partir de uma primeira execução mais ampla do mesmo ramo e do conhecimento
  da área (risco de circularidade); a verificação independente fica para o snowballing.

**Veredito da S2 revisada: APROVADA.** Adendo sugerido no §15.3:
> 2026-09-28 · §6.3 · S2 dividida em S2a (RL ∧ auditoria ∧ FL, blocos ampliados) e S2b (FL robusto ∧ auditoria/avaliação,
> sem bloco de RL). · A S2 original retornou 4 registros no arXiv, nenhum útil à QP7; auditorias de FL robusto não citam RL.
