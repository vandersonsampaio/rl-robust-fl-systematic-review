# Data dictionary

All CSV files are UTF-8 with a header row. Column names are in English, and free-text values extracted from the articles are in Portuguese. Columns whose content is free text in Portuguese end in `_pt`, or are marked *(pt)* below.

## Common codes

| code | meaning |
|---|---|
| `S` / `P` / `N` | met / partially met / not met (*sim*, *parcial*, *não*); in quality criteria, S = 1, P = 0.5, N = 0 |
| `?` | the text supports more than one reading (genuine ambiguity) |
| `não reportado` | the article does not report the information; scored as N |
| `V2-xxxx` | record from the database searches |
| `SB-xx` | record found by snowballing and absent from the databases |
| `R-xxx` | record from the separate search for related reviews |

### Screening decisions

| code | meaning |
|---|---|
| `I` | included (stage 1: proceeds to full text) |
| `D` | uncertain at stage 1; referred to full-text assessment |
| `E-IC1` … `E-IC5` | excluded for failing inclusion criterion IC1–IC5 |
| `E-EC1` … `E-EC7` | excluded under exclusion criterion EC1–EC7 |
| `E-PER` | published before 2017 |
| `Q7-I` / `Q7-D` / `Q7-E` | RQ7 flow: included / uncertain / excluded |
| `nao_recuperado` | full text could not be obtained |

The criteria themselves are in the paper (Table "Eligibility criteria") and in protocol §7, with the RQ7 groups Q7a–Q7c (amendment A25). At stage 1, the reason recorded is the first unmet criterion in the order E-PER → IC1 → EC5 → EC1 → EC4 → EC3 → IC2 → EC2 → IC3 → others.

Decision methods (`s1_method`, `rq7_method`): `leitura_manual` (manual reading of title and abstract), `herdado:<id>` (decision inherited, by normalized title, from the preliminary screening round of September 27, 2026; `<id>` is a row of `screening/stage1_preliminary_round.csv`), `regra` (explicit exclusion rule, for example, no federated learning term).

## search/

- **`search_log.csv`**: one row per search run or step, in chronological order: `date`, `source` (database, validation step or deduplication), `query` (exact text executed, or the string label), `fields`, `filters`, `n_results`, `export_file` (file name in the working folders of the review), `note_pt` *(pt)*. Rows dated September 27 are preliminary runs, and validation rows (`União (validação §6.4)`, arXiv rows marked `VALIDAÇÃO §6.4`) record the string validation; neither enters the counts. The final searches are the rows of September 28 marked `busca definitiva` or adopted as final.
- **`reference_set.csv`**: `id` (Q1–Q5 reference studies, B1–B2 boundary controls), `study`, `venue_year`, `agent` (learning method of the study), `expected` (outcome expected from a valid S1), `retrieved_by_final_S1` (yes/no), `outcome` (what happened to the study in the review).
- **`related_reviews/review_search_records.csv`** (404 unique records of the separate search for related reviews; rules in `related_reviews/selection_and_coding_rules.md`):

  | column | content |
  |---|---|
  | `rid` | record id (`R-xxx`) |
  | `sources` | databases where the record appeared, separated by `;` (`ACM-titulo` and `ACM-resumo` are the ACM queries on title and on abstract) |
  | `title`, `year`, `authors`, `venue`, `doi`, `arxiv` | identification |
  | `s1_id`, `s1_decision` | id and stage-1 decision of the same record in the main search, when it was already among the records screened with S1 |
  | `screening` | `revisao_central` (review, survey or SoK centred on FL security against adversarial clients), `ja_na_S1` (already screened with S1), `fora` (out of scope) |
  | `rl_as_object` | for the 45 central reviews and R-376: `cataloga` (catalogs an RL-based defense), `sugere_como_direcao` (suggests RL as a future direction without analysis), `N` (does not mention RL as a defense) |
  | `full_text_read` | S/N: the full text was read |
  | `review_by_title_abstract` | S/N: the record is a review, survey or SoK according to its title and abstract |
  | `adversarial_clients` | S/N: the title or abstract addresses adversarial clients |
  | `rl_in_abstract` | S/N: the abstract mentions RL or bandits |
  | `rl_mentions_in_text` | number of RL mentions found in the full text, when it was searched |

## screening/

- **`records.csv`** (4,863 unique records): `id`, `title`, `year`, `venue`, `authors`, `doi`, `arxiv`, `url`, `databases` (sources where the record appeared), `search_strings` (s1, s2a, s2b).
- **`stage1_decisions.csv`**: the stage-1 decision for each record.
  - S1 criteria: `s1_decision`, `s1_reason_pt`, `s1_confidence` (`alta` = high, `media` = medium), `s1_method`. These are empty for the 809 records assessed only for RQ7.
  - RQ7 flow: `rq7_decision`, `rq7_reason_pt`, `rq7_method`.
  - `full_text_sought`: `S` (I or D in S1, or Q7-I or Q7-D in RQ7), `§9.2` (E-EC2 at stage 1: marked for the list of non-RL adaptive defenses of protocol §9.2; these 26 records were not read in full and have no form in `extraction/non_rl_adaptive_defenses.csv`, see `extraction/README.md`), `N` (not sought).
- **`stage1_preliminary_round.csv`** (3,769 rows): decisions of the preliminary screening round of September 27, 2026 (ACM DL, IEEE Xplore and Scopus, original S1), from which 3,341 stage-1 decisions were inherited. Columns: `preliminary_id` (`ACM-`, `IEEE-`, `SCO-`), `database`, `title`, `year`, `venue`, `doi_or_arxiv`, `decision`, `reason_pt` *(pt)*, `confidence`, `method` (`leitura_manual`, `regra`, `herdado:<id>` within the same round, or `não registrado` for the ACM records, whose method was not recorded) and `inherited_by` (the `V2-` record that inherited the decision). Abstracts are not included.
- **`stage2_decisions.csv`**: full-text decisions for the main synthesis (`flow = S1`) and RQ7 (`flow = QP7`). `source` is the database of the PDF (`ieee`, `scopus`, `acm`, `arXiv`) or `novos` for records found by snowballing.
  - Decision: `stage1_decision`, `stage2_decision` and `stage2_reason_pt`.
  - `related_version` is the version kept when EC7 applies.
  - `checked_by_r2` (S/N) marks whether R2 checked the decision in round 1 (36 exclusions and 16 inclusions; `reliability/stage2_consensus.csv`).
  - `via_snowballing` and `snowballing_origin` record snowballing. Full texts that could not be retrieved have `stage2_decision = nao_recuperado`, including the two snowballing candidates SB-11 (FedDive) and SB-12 (Zhang et al., Neurocomputing 2024) (amendment A8).
- **`screening_flow.csv`**: PRISMA counts for the main synthesis and RQ7.
- **`exclusion_reasons.csv`**: number of exclusions per code, stage and flow.
- **`deduplication_log.csv`**: one row per raw record (6,580): `id` of the unique record it was merged into, `database`, `search_string`, `export_file` and `title`.
- **`snowballing_iteration1.csv`**: candidates of the first iteration.
- **`snowballing_iteration2_main_synthesis.csv`**: the 94 references of R2Fed (V2-0945) and FedCHO (SB-03), screened by title in the second backward iteration (amendment A26). `decision_pt`: `fora` (out of scope) or `já incluído` (already included).

## extraction/main_corpus.csv (77 studies)

| column | content |
|---|---|
| `id`, `title`, `authors`, `year`, `venue`, `doi_or_arxiv` | identification; the year is the year of the volume (one study published online in September 2026 has volume year 2027) |
| `peer_reviewed` | S = peer reviewed, N = preprint |
| `domain`, `fl_setting` *(pt)* | application domain; FL setting (cross-device or cross-silo, horizontal, hierarchical, decentralized) |
| `algorithm`, `state`, `action`, `reward` *(pt)* | the agent: RL or bandit algorithm, state, action and reward |
| `decision_granularity` | `regra/rodada` (rule per round), `peso/cliente` (weight per client), `selecao/cliente` (selection or exclusion per client), `parametro` (defense parameter); combinations joined by `+` |
| `test_set_use` | S = the test set is used in the reward, state, model selection or update verification; P = data sampled from the test set but disjoint from the final evaluation; N = not used; ? = data source not described |
| `learning_mode` *(pt)* | online during FL, offline pretraining, or both |
| `learning_budget` *(pt)* | effective budget of the agent (steps, episodes, rounds, optimization parameters) |
| `horizon_analysis` | S if the gain over a non-learned policy is reported as a function of the number of rounds (none in the corpus) |
| `signal`, `memory`, `ablations` *(pt)* | signal used by the agent; inter-round memory (S/N/?); ablations and their results |
| `signal_privacy` *(pt)* | data the signal requires (updates only, server-side data, test set, reconstruction of client data, device monitoring) |
| `cost` *(pt)* | reported computational cost |
| `non_learned_comparison` *(pt)* | non-learned policies the agent is compared with |
| `comparison_result` *(pt)* | reported values of those comparisons |
| `discussed_as_finding` | S if the authors comment on the comparison and draw a conclusion from it; for ties, whether they acknowledge the equality is recorded in the text (A21) |
| `attacks`, `adaptive_attack` | attacks evaluated *(pt)*; adaptive attack S = the adversary knows and adapts to the defense, P = described as adaptive without using knowledge of the defense |
| `datasets_models`, `clients`, `static_baselines` *(pt)* | experimental setting |
| `seeds_statistics` *(pt)* | number of runs, variability and statistical tests |
| `code` | S/P/N under the QA4 rule (A24), with the link |
| `notes` *(pt)* | reading notes |
| `rq2_category` | strongest non-learned reference, derived by the rule of `scripts/pipeline/sintese.py`, in precedence order: `same-signal heuristic`, `fixed action`, `different-signal heuristic`, `random`, `partial ablation`, `oracle`, `none`; the oracle sets the category only when it is the only reference (A27) |
| `rq2_has_oracle` | S if the study also compares the agent with an oracle, whatever its category (A27) |
| `rq2_closest_result` | for the 15 closest comparisons (same-signal heuristic or fixed action that is a defense): `tie` (difference up to about 1 percentage point in some regime, or the agent does not beat the reference in every regime; losses are counted here), `narrow win` (more than about 1 and up to about 6 points) or `clear win`; see `reliability/reconciliation_rules.md` |

`extraction/extraction_revisions.csv` lists, in order, every field corrected after the preliminary extraction (`id`, `field_pt`, `value`). A later row overrides an earlier one, and `main_corpus.csv` already includes all revisions. `field_pt` uses the Portuguese field names of the working files:

| `field_pt` | column of `main_corpus.csv` |
|---|---|
| `algoritmo`, `estado`, `recompensa`, `modo`, `orcamento` | `algorithm`, `state`, `reward`, `learning_mode`, `learning_budget` |
| `vazamento_teste` | `test_set_use` |
| `analise_horizonte` | `horizon_analysis` |
| `sinal`, `memoria`, `ablacoes`, `privacidade_sinal`, `custo` | `signal`, `memory`, `ablations`, `signal_privacy`, `cost` |
| `comparacao_nao_aprendida`, `resultado_comparacao`, `discutido_como_achado` | `non_learned_comparison`, `comparison_result`, `discussed_as_finding` |
| `ataques`, `ataque_adaptativo` | `attacks`, `adaptive_attack` |
| `datasets_modelos`, `clientes`, `sementes_estatistica` | `datasets_models`, `clients`, `seeds_statistics` |
| `codigo`, `notas`, `doi_arxiv` | `code`, `notes`, `doi_or_arxiv` | The rows for V2-1120 (TARS) refer to a study that was extracted and then excluded under IC4 (amendment A22), so V2-1120 is not in `main_corpus.csv`.

## extraction/quality_assessment.csv

`QA1`–`QA9` (S/P/N), `total` (sum with S = 1, P = 0.5, N = 0) and `rationale_pt`. The criteria are defined in the paper and in `reliability/codebook/codebook_v2_r1_pt.md`. QA1–QA5 and QA7–QA9 are derived by explicit rules from the extraction fields (`scripts/pipeline/etapa2_lote2.py`), and QA6 was assessed in the full-text reading.

| criterion | dimension | S |
|---|---|---|
| QA1 | experimental validity | neither the reward nor model selection uses the test set |
| QA2 | statistical rigour | ≥ 3 independent runs with variability |
| QA3 | statistical rigour | statistical test or confidence interval on the main comparisons |
| QA4 | reproducibility | code of the agent and the experiment accessible without intermediation (A24) |
| QA5 | experimental validity | comparison with a same-signal heuristic or a fixed action that is a defense (A23) |
| QA6 | security evaluation | attacks verifiably faithful to their original definitions |
| QA7 | reporting | training volume and an optimization parameter of the agent reported (A20) |
| QA8 | security evaluation | strong static defenses of both families: one using server-side data and one robust statistic (A19) |
| QA9 | security evaluation | an adaptive adversary that knows the defense |

## extraction/rq7_corpus.csv (34 works)

| column | content |
|---|---|
| `id` | identifier (`V2-`, `SB-`, or `C-` for canonical readings) |
| `type` *(pt)* | `auditoria` (audit), `benchmark`, `SoK`, `avaliação` (evaluation), `reprodutibilidade` (reproducibility study), `survey+experimento`; combinations joined by `+` |
| `scope` *(pt)* | `FL robusto` (robust FL), `VFL`, `DFL`, `pFL`, `MARL`, `RL geral` (general RL) |
| `simple_baseline_matches` | whether a simple baseline matches or beats a more sophisticated method: `S`, `N` or `misto` (mixed) |
| `pattern` | pattern of results, several per study separated by `;`: `A` = under attack, simple defenses match or beat complex ones; `B` = without attack, robustness has a cost (FedAvg or the plain mean wins); `C` = simple attacks match or beat optimized ones; `X` = counterexample (the simple method fails); empty = does not apply |
| `pitfalls` | evaluation pitfalls identified, several per study separated by `;`: `i` = easy datasets or simplistic attacks; `ii` = non-IID data breaks the defense; `iii` = an adaptive adversary breaks the defense; `iv` = bugs or incomplete metrics; `v` = simple defenses suffice; empty = none identified |
| `rl_defense_mentioned` | `nao` (no RL-based defense mentioned) or `cita` (cites or catalogs an RL-based defense without evaluating it) |
| `seeds` *(pt)* | number of seeds or runs and whether variability is reported |
| `statistical_test` | S/N: hypothesis test or multiple-comparison correction |
| `finding_pt` | main finding |

## extraction/non_rl_adaptive_defenses.csv

Adaptive defenses without an RL or bandit component that were read in full text: the five excluded under EC2 at stage 2 (`origin = S1: E-EC2`) and two RQ7 works that would fall under EC2 in S1. Descriptive fields as in the main corpus; free-text values in Portuguese. The 26 records excluded under EC2 at stage 1 have no form (see `extraction/README.md`).
