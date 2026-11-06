# Reinforcement Learning and Bandit-based Defenses for Robust Federated Learning: Systematic Literature Review Data

Supplementary material for the systematic review *Reinforcement Learning and Bandit-based Defenses for Robust Federated Learning: A Systematic Literature Review*.

The review asks whether the performance attributed to RL- and bandit-based federated learning (FL) defenses comes from learning or from the other components of the defense. This repository holds the protocol and its amendments, the search records, every screening decision, the extraction and quality forms, the reliability checks with the second reviewer, and scripts that recompute the counts reported in the paper.

## Contents

| folder | content |
|---|---|
| `protocol/` | review protocol v1.1 (original, in Portuguese) and the 27 dated amendments (A1–A27), with an English summary |
| `search/` | search strings, search log, reference set and validation of the strings, and the separate search for related reviews, with its selection and coding rules (see `search/README.md`) |
| `screening/` | 4,863 unique records, stage-1 decisions (with the preliminary round they inherit from) and stage-2 decisions, PRISMA flow, exclusion reasons, deduplication log and snowballing records (see `screening/README.md`) |
| `extraction/` | data dictionary, main corpus (77 studies), quality assessment (QA1–QA9), RQ7 corpus (34 works), non-RL adaptive defenses and the log of extraction revisions |
| `reliability/` | agreement between reviewers in both rounds, second reviewer's coded decisions, codebook and reconciliation rules |
| `scripts/` | `validate_counts.py`, `tables.py`, `figures.py` and `sensitivity.py`, which run on this repository; `pipeline/` holds the scripts used during the review |
| `outputs/` | tables and figures of the paper (LaTeX/TikZ) and the tables and figures regenerated from the data in this repository |

## Reproducing the counts

The scripts need only Python 3.9 or later and its standard library.

```
python scripts/validate_counts.py   # recomputes 65 counts of the paper and compares them with the reported values
python scripts/tables.py            # writes summary tables to outputs/generated_tables_and_figures/from_repository/
python scripts/figures.py           # writes the funnel and quality heatmap data and SVG drawings to the same folder
python scripts/sensitivity.py       # writes the sensitivity analysis to reliability/sensitivity_analysis.md
```

## Key numbers

- **Search (September 28, 2026):** 6,580 records from Scopus, IEEE Xplore, ACM Digital Library and arXiv. Deduplication left 4,863 unique records: 4,054 were screened with the main criteria and 809 were assessed only for RQ7.
- **Main synthesis:** 77 studies, 75 from the database searches and 2 from snowballing.
- **RQ7:** 34 works, 25 from the secondary searches, 4 from snowballing and 5 canonical readings.

## Conventions

- **Study identifiers.** `V2-xxxx` identifies a record from the database searches, and `SB-xx` a record found by snowballing that was not in the databases. The review on adaptive adversaries is cited in the paper as `eprint2025adaptive`, and in the RQ7 form as `C-Szelag`.
- **Codes.** `S`/`P`/`N` mean met / partially met / not met (in Portuguese, *sim*, *parcial*, *não*). `?` marks genuine ambiguity in the text, and `não reportado` marks information missing from the article.
- **Language.** Column names and documentation are in English. Free-text fields extracted from the articles are in Portuguese, and those columns end in `_pt` or are listed in `extraction/data_dictionary.md`. The original working documents (protocol, codebook, agreement analyses, sensitivity analysis) are kept in Portuguese in `original_pt/` subfolders, because they are the records used during the review.
- **Reviewers.** R1 is the first author, and R2 is the second reviewer. R2's decisions are included as coded values, together with the name of the primary metric R2 recorded for each RQ2 comparison. Free-text comments and the original spreadsheets are not included.
- **Use of an LLM.** The authors used Claude (Anthropic) to produce a preliminary structured extraction, which was compared field by field with the authors' manual records (`reliability/original_pt/comparacao_fichamento_autor_vs_claude.md`, `comparacao_QP7_autor_vs_claude.md`), to help convert those records into structured codes, and to generate the scripts that apply the predefined rules, compute counts and produce tables and figures. The authors read every full text, recorded each study manually, made all inclusion and final coding decisions, and interpreted the results. Every discrepancy affecting the synthesis was resolved against the original article.
- **Full texts.** The PDFs of the included studies are not distributed. Every study is identified by DOI or arXiv id in `extraction/main_corpus.csv` and `screening/records.csv`, except V2-2573, whose DOI printed in the PDF is not registered; its `notes` field gives the article page.

## Protocol status

The protocol (v1.1, dated September 27, 2026) was written before the search but was not preregistered. No frozen copy of the protocol before the search exists apart from v1.1 itself, and every later change is a dated amendment in `protocol/amendments/`. This is why the repository has no `original_protocol.pdf`.

## Licence

Data and documents are released under CC BY 4.0, and the code in `scripts/` under the MIT licence. See `LICENSE`.
