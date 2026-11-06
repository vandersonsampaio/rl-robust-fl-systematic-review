"""Regenerate the data of the evidence funnel and the quality heatmap, and draw both as SVG.

Usage: python scripts/figures.py
Output: outputs/generated_tables_and_figures/from_repository/funnel.csv, funnel.svg,
        quality_heatmap.csv and quality_heatmap.svg.
The figures in the paper are drawn with TikZ/pgfplots (outputs/generated_tables_and_figures/paper_figures/);
these SVG files show the same data. Only the Python standard library is required.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs' / 'generated_tables_and_figures' / 'from_repository'


def rows(path):
    with open(ROOT / path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


E = rows('extraction/main_corpus.csv')
Q = {r['id']: r for r in rows('extraction/quality_assessment.csv')}
OUT.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ evidence funnel
same = [r for r in E if r['rq2_category'] == 'same-signal heuristic']
steps = [
    ('Studies in the main synthesis', len(E)),
    ('Some non-learned policy', sum(r['rq2_category'] != 'none' for r in E)),
    ('Fixed action, heuristic or oracle',
     sum(r['rq2_category'] in ('fixed action', 'same-signal heuristic', 'different-signal heuristic', 'oracle')
         or r['rq2_has_oracle'] == 'S' for r in E)),
    ('Heuristic on the same signal', len(same)),
    ('Same signal, >= 3 seeds and variability', sum(Q[r['id']]['QA2'] == 'S' for r in same)),
    ('Same signal, statistical test on the comparison', 0),  # coded in the RQ2 reading; none applies a test
]
with open(OUT / 'funnel.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['step', 'studies'])
    w.writerows(steps)
W, bar, gap, left = 760, 28, 10, 330
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{len(steps) * (bar + gap) + 20}" font-family="sans-serif" font-size="13">']
for k, (label, n) in enumerate(steps):
    y = 10 + k * (bar + gap)
    w = (W - left - 60) * n / steps[0][1]
    svg += [f'<text x="{left - 8}" y="{y + bar * 0.68}" text-anchor="end">{label}</text>',
            f'<rect x="{left}" y="{y}" width="{max(w, 1):.1f}" height="{bar}" fill="#4a78b5"/>',
            f'<text x="{left + w + 6:.1f}" y="{y + bar * 0.68}">{n}</text>']
(OUT / 'funnel.svg').write_text('\n'.join(svg + ['</svg>']) + '\n', encoding='utf-8')

# ------------------------------------------------------------------ quality heatmap (studies ordered by total)
score = {'S': 1.0, 'P': 0.5, 'N': 0.0}
ids = sorted(Q, key=lambda i: (-sum(score[Q[i][f'QA{c}']] for c in range(1, 10)), i))
with open(OUT / 'quality_heatmap.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['criterion'] + ids)
    for c in range(1, 10):
        w.writerow([f'QA{c}'] + [Q[i][f'QA{c}'] for i in ids])
cell, top, lft = 11, 70, 50
color = {'S': '#1f6f3f', 'P': '#9cc9a8', 'N': '#f2f2f2'}
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{lft + cell * len(ids) + 20}" height="{top + cell * 9 + 20}" font-family="sans-serif" font-size="10">']
for j, i in enumerate(ids):
    x = lft + j * cell + cell * 0.7
    svg.append(f'<text transform="translate({x:.1f},{top - 4}) rotate(-90)">{i.replace("V2-", "")}</text>')
for c in range(1, 10):
    y = top + (c - 1) * cell
    svg.append(f'<text x="{lft - 6}" y="{y + cell * 0.8}" text-anchor="end">QA{c}</text>')
    for j, i in enumerate(ids):
        svg.append(f'<rect x="{lft + j * cell}" y="{y}" width="{cell - 1}" height="{cell - 1}" fill="{color[Q[i][f"QA{c}"]]}"/>')
(OUT / 'quality_heatmap.svg').write_text('\n'.join(svg + ['</svg>']) + '\n', encoding='utf-8')
print('written to', OUT.relative_to(ROOT))
