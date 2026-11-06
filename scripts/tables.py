"""Regenerate the summary tables of the paper from the CSV files of this repository.

Usage: python scripts/tables.py
Output: outputs/generated_tables_and_figures/from_repository/*.csv and tables.md
Only the Python standard library is required.
"""
import csv
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs' / 'generated_tables_and_figures' / 'from_repository'


def rows(path):
    with open(ROOT / path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save(name, header, data):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / name, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        w.writerows(data)
    return header, data


def md(title, header, data):
    lines = [f'## {title}', '', '| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    lines += ['| ' + ' | '.join(str(x) for x in r) + ' |' for r in data]
    return '\n'.join(lines) + '\n'


E = rows('extraction/main_corpus.csv')
Q = {r['id']: r for r in rows('extraction/quality_assessment.csv')}
out = ['# Tables regenerated from the repository data', '']

# Corpus by year and peer review
years = Counter(r['year'] for r in E)
out.append(md('Studies by year', *save('corpus_by_year.csv', ['year', 'studies'], sorted(years.items()))))
peer = Counter('peer-reviewed' if r['peer_reviewed'].strip().upper().startswith('S') else 'preprint' for r in E)
out.append(md('Peer review', *save('corpus_peer_review.csv', ['status', 'studies'], sorted(peer.items()))))

# RQ2: strongest non-learned reference
order = ['same-signal heuristic', 'fixed action', 'different-signal heuristic', 'random', 'partial ablation', 'oracle', 'none']
cat = Counter(r['rq2_category'] for r in E)
out.append(md('RQ2: strongest non-learned reference per study',
              *save('rq2_categories.csv', ['category', 'studies'], [(c, cat[c]) for c in order])))

# RQ2: closest comparisons (Table QP2, first two groups)
closest = [(r['id'], r['rq2_category'], r['rq2_closest_result'], r['seeds_statistics'][:80])
           for r in E if r['rq2_category'] in ('same-signal heuristic', 'fixed action')]
out.append(md('RQ2: closest comparisons (same-signal heuristic or fixed action that is a defense)',
              *save('rq2_closest_comparisons.csv', ['id', 'category', 'result', 'runs_and_statistics_pt'], closest)))

# Quality: aggregate table (Table QA aggregate)
agg = []
for i in range(1, 10):
    c = Counter(Q[r['id']][f'QA{i}'] for r in E)
    agg.append((f'QA{i}', c['S'], c['P'], c['N']))
out.append(md('Quality assessment: studies per score (S = 1, P = 0.5, N = 0)',
              *save('quality_aggregate.csv', ['criterion', 'S', 'P', 'N'], agg)))
score = {'S': 1, 'P': 0.5, 'N': 0}
tot = [sum(score[Q[r['id']][f'QA{i}']] for i in range(1, 10)) for r in E]
summary = [('mean', round(statistics.mean(tot), 2)), ('median', statistics.median(tot)), ('max', max(tot)),
           ('studies with score >= 5', sum(t >= 5 for t in tot))]
out.append(md('Quality assessment: total score', *save('quality_total.csv', ['statistic', 'value'], summary)))

(OUT / 'tables.md').write_text('\n'.join(out), encoding='utf-8')
print('written to', OUT.relative_to(ROOT))
