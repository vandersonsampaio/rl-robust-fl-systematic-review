# Related reviews: selection and coding rules

English account of `original_pt/selection_and_coding_rules_pt.md`. The records are in `review_search_records.csv`, one row per unique record, and the columns are defined in `extraction/data_dictionary.md`.

## Scope

The search was run on October 15–16, 2026 in ACM DL, IEEE Xplore, Scopus and arXiv, from 2017 on, only to position the review in the related-work section. No record from it entered the main corpus, whose search ended on September 28, 2026.

String: `("federated learning") AND (byzantine OR poisoning OR backdoor OR "malicious client*" OR "robust aggregation") AND (survey OR review OR "systematization of knowledge" OR SoK)`. It has no RL terms, so that it also retrieves reviews that discuss RL defenses only in the body of the text.

## From 404 records to 45 central reviews

| `screening` | n | rule |
|---|---|---|
| `ja_na_S1` | 90 | the record was already among the 4,054 records screened with S1 (same DOI or normalized title); its S1 decision is in `s1_decision` |
| `revisao_central` | 45 | review, survey or SoK whose central topic, by title and abstract, is the security of FL against adversarial clients |
| `fora` | 269 | not a review, or the security of FL against adversarial clients is not its central topic |

All 45 central reviews were read in full text: 32 by October 16, 2026, and 13 on October 22, 2026 (7 from arXiv and 6 obtained by the authors). The column `rl_as_object` records how each one treats RL: `cataloga` (describes an RL-based defense), `sugere_como_direcao` (suggests RL as a future direction without analyzing it) or `N` (does not mention RL as a defense). None has RL- or bandit-based defenses as its object of analysis. Two catalog an RL defense (R-355, R-394), two suggest RL as a future direction (R-222, R-385), and the other 41 do not mention RL as a defense. R-376 (Ahmad et al., V2-2725) also suggests RL, but it is one of the records already screened with S1, not one of the 45. On October 22, 2026, R-232 was recoded from `sugere_como_direcao` to `N`, because RL appears in it only as an attack technique.

## Selection of the related-work table

A work enters the table (Table 2 of the paper) if it was identified in the main or the separate search, in RQ7 snowballing or in reference reading, and meets at least one criterion:

1. it catalogs RL- or bandit-based defenses, or suggests them as a future direction;
2. it runs experiments or audits evaluation practices;
3. it is one of the two broad surveys chosen to represent the group of reviews that organize the literature by attack or defense family. This choice is the authors' judgment; the other central reviews of that group are in the CSV with `rl_as_object = N`.

| work | origin | criterion | reason |
|---|---|---|---|
| Rodríguez-Barroso et al., 2023 (SB-07) | RQ7 snowballing | 2 | survey with an experiment |
| Sharma et al., 2023 (SB-09) | RQ7 snowballing | 2 | SoK with an experiment |
| Ali et al., 2023 (V2-0091) | main search | 1 | survey of DL security that includes RL |
| Lyu et al., 2024 (R-293) | separate search | 3 | broad survey of privacy and robustness in FL |
| Wan et al., 2024 (R-003) | separate search | 3 | broad survey of poisoning and backdoor in wireless FL |
| Yang et al., 2024 (R-394) | separate search | 1 | catalogs an RL defense (GAAvernor) |
| Szeląg et al., 2025 | RQ7 (C-Szelag) | 2 | survey with an experiment on adaptive adversaries |
| Ahmad et al., 2025 (V2-2725; R-376) | main search | 1 | suggests RL as a future direction |
| Khan et al., 2025 (V2-4764) | main search | 1, 2 | SoK and audit of evaluation practices; cites RL |
| Zhang et al., 2025 (V2-4839) | main search | 2 | SoK with a benchmark |
| Junior et al., 2025 (V2-0101) | main search | 1, 2 | systematic review of the practicality of defenses; cites RL |
| Soulb et al., 2025 (R-304) | separate search | 2 | review with case studies (95% CI, paired tests); added on October 22, 2026 |
| Zakaria and Khalid, 2025 (R-385) | separate search | 1 | suggests an RL defense agent as a trend; added on October 22, 2026 |
| Bajgai et al., 2026 (V2-0566) | main search | 1 | survey of FL and RL in security |
| Li et al., 2025 (R-355) | separate search | 1 | catalogs R2Fed as an RL resilience mechanism and suggests RL-based aggregation; coded N from the abstract, recoded after full-text reading on October 22, 2026 |
| Chacko and Kalaivani, 2026 (R-222) | separate search | 1 | suggests deep RL for trust assessment; added on October 22, 2026 |
| Bellachia et al., 2026 (SB-08) | RQ7 snowballing | 2 | systematic review with a backdoor benchmark |
| Shahsavari et al., 2026 (V2-4840) | main search | 1, 2 | SoK and audit; cites RL |

**Check of the remaining central reviews.** R-232 (RL only as an attack), R-403 (RL cited as an application area of FL) and R-384 (systematic review without an experiment or audit) meet none of the criteria.

## Coding of the table columns

Each cell records whether the aspect is an object of the work's analysis (✓), is treated partially (◐) or is not treated (✗). R1 coded every cell from the full text.

| column | ✓ | ◐ | ✗ |
|---|---|---|---|
| RL/bandits | analyzes RL- or bandit-based defenses as its object | catalogs RL defenses, suggests RL as a future direction without analysis, or treats RL outside the aggregation defense | does not mention RL as a defense |
| FL robustness | FL robustness is the central topic | FL robustness is one of several paradigms or applications covered | not treated |
| Adversarial clients | the adversary is a client that sends malicious updates, and it is the focus | adversarial clients are one of several threats or sources of failure | not treated |
| Incremental contribution of learning | asks whether the performance of a defense comes from its learned component | discusses the question without analyzing it | not treated |
| Baselines by controlled component | classifies baselines by the components they hold constant | compares with simple baselines without classifying them by component | not treated |
| Seeds, inference, testing and budget | analyzes the four aspects together in the reviewed literature | audits how the literature evaluates defenses, or explicitly recommends one of the four practices without analyzing all four | does not audit the evaluation practices of the literature (running one's own experiments with seeds or tests does not count) |

No work has ✓ or ◐ in the columns on the incremental contribution of learning and on baselines by controlled component: none has RL- or bandit-based defenses as its object, so none can ask whether performance comes from learning. The other four columns are coded below (quality = seeds, inference, testing and budget).

| work | RL/bandits | robustness | adversaries | quality | evidence for the ◐ and ✓ marks |
|---|---|---|---|---|---|
| Rodríguez-Barroso et al., 2023 (SB-07) | ✗ | ✓ | ✓ | ✗ | survey of FL threats with its own experiment (25 runs in part of the tests); does not audit the literature |
| Sharma et al., 2023 (SB-09) | ✗ | ✓ | ✓ | ◐ | SoK that models the completeness of attack studies (audit of evaluation practices) |
| Ali et al., 2023 (V2-0091) | ◐ | ◐ | ✓ | ✗ | survey of attacks on DL; FL and DRL are two of the paradigms covered |
| Lyu et al., 2024 (R-293) | ✗ | ✓ | ✓ | ✗ | survey of privacy and robustness in FL |
| Wan et al., 2024 (R-003) | ✗ | ✓ | ✓ | ✗ | survey of poisoning and backdoor in wireless FL; RL cited outside the defense |
| Yang et al., 2024 (R-394) | ◐ | ✓ | ✓ | ✗ | catalogs GAAvernor (an RL defense) without analyzing it |
| Szeląg et al., 2025 | ✗ | ✓ | ✓ | ✗ | survey of adaptive adversaries with an experiment (paired t-test); does not audit the literature or cite RL defenses |
| Ahmad et al., 2025 (V2-2725) | ◐ | ✓ | ✓ | ✗ | systematic review of Byzantine-resilient aggregation; suggests RL as a future direction |
| Khan et al., 2025 (V2-4764) | ◐ | ✓ | ✓ | ◐ | audit of 50 defenses (30% MNIST only, 40% simplistic attacks); catalogs GAAvernor without evaluating it |
| Zhang et al., 2025 (V2-4839) | ✗ | ✓ | ✓ | ✗ | benchmark of 17 defenses × 15 attacks; does not audit how the literature evaluates |
| Junior et al., 2025 (V2-0101) | ◐ | ✓ | ✓ | ◐ | systematic review of the practicality of defenses in IoT (examines evaluation conditions); cites RL |
| Soulb et al., 2025 (R-304) | ✗ | ✓ | ◐ | ◐ | review with case studies; adversaries are one of three sources of fragility (with non-IID data and noisy labels); recommends reporting CIs and significance |
| Zakaria and Khalid, 2025 (R-385) | ◐ | ✓ | ✓ | ✗ | systematic review; suggests an RL defense agent as a trend |
| Li et al., 2025 (R-355) | ◐ | ✓ | ✓ | ✗ | catalogs R2Fed as an RL resilience mechanism and suggests RL-based aggregation |
| Bajgai et al., 2026 (V2-0566) | ◐ | ◐ | ◐ | ✗ | survey of FL and RL for cyber defense; RL is not examined as a component of an aggregation defense |
| Chacko and Kalaivani, 2026 (R-222) | ◐ | ✓ | ✓ | ✗ | survey of adaptive trust-aware FL in healthcare; suggests deep RL for trust assessment |
| Bellachia et al., 2026 (SB-08) | ✗ | ✓ | ✓ | ✗ | systematic review with a backdoor benchmark; does not audit how the literature evaluates |
| Shahsavari et al., 2026 (V2-4840) | ◐ | ◐ | ◐ | ◐ | SoK of FL for vehicular intrusion detection; audits more than 60 works (artificial IID, weak adversarial evaluation); catalogs DRL-PBFL |

## The 45 central reviews

| rid | year | title | `rl_as_object` | in the table |
|---|---|---|---|---|
| R-001 | 2025 | Backdoor attacks and defense mechanisms in federated learning: A survey | `N` | no |
| R-002 | 2024 | A survey on privacy-preserving federated learning against poisoning attacks | `N` | no |
| R-003 | 2024 | Data and Model Poisoning Backdoor Attacks on Wireless Federated Learning, and the Defense Mechanisms: A Comprehensive Survey | `N` | yes |
| R-004 | 2024 | Backdoor attacks and defenses in federated learning: Survey, challenges and future research directions | `N` | no |
| R-005 | 2022 | Defense Strategies Toward Model Poisoning Attacks in Federated Learning: A Survey | `N` | no |
| R-015 | 2025 | Securing the collective intelligence: a comprehensive review of federated learning security attacks and defensive strategies: Securing the collective ... | `N` | no |
| R-031 | 2026 | On the security and privacy of federated learning: A survey with attacks, defenses, frameworks, applications, and future directions | `N` | no |
| R-032 | 2022 | Federated learning attack surface: taxonomy, cyber defences, challenges, and future directions | `N` | no |
| R-042 | 2023 | Backdoor Attacks and Defenses in Federated Learning: State-of-the-Art, Taxonomy, and Future Directions | `N` | no |
| R-101 | 2022 | A contemplative perspective on federated machine learning: Taxonomy, threats & vulnerability assessment and challenges | `N` | no |
| R-128 | 2024 | A survey on vulnerability of federated learning: A learning algorithm perspective | `N` | no |
| R-133 | 2021 | A survey on security and privacy of federated learning | `N` | no |
| R-154 | 2021 | Achieving security and privacy in federated learning systems: Survey, research challenges and future directions | `N` | no |
| R-159 | 2025 | Federated Learning for Urban Sensing Systems: A Comprehensive Survey on Attacks, Defences, Incentive Mechanisms, and Applications | `N` | no |
| R-174 | 2024 | Research Progress on Security and Privacy of Federated Learning: A Survey | `N` | no |
| R-222 | 2026 | Adaptive Trust-Aware Federated Learning for Detecting Malicious Clients in Healthcare Networks:A Survey | `sugere_como_direcao` | yes |
| R-223 | 2025 | State-of-the-Art Defense Schemes Against Byzantine Attack in Federated Learning | `N` | no |
| R-229 | 2026 | Detecting Malicious Clients in Federated Learning | `N` | no |
| R-231 | 2026 | A Comprehensive Review of Attacks and Defense Mechanisms in Federated Learning for Autonomous Driving and VANETs | `N` | no |
| R-232 | 2023 | Poisoning Attacks in Federated Learning: A Survey | `N` | no |
| R-233 | 2026 | Beyond Data Silos: A Comprehensive Survey on Privacy-Preserving and Secure Federated Learning | `N` | no |
| R-239 | 2025 | Poisoning Attacks and Defenses Techniques for Federated Learning: A Survey | `N` | no |
| R-241 | 2025 | Securing Federated Learning in IoT: A Survey of Attacks, Defenses, and Frameworks | `N` | no |
| R-245 | 2025 | Poisoning Attacks Against Federated Recommender Systems and the Defenses: A Survey | `N` | no |
| R-250 | 2023 | Federated learning: Applications, Security hazards and Defense measures | `N` | no |
| R-279 | 2021 | A survey on security and privacy threats to federated learning | `N` | no |
| R-283 | 2024 | A Review on Federated Learning with a Focus on Security and Privacy | `N` | no |
| R-284 | 2026 | Defense Against Adversarial Attacks in Federated Learning: A Research for Secure Biomedical Innovation | `N` | no |
| R-293 | 2024 | Privacy and Robustness in Federated Learning: Attacks and Defenses | `N` | yes |
| R-298 | 2026 | Trustworthy Distributed Machine Learning in Cloud-Edge-IoT Systems: A Heterogeneity-Aware Survey of Security, Privacy, and Robustness | `N` | no |
| R-304 | 2025 | Evaluating the Robustness in Federated Learning for Medical Imaging | `N` | yes |
| R-355 | 2025 | Towards Resilient Federated Learning in CyberEdge Networks: Recent Advances and Future Trends | `cataloga` | yes |
| R-364 | 2023 | A Survey on Federated Learning Poisoning Attacks and Defenses | `N` | no |
| R-366 | 2023 | Poisoning Attacks and Defenses in Federated Learning: A Survey | `N` | no |
| R-371 | 2020 | Threats to Federated Learning: A Survey | `N` | no |
| R-377 | 2026 | Framing Adversarial Federated Learning Threats through MITRE ATLAS | `N` | no |
| R-378 | 2025 | Byzantine fault tolerance in distributed machine learning: a survey | `N` | no |
| R-384 | 2023 | Navigating the Void: Uncovering Research Gaps in the Detection of Data Poisoning Attacks in Federated Learning-Based Big Data Processing | `N` | no |
| R-385 | 2025 | A Review of Federated Learning Attacks: Threat Models and Defence Strategies | `sugere_como_direcao` | yes |
| R-388 | 2022 | Privacy and Security in Federated Learning: A Survey | `N` | no |
| R-391 | 2025 | Privacy-Preserving Federated Learning in Healthcare, E-Commerce, and Finance: A Taxonomy of Security Threats and Mitigation Strategies | `N` | no |
| R-393 | 2024 | Challenges and Countermeasures of Federated Learning Data Poisoning Attack Situation Prediction | `N` | no |
| R-394 | 2024 | Robust and privacy-preserving collaborative training: a comprehensive survey | `cataloga` | yes |
| R-402 | 2025 | A survey of security threats in federated learning | `N` | no |
| R-403 | 2022 | Threats, attacks and defenses to federated learning: issues, taxonomy and perspectives | `N` | no |
