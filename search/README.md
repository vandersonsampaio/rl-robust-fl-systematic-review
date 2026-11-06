# Search

| file | content |
|---|---|
| `search_strings.md` | final strings S1, S2a and S2b per database, number of records per database and string, and the string of the separate search for related reviews |
| `search_log.csv` | every search run, in order: preliminary runs of September 27, validation runs, final runs of September 28, the Web of Science string (not run) and the deduplication step |
| `reference_set.csv` | reference set used to validate S1 (Q1–Q5 and the boundary controls B1, B2) and the outcome of each study |
| `reference_set_validation.md` | how S1 and S2 were validated: diagnosis of the original S1, the revised blocks, the arXiv API limitation and the split of S2 into S2a and S2b |
| `arxiv_queries/` | exact queries sent to the arXiv API (`string_arxiv_revisada_all.txt` for S1, `string_arxiv_s2_revisada.txt` for S2a, `string_arxiv_s2b.txt` for S2b) |
| `related_reviews/review_search_records.csv` | the 404 unique records of the separate search for related reviews, with screening and coding |
| `related_reviews/selection_and_coding_rules.md` | how the 404 records were reduced to 45 central reviews, how the works of the related-work table were selected, and how its columns were coded |
| `original_pt/`, `related_reviews/original_pt/` | the original working documents in Portuguese (see below) |

Column definitions and codes are in `extraction/data_dictionary.md`, section `search/`.

## Record counts

The counts in `search_strings.md` and in the paper (6,580 records identified, 1,717 duplicates) are the rows of the exported files. The Scopus S1 search was exported in three overlapping batches because of the 2,000-record display limit (amendment A5): its 4,226 rows hold 3,541 distinct records, and the 685 repeated rows were removed during deduplication together with the duplicates across databases and strings. `screening/deduplication_log.csv` has one row per exported record, with its export file.

## Original working documents

The files in `original_pt/` are the records written during the review, kept in Portuguese and unedited. They are not translated one to one. Their content is given in English in the files below.

| original (Portuguese) | English content |
|---|---|
| `original_pt/search_strings_S1_S2_pt.md` | `search_strings.md`. The original is the string file written before the final runs, with execution instructions. The English file gives the text actually executed. |
| `original_pt/reference_set_validation_pt.md` | `reference_set_validation.md` and `reference_set.csv` |
| `related_reviews/original_pt/selection_and_coding_rules_pt.md` | `related_reviews/selection_and_coding_rules.md` |

The original documents refer to the working folders and column names used during the review. Their correspondence with this repository is:

| in the original documents | in this repository |
|---|---|
| `triagem/log_buscas.csv` | `search/search_log.csv` |
| `validacao/validacao_6.4.md` | `search/original_pt/reference_set_validation_pt.md` |
| `buscas_strings_S1_S2.md` | `search/original_pt/search_strings_S1_S2_pt.md` |
| `string_arxiv_revisada_all.txt` and the other arXiv strings | `search/arxiv_queries/` (`string_arxiv_revisada.txt`, the `abs` variant not adopted, is not included) |
| `scripts/validar_qgs.py`, `scripts/busca_arxiv.py`, `scripts/busca_revisoes.py` | `scripts/pipeline/` |
| `SLR_Related/revisoes_consolidado.csv` | `search/related_reviews/review_search_records.csv` |
| columns `triagem`, `rl_objeto`, `s1_decisao` | `screening`, `rl_as_object`, `s1_decision` |
| QGS (*quasi-gold standard*) | reference set |
| §6.2, §6.3, §6.4, §15.3 | sections of `protocol/protocol_v1.1_pt.md` |
