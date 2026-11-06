# Search strings

All searches were run on **September 28, 2026**, covering January 1, 2017 to the search date and English-language records. The exact text executed in each source, the filters and the number of records are in `search_log.csv`. Entries dated September 27–28 that precede the final runs (`S1 atual`, `S1 revisada`) belong to the validation of the string against the reference set (`reference_set.csv`, amendment A3).

| string | purpose | Scopus | IEEE Xplore | ACM DL | arXiv | total |
|---|---|---|---|---|---|---|
| S1 | main synthesis (RQ1–RQ6) | 4,226 | 762 | 96 | 68 | 5,152 |
| S2a | RQ7: audits of RL-based FL defenses | 194 | 148 | 52 | 8 | 402 |
| S2b | RQ7: audits and evaluations of robust FL | 455 | 292 | 120 | 159 | 1,026 |
| **total** | | **4,875** | **1,202** | **268** | **235** | **6,580** |

Web of Science was planned as a complementary source but was not searched (amendment A5).

## S1: RL- and bandit-based FL defenses

Three blocks are combined: A (federated learning), B (RL or bandits) and C (adversarial clients).

### Scopus (TITLE-ABS-KEY)

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

Exported in three batches because of the 2,000-record display limit.

### IEEE Xplore (Command Search, All Metadata, 2017–2026)

```
("All Metadata":"federated learning" OR "All Metadata":"federated optimization" OR "All Metadata":"federated averaging")
AND ("All Metadata":reinforcement OR "All Metadata":RL OR "All Metadata":DRL OR "All Metadata":MARL
     OR "All Metadata":"Q-learning" OR "All Metadata":"Q learning" OR "All Metadata":DQN OR "All Metadata":DDQN
     OR "All Metadata":DDPG OR "All Metadata":TD3 OR "All Metadata":PPO OR "All Metadata":"actor-critic"
     OR "All Metadata":"actor critic" OR "All Metadata":"policy gradient" OR "All Metadata":"policy learning"
     OR "All Metadata":"policy optimization" OR "All Metadata":bandit* OR "All Metadata":multiarmed
     OR "All Metadata":"upper confidence bound" OR "All Metadata":UCB OR "All Metadata":"Thompson sampling"
     OR "All Metadata":LinUCB OR "All Metadata":"Markov decision process" OR "All Metadata":MDP)
AND ("All Metadata":byzantine OR "All Metadata":poisoning OR "All Metadata":backdoor OR "All Metadata":malicious
     OR "All Metadata":adversar* OR "All Metadata":"robust aggregation" OR "All Metadata":attack*
     OR "All Metadata":untrust* OR "All Metadata":sybil OR "All Metadata":"free-riding" OR "All Metadata":selfish)
```

### ACM Digital Library (2017–2026)

The interface did not accept OR between fields. The query below was therefore run twice, once restricted to Abstract (89 records) and once to Title (7 records), and Keywords was not used (amendment A5).

```
(Title:(A) OR Abstract:(A) OR Keyword:(A)) AND (Title:(B) OR Abstract:(B) OR Keyword:(B)) AND (Title:(C) OR Abstract:(C) OR Keyword:(C))
A = "federated learning" OR "federated optimization" OR "federated averaging"
B = reinforcement OR bandit* OR multiarmed OR RL OR DRL OR MARL OR "Q-learning" OR "Q learning" OR DQN OR DDQN
    OR DDPG OR TD3 OR PPO OR "actor-critic" OR "actor critic" OR "policy gradient" OR "policy learning"
    OR "policy optimization" OR "upper confidence bound" OR UCB OR "Thompson sampling" OR LinUCB
    OR "Markov decision process" OR MDP
C = byzantine OR poisoning OR backdoor OR malicious OR adversar* OR "robust aggregation" OR attack*
    OR untrust* OR sybil OR "free-riding" OR selfish
```

### arXiv (API, field `all`, categories cs.LG, cs.CR, cs.DC, cs.AI, stat.ML)

Exact query in `arxiv_queries/string_arxiv_revisada_all.txt`.

## S2a: audits of RL-based FL defenses (RQ7)

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

The same blocks were run in IEEE Xplore (All Metadata syntax) and ACM DL (by field). The arXiv query is in `arxiv_queries/string_arxiv_s2_revisada.txt`.

## S2b: audits and evaluations of robust FL (RQ7)

```
TITLE-ABS-KEY ( "federated learning"
AND ( poisoning OR byzantine OR backdoor OR "robust aggregation" )
AND ( reproducib* OR "sanity check" OR "simple baseline*" OR benchmark* OR "empirical evaluation" OR pitfall*
      OR revisit* OR rethink* OR "fair comparison" OR systematization OR sok ) )
AND PUBYEAR > 2016
```

The same blocks were run in IEEE Xplore and ACM DL. The arXiv query is in `arxiv_queries/string_arxiv_s2b.txt`.

## Search for related reviews (positioning only)

This search was run on October 15–16, 2026 in ACM DL, IEEE Xplore, Scopus and arXiv, from 2017 on. It served only to position the review against previous reviews, and **no record from it entered the corpus**. The string has no RL terms, so that it also retrieves reviews that mention RL defenses only in the body of the text:

```
("federated learning") AND (byzantine OR poisoning OR backdoor OR "malicious client*" OR "robust aggregation")
AND (survey OR review OR "systematization of knowledge" OR SoK)
```

Records, screening decisions and the coding of the compared works are in `related_reviews/`.

## Original working document

`original_pt/search_strings_S1_S2_pt.md` is the string file used before the search, in Portuguese. `original_pt/reference_set_validation_pt.md` records how the strings were validated against the reference set, and `reference_set_validation.md` gives that validation in English.
