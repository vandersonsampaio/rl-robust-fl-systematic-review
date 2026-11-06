# Screening

| file | content |
|---|---|
| `records.csv` | the 4,863 unique records after deduplication |
| `deduplication_log.csv` | one row per exported record (6,580), linked to its unique record |
| `stage1_decisions.csv` | stage-1 decision (title and abstract) for every unique record: S1 criteria for 4,054 records, RQ7 criteria for 826 (17 records have both) |
| `stage1_preliminary_round.csv` | decisions of the preliminary screening round of September 27, 2026, from which 3,341 stage-1 decisions were inherited |
| `stage2_decisions.csv` | full-text decisions: 130 rows in the main flow (124 from the databases, 6 from snowballing) and 46 in the RQ7 flow (40 from the databases, 6 from snowballing) |
| `screening_flow.csv` | PRISMA counts for the main synthesis and RQ7 |
| `exclusion_reasons.csv` | number of exclusions per code, stage and flow |
| `snowballing_iteration1.csv` | candidates of the first snowballing iteration |
| `snowballing_iteration2_main_synthesis.csv` | the 94 references screened in the second backward iteration (amendment A26) |
| `original_pt/prisma_stage1_pt.md` | stage-1 PRISMA report written by `scripts/pipeline/triagem_v2.py`, in Portuguese |

Columns and codes are defined in `extraction/data_dictionary.md`. `scripts/validate_counts.py` recomputes the PRISMA counts from these files.

## How the stage-1 decisions were made

The S1 string was first run on September 27, 2026 in ACM DL, IEEE Xplore and Scopus, and those records were screened in a preliminary round. After the string was revised (amendment A3), all databases were searched again on September 28. Records of the final search whose normalized title had already been screened kept the earlier decision, recorded as `s1_method = herdado:<id>`, where `<id>` is the row of `stage1_preliminary_round.csv` that holds the original decision, reason, confidence and method.

| method of the S1 decision (4,054 records) | direct | through inheritance | total |
|---|---|---|---|
| rule (`regra`: explicit exclusion rule, such as no federated learning term or year before 2017) | 598 | 2,789 | 3,387 |
| manual reading of title and abstract (`leitura_manual`) | 115 | 489 | 604 |
| not recorded (ACM records of the preliminary round) | – | 63 | 63 |

## Known limitations

- **Residual duplicates.** Three pairs of records with the same normalized title were not merged by deduplication and count as separate records among the 4,863: V2-0945 / V2-3990 (R²Fed; the LaTeX superscript in the Scopus title prevented the match), V2-0763 / V2-2998 (FLPurifier; the Scopus copy has no DOI) and V2-0005 / V2-4724 (journal article of 2025 and arXiv preprint of 2023). In each pair both records received the same stage-1 decision. R²Fed was later included through snowballing as V2-0945, and its stage-2 reason records V2-3990 as a duplicate, so the corpus counts it once.
- **Snowballing records.** Records found only by snowballing (`SB-xx`) are not in `records.csv`, which holds database records. Their title, venue and origin are in `stage2_decisions.csv` (`stage2_reason_pt`, `snowballing_origin`) and in `snowballing_iteration1.csv`. SB-03, the only one in the main synthesis, is fully identified in `extraction/main_corpus.csv`.
