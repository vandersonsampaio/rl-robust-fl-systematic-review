"""Recompute the counts reported in the paper from the CSV files of this repository.

Usage: python scripts/validate_counts.py
Exits with status 1 if any recomputed value differs from the value reported in the paper.
Only the Python standard library is required.
"""
import csv
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rows(path):
    with open(ROOT / path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


checks = []


def check(label, value, expected):
    checks.append((label, value, expected, value == expected))


# ------------------------------------------------------------------ screening (PRISMA, Fig. 2)
s1 = rows('screening/stage1_decisions.csv')
s2 = rows('screening/stage2_decisions.csv')
dedup = rows('screening/deduplication_log.csv')
check('records identified', len(dedup), 6580)
check('unique records', len(s1), 4863)
check('screened with S1 criteria', sum(1 for r in s1 if r['s1_decision']), 4054)
check('assessed exclusively for RQ7', sum(1 for r in s1 if not r['s1_decision']), 809)
c1 = Counter(r['s1_decision'] for r in s1 if r['s1_decision'])
check('stage 1: full texts sought (I + D)', c1['I'] + c1['D'], 124)
check('stage 1: excluded (all codes except EC2)', sum(v for k, v in c1.items() if k.startswith('E-') and k != 'E-EC2'), 3904)
snow = lambda r: r['via_snowballing'].strip().upper().startswith('S')
main2 = [r for r in s2 if r['flow'] == 'S1' and not snow(r)]
c2 = Counter(r['stage2_decision'] for r in main2)
check('stage 2: full texts sought', len(main2), 124)
check('stage 2: not retrieved', c2['nao_recuperado'], 4)
check('stage 2: assessed', len(main2) - c2['nao_recuperado'], 120)
check('stage 2: excluded', sum(v for k, v in c2.items() if k.startswith('E-')), 45)
check('included through database searches', c2['I'], 75)
check('included through snowballing', sum(1 for r in s2 if r['flow'] == 'S1' and snow(r) and r['stage2_decision'] == 'I'), 2)
q7 = [r for r in s2 if r['flow'] == 'QP7']
check('RQ7 included through searches', sum(1 for r in q7 if not snow(r) and r['stage2_decision'] == 'Q7-I'), 25)
check('RQ7 included through snowballing', sum(1 for r in q7 if snow(r) and r['stage2_decision'] == 'Q7-I'), 4)
for fl, name in (('S1', 'main'), ('QP7', 'RQ7')):
    sb = [r for r in s2 if r['flow'] == fl and snow(r)]
    nr = sum(1 for r in sb if r['stage2_decision'] == 'nao_recuperado')
    check(f'snowballing ({name}): full texts assessed', len(sb) - nr, 5)
    check(f'snowballing ({name}): not retrieved', nr, 1)
flow = {r['step']: r for r in rows('screening/screening_flow.csv')}
check('screening_flow.csv total main synthesis', flow['total included']['main_synthesis'], '77')

# ------------------------------------------------------------------ corpus and RQ2
E = rows('extraction/main_corpus.csv')
check('studies in the main synthesis', len(E), 77)
check('peer-reviewed studies', sum(1 for r in E if r['peer_reviewed'].strip().upper().startswith('S')), 73)
cat = Counter(r['rq2_category'] for r in E)
check('RQ2: no non-learned comparison', cat['none'], 32)
check('RQ2: some non-learned comparison', len(E) - cat['none'], 45)
# any comparison with a fixed action, a heuristic or an oracle (the oracle does not set the category, A27)
strong = sum(1 for r in E if r['rq2_category'] in ('fixed action', 'same-signal heuristic', 'different-signal heuristic', 'oracle')
             or r['rq2_has_oracle'] == 'S')
check('RQ2: fixed action, heuristic or oracle', strong, 23)
check('RQ2: same-signal heuristic', cat['same-signal heuristic'], 6)
check('RQ2: fixed action that is a defense', cat['fixed action'], 9)
check('RQ2: oracle as the only reference', cat['oracle'], 1)
check('RQ2: studies with an oracle comparison', sum(r['rq2_has_oracle'] == 'S' for r in E), 3)
check('RQ2: different-signal heuristic', cat['different-signal heuristic'], 6)
closest = [r for r in E if r['rq2_category'] in ('same-signal heuristic', 'fixed action')]
res = Counter(r['rq2_closest_result'] for r in closest)
check('RQ2: closest comparisons', len(closest), 15)
check('RQ2: ties among closest comparisons', res['tie'], 7)
check('RQ2: wins among closest comparisons', res['narrow win'] + res['clear win'], 8)

# ------------------------------------------------------------------ quality (Table QA aggregate)
Q = {r['id']: r for r in rows('extraction/quality_assessment.csv')}
expected_qa = {1: (38, 20, 19), 2: (13, 12, 52), 3: (7, 0, 70), 4: (9, 3, 65), 5: (15, 30, 32),
               6: (2, 72, 3), 7: (22, 47, 8), 8: (10, 16, 51), 9: (5, 15, 57)}
for i, exp in expected_qa.items():
    c = Counter(Q[r['id']][f'QA{i}'] for r in E)
    check(f'QA{i} S/P/N', (c['S'], c['P'], c['N']), exp)
score = {'S': 1, 'P': 0.5, 'N': 0}
tot = [sum(score[Q[r['id']][f'QA{i}']] for i in range(1, 10)) for r in E]
check('quality: mean score (2 decimals)', round(statistics.mean(tot), 2), 2.97)
check('quality: median score', statistics.median(tot), 3.0)
check('quality: maximum score', max(tot), 8.5)
check('quality: studies with score >= 5', sum(1 for t in tot if t >= 5), 8)
same = [r['id'] for r in E if r['rq2_category'] == 'same-signal heuristic']
check('same-signal studies with QA2 = S', sum(1 for i in same if Q[i]['QA2'] == 'S'), 1)

# ------------------------------------------------------------------ RQ7
check('RQ7 corpus', len(rows('extraction/rq7_corpus.csv')), 34)

# ------------------------------------------------------------------ inter-rater agreement (Table Reliability)
def agreement(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / n ** 2
    return n, round(po, 3), round((po - pe) / (1 - pe), 2)


def check_agreement(label, a, b, expected):
    n, po, kappa = agreement(a, b)
    check(f'{label}: n', n, expected[0])
    check(f'{label}: agreement', po, expected[1])
    check(f'{label}: kappa', kappa, expected[2])


blind = rows('reliability/stage1_blind_sample.csv')
check_agreement('agreement stage 1', [r['r1_binary'] for r in blind], [r['r2_binary'] for r in blind], (811, 0.986, 0.74))
cons = [r for r in rows('reliability/stage2_consensus.csv') if r['check'] in ('A_exclusoes', 'B_inclusoes')]
binary = lambda d: 'I' if d == 'I' else 'E'
check_agreement('agreement stage 2 (round 1)', [binary(r['r1']) for r in cons], [binary(r['r2_original']) for r in cons],
                (52, 0.654, 0.35))
rq2 = rows('reliability/r2_round2_rq2_agreement.csv')
r1_cat = {r['id']: r['r1_before_consensus'] for r in rq2}
r2_round1 = {'fixa': 'fixa', 'heurística (mesmo sinal)': 'mesmo', 'heurística (outro sinal)': 'outro',
             'parcial/ablação': 'parcial', 'aleatória': 'aleatoria', 'Nenhuma': 'nenhuma'}
rq2_r1 = rows('reliability/r2_round1_rq2.csv')
check_agreement('agreement RQ2 (round 1)', [r1_cat[r['id']] for r in rq2_r1],
                [r2_round1.get(r['comparison'], r['comparison']) for r in rq2_r1], (52, 0.346, 0.14))
coded = [r for r in rq2 if r['r2'] != '?']
check_agreement('agreement RQ2 (round 2)', [r['r1_before_consensus'] for r in coded], [r['r2'] for r in coded],
                (51, 0.588, 0.49))
qual = rows('reliability/r2_round2_quality_agreement.csv')
q1 = [r for r in qual if r['r2_round1']]
check_agreement('agreement quality (round 1)', [r['r1'] for r in q1], [r['r2_round1'] for r in q1], (144, 0.431, 0.15))
q2 = [r for r in qual if r['r2'] in ('S', 'P', 'N')]
check_agreement('agreement quality (round 2)', [r['r1'] for r in q2], [r['r2'] for r in q2], (223, 0.794, 0.67))

# ------------------------------------------------------------------ report
width = max(len(c[0]) for c in checks)
fail = 0
for label, value, expected, ok in checks:
    fail += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {label:<{width}}  {value}" + ('' if ok else f'  (paper: {expected})'))
print(f'\n{len(checks) - fail} of {len(checks)} checks match the paper.')
sys.exit(1 if fail else 0)
