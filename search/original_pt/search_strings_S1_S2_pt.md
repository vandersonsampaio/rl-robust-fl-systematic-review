# Strings de busca validadas — S1 e S2 (2026-09-28)

Validação: `validacao/validacao_6.4.md`. Estas strings substituem as do §6.2/§6.3 do protocolo (registrar o adendo no §15.3).
Ao rodar, copie o **texto exato executado** para `triagem/log_buscas.csv` (data, base, string, campos, filtros, nº de resultados, arquivo).

## S1 (defesas de FL com RL/bandit)

### Scopus (Advanced search)
```
TITLE-ABS-KEY ( ( "federated learning" OR "federated optimization" OR "federated averaging" )
AND ( reinforcement OR bandit* OR multiarmed OR RL OR DRL OR MARL OR "Q-learning" OR "Q learning"
      OR dqn OR ddqn OR ddpg OR td3 OR ppo OR "actor-critic" OR "actor critic" OR "policy gradient"
      OR "policy learning" OR "policy optimization" OR "upper confidence bound" OR ucb
      OR "Thompson sampling" OR linucb OR "Markov decision process" OR mdp )
AND ( byzantine OR poisoning OR backdoor OR malicious OR adversar* OR "robust aggregation" OR attack*
      OR untrust* OR sybil OR "free-rid*" OR selfish ) )
AND PUBYEAR > 2016
```

### IEEE Xplore (Command Search, "All Metadata"; rodar B1 e B2 e unir)
A e C são iguais nas duas execuções:
```
("All Metadata":"federated learning" OR "All Metadata":"federated optimization" OR "All Metadata":"federated averaging")
AND (<B1 ou B2>)
AND ("All Metadata":byzantine OR "All Metadata":poisoning OR "All Metadata":backdoor OR "All Metadata":malicious
     OR "All Metadata":adversar* OR "All Metadata":"robust aggregation" OR "All Metadata":attack*
     OR "All Metadata":untrust* OR "All Metadata":sybil OR "All Metadata":"free-riding" OR "All Metadata":selfish)
```
B1:
```
"All Metadata":reinforcement OR "All Metadata":RL OR "All Metadata":DRL OR "All Metadata":MARL
OR "All Metadata":"Q-learning" OR "All Metadata":"Q learning" OR "All Metadata":DQN OR "All Metadata":DDQN
OR "All Metadata":DDPG OR "All Metadata":TD3 OR "All Metadata":PPO OR "All Metadata":"actor-critic"
OR "All Metadata":"actor critic" OR "All Metadata":"policy gradient" OR "All Metadata":"policy learning"
OR "All Metadata":"policy optimization"
```
B2:
```
"All Metadata":bandit* OR "All Metadata":multiarmed OR "All Metadata":"upper confidence bound" OR "All Metadata":UCB
OR "All Metadata":"Thompson sampling" OR "All Metadata":LinUCB OR "All Metadata":"Markov decision process" OR "All Metadata":MDP
```
Filtro: anos 2017–2026. Se o IEEE recusar pelo limite de termos/curingas, dividir também o bloco C em duas metades.

### ACM Digital Library (Advanced Search → Edit query; Title + Abstract + Keywords)
Repetir cada bloco nos três campos:
```
(Title:("federated learning" OR "federated optimization" OR "federated averaging")
 OR Abstract:("federated learning" OR "federated optimization" OR "federated averaging")
 OR Keyword:("federated learning" OR "federated optimization" OR "federated averaging"))
AND
(Title:(<B>) OR Abstract:(<B>) OR Keyword:(<B>))
AND
(Title:(<C>) OR Abstract:(<C>) OR Keyword:(<C>))
```
com
```
<B> = reinforcement OR bandit* OR multiarmed OR RL OR DRL OR MARL OR "Q-learning" OR "Q learning" OR DQN OR DDQN
      OR DDPG OR TD3 OR PPO OR "actor-critic" OR "actor critic" OR "policy gradient" OR "policy learning"
      OR "policy optimization" OR "upper confidence bound" OR UCB OR "Thompson sampling" OR LinUCB
      OR "Markov decision process" OR MDP
<C> = byzantine OR poisoning OR backdoor OR malicious OR adversar* OR "robust aggregation" OR attack*
      OR untrust* OR sybil OR "free-riding" OR selfish
```
Filtro de data: 2017–2026.

### Web of Science (se houver acesso)
```
TS=( ("federated learning" OR "federated optimization" OR "federated averaging")
AND (reinforcement OR bandit* OR multiarmed OR RL OR DRL OR MARL OR "Q-learning" OR "Q learning" OR DQN OR DDQN
     OR DDPG OR TD3 OR PPO OR "actor-critic" OR "actor critic" OR "policy gradient" OR "policy learning"
     OR "policy optimization" OR "upper confidence bound" OR UCB OR "Thompson sampling" OR LinUCB
     OR "Markov decision process" OR MDP)
AND (byzantine OR poisoning OR backdoor OR malicious OR adversar* OR "robust aggregation" OR attack*
     OR untrust* OR sybil OR "free-rid*" OR selfish) )
AND PY=(2017-2026)
```

### arXiv (API; já executada na validação → `validacao/arxiv_revisada_all.csv`, 68 registros)
Texto exato em `validacao/string_arxiv_revisada_all.txt` (campo `all:`, categorias cs.LG, cs.CR, cs.DC, cs.AI, stat.ML).
Posso reexecutar no dia da busca definitiva com `scripts/busca_arxiv.py`.

## S2 (QP7) = S2a ∪ S2b — rodar no Scopus e no arXiv

### Scopus — S2a (auditoria de defesas de FL com RL)
```
TITLE-ABS-KEY ( ( reinforcement OR bandit* OR multiarmed OR RL OR DRL OR MARL OR "Q-learning" OR "Q learning"
      OR dqn OR ddpg OR td3 OR ppo OR "actor-critic" OR "actor critic" OR "policy gradient" OR "policy learning"
      OR "policy optimization" OR "upper confidence bound" OR ucb OR "Thompson sampling" )
AND ( ablation OR "random policy" OR "fixed policy" OR "heuristic baseline" OR "simple baseline*" OR reproducib*
      OR "sanity check" OR "random selection" OR "random baseline" OR "fixed action" OR "static policy"
      OR "heuristic policy" OR "heuristic selection" OR replicat* OR reimplement* )
AND ( "federated learning" OR "robust aggregation" OR byzantine ) )
AND PUBYEAR > 2016
```

### Scopus — S2b (auditoria/avaliação de FL robusto)
```
TITLE-ABS-KEY ( "federated learning"
AND ( poisoning OR byzantine OR backdoor OR "robust aggregation" )
AND ( reproducib* OR "sanity check" OR "simple baseline*" OR benchmark* OR "empirical evaluation" OR pitfall*
      OR revisit* OR rethink* OR "fair comparison" OR systematization OR sok ) )
AND PUBYEAR > 2016
```

### arXiv (já executadas na validação)
- S2a: `validacao/string_arxiv_s2_revisada.txt` → 8 registros
- S2b: `validacao/string_arxiv_s2b.txt` → 159 registros

## Exportação (para evitar a higienização manual)
- **Scopus:** Export → **CSV**, marcando *Citation information*, *Bibliographical information* e *Abstract & keywords*
  (inclui DOI, palavras-chave e resumo). Acima de 2.000 resultados: exportar em faixas de ano (ex.: 2017–2023, 2024, 2025–2026).
- **IEEE:** Export → CSV (como antes), uma vez para B1 e outra para B2.
- **ACM:** Export Citations → BibTeX, todos os resultados.
