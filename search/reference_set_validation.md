# Validation of the search strings

English account of `original_pt/reference_set_validation_pt.md` (September 28, 2026). The validation was run by R1 before the final searches, and its result led to amendment A3. The reference set and the outcome of each study are in `reference_set.csv`.

## S1

**Criterion.** The union of the databases must retrieve all five studies of the reference set (Q1–Q5). Two boundary controls check the edges of the string: B1 is an adaptive defense without RL, which S1 should not retrieve, and B2 is an RL attacker, which S1 retrieves and EC1 excludes.

**Original S1: 4 of 5, rejected.** Q1 (AdaAggRL, arXiv:2406.14217) was missing from every database. Q2–Q5 were retrieved. Both controls behaved as expected: B2 was retrieved and excluded under EC1, and B1 was not retrieved. Adaptive defenses without RL are covered by snowballing and by the list of non-RL adaptive defenses (`extraction/non_rl_adaptive_defenses.csv`).

### Diagnosis

1. **Q1 has no term of block B.** Its abstract says only "RL-based adaptive aggregation" and "policy learning", while block B required "reinforcement learning", algorithm acronyms (DQN, TD3 and others) or "multi-armed/contextual bandit". The failure is in the sensitivity of the string, so it repeats in every database.
2. **Variant terms in included records.** Of the 65 unique records included at that point, 8 would not match S1 by title and abstract. They were exported only because of indexed metadata (IEEE Terms, indexed keywords):

   | variant used in the record | S1 term that failed |
   |---|---|
   | "Q learning" (no hyphen; TARS, Q4) | "Q-learning" |
   | "Upper Confidence Bound (UCB)" (SARA) | none |
   | "UCB" | none |
   | "multiarmed bandits", "Thompson Sampling" | "multi-armed bandit" |
   | "deep reinforcement algorithm" | "reinforcement learning" |
   | "actor–critic" (en dash) | "actor-critic" |
   | "DRL" | none |
   | "untrusted nodes" (block C) | none |

3. **arXiv API.** The phrase query `abs:"reinforcement learning"` did not retrieve Q1 or Q2, although both have the phrase in the title or abstract (tested by intersecting `id_list` with `search_query`). Unquoted terms (`abs:reinforcement`) and the `all:` field work.

### Revised S1: 5 of 5, adopted

- **Block A (FL):** unchanged.
- **Block B (RL and bandits):** extended with `reinforcement`, `bandit*`, `multiarmed`, `RL`, `DRL`, `MARL`, `"Q learning"`, `DDQN`, `"actor critic"`, `"policy learning"`, `"policy optimization"`, `"upper confidence bound"`, `UCB`, `"Thompson sampling"`, `LinUCB`, `"Markov decision process"` and `MDP`.
- **Block C (adversary):** extended with `untrust*`, `sybil`, `"free-rid*"` and `selfish`.
- **arXiv:** the `all` field instead of `abs` (68 records instead of 67), because of the limitation above. The original arXiv string returned 27 records.

The revised string retrieved Q1, Q2 and Q5 in arXiv, and Q3 and Q4 were already retrieved in the other databases, so the union reached 5 of 5. The preliminary runs in ACM DL, IEEE Xplore and Scopus (September 27) predated this validation, so the revised string was run again in all databases on September 28, and these are the final searches. The final strings are in `search_strings.md`.

## S2 (RQ7)

The protocol defines no reference set for S2. The validation set below was assembled on September 28, 2026, and is declared as such.

**Original S2 (RL ∧ audit ∧ FL): rejected.** The syntax worked and the string retrieved the two RQ7 targets already known from Scopus (an RL ablation and a comparison with UCB and Thompson sampling). In arXiv (`all` field), however, it returned 4 records, none useful for RQ7, or 8 with the extended RL block. The intersection of RL, audit and FL is nearly empty. Audits of robust FL do not mention RL and fall outside the string. None of the canonical readings of protocol §13 is retrieved either, by design, and they remain direct inclusions.

**Revised S2 = S2a ∪ S2b: adopted.**

- **S2a** (audits of RL-based FL defenses): the original S2 with the RL and audit blocks extended. It retrieves the four RQ7 targets known from Scopus.
- **S2b** (audits and evaluations of robust FL, without an RL block): `"federated learning" AND (poisoning OR byzantine OR backdoor OR "robust aggregation") AND (reproducib* OR "sanity check" OR "simple baseline*" OR benchmark* OR "empirical evaluation" OR pitfall* OR revisit* OR rethink* OR "fair comparison" OR systematization OR SoK)`. In arXiv it returned 159 records and retrieved all six targets: *Back to the Drawing Board* (2108.10241), *SoK: Benchmarking Poisoning* (2502.03801), *Decoding FL Defenses* (2502.05211), *FL Attacks Revisited* (2111.03363), *Blades* (2206.05359) and *BackFed* (2507.04903). Two retrieved titles were noise (consensus and blockchain).

**Caveat.** The S2b targets were identified from an earlier, broader run of the same branch and from knowledge of the field, so this validation is at risk of circularity. Snowballing provided the independent check.
