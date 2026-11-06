# Scripts

## Scripts that run on this repository

These four scripts need only Python 3.9 or later and its standard library.

| script | what it does |
|---|---|
| `validate_counts.py` | recomputes the counts reported in the paper (PRISMA flow, RQ2 categories and closest comparisons, QA1–QA9 distributions and totals, RQ7, inter-rater agreement) from the CSV files and compares each one with the reported value; exits with status 1 on any mismatch |
| `tables.py` | regenerates the summary tables (corpus by year, peer review, RQ2 categories, closest comparisons, quality aggregate and totals) in `outputs/generated_tables_and_figures/from_repository/` |
| `figures.py` | regenerates the data of the evidence funnel and of the quality heatmap and draws both as SVG in the same folder |
| `sensitivity.py` | recomputes the central RQ2 and quality counts under alternative readings and under R2's coding, and writes `reliability/sensitivity_analysis.md`; repository version of `pipeline/sensibilidade.py`, updated for amendment A27 |

## pipeline/

`pipeline/` holds the scripts used during the review, as they were run. They are kept for transparency and are not meant to run on this repository's layout, because they read the working folders of the review (`triagem_v2/`, `validacao/`, `paper_latex/`), which contain the full texts and other files that cannot be redistributed. Their names and comments are in Portuguese. The main ones are:

| script | role |
|---|---|
| `triagem_v2.py` | deduplication and stage-1 screening; writes the PRISMA counts of stage 1 |
| `amostra_revisor2.py` | draws the calibration set and the 20% blind sample for R2 (seed 20261005) |
| `kappa_revisor2.py` | stage-1 agreement (kappa, PABAK) |
| `etapa2_lote2.py` | stage-2 decisions, main extraction and quality scores (QA rules), applying `extraction_revisions.csv` |
| `extracao_qp7.py` | RQ7 extraction form |
| `sintese.py` | synthesis of RQ1–RQ6 and the final PRISMA flow |
| `concordancia_qp2_R2v2.py`, `concordancia_qualidade_R2v2.py` | round-2 agreement with R2 |
| `sensibilidade.py` | sensitivity analysis of the RQ2 and quality counts |
| `fig_funil.py`, `fig_qa_heatmap.py`, `tabelas_latex.py` | figures and tables of the paper (TikZ/pgfplots and LaTeX) |
| `busca_revisoes.py` | consolidation of the separate search for related reviews |
