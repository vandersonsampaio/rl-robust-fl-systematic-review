# Extraction

| file | content |
|---|---|
| `data_dictionary.md` | columns and codes of every CSV file in the repository |
| `main_corpus.csv` | extraction form of the 77 studies of the main synthesis (RQ1–RQ6) |
| `quality_assessment.csv` | QA1–QA9 scores, total and rationale for the 77 studies |
| `rq7_corpus.csv` | form of the 34 works of RQ7 (audits, benchmarks, SoKs and canonical readings) |
| `non_rl_adaptive_defenses.csv` | reduced form of the adaptive defenses without RL or bandits that were read in full text (protocol §9.2) |
| `extraction_revisions.csv` | every field corrected after the preliminary extraction, in order; `main_corpus.csv` already includes them |
| `code_availability_check.md` | how QA4 was checked against each study's repository (amendment A24) |
| `original_pt/code_availability_check_pt.md` | the original of the code check, in Portuguese |

The free-text fields are in Portuguese. The extraction was compared field by field with R1's manual reading notes (amendment A14; `reliability/original_pt/comparacao_fichamento_autor_vs_claude.md`).

## Deviations and limitations

- **Non-RL adaptive defenses (protocol §9.2).** The protocol gives a reduced form to every record excluded under EC2. Forms were filled only for the defenses read in full text: the five excluded under EC2 at stage 2 and two RQ7 works that would fall under EC2 in S1. The 26 records excluded under EC2 at stage 1 are identified in `screening/stage1_decisions.csv` (`full_text_sought = §9.2`) but were not read in full and have no form.
- **QA4 for V2-0688 and V2-1057.** Their IEEE supplements could not be opened, and both are scored N (see `code_availability_check.md`).

## Paths in the original documents

| in the original documents | in this repository |
|---|---|
| `triagem_v2/extracao_principal.csv` | `extraction/main_corpus.csv` |
| `triagem_v2/qualidade.csv` | `extraction/quality_assessment.csv` |
| `triagem_v2/extracao_qp7.csv` | `extraction/rq7_corpus.csv` |
| `extracao_adaptativo_nao_rl.csv` | `extraction/non_rl_adaptive_defenses.csv` |
| `triagem_v2/revisao_extracao.tsv` | `extraction/extraction_revisions.csv` |
| `scripts/<name>.py` | `scripts/pipeline/<name>.py` |
