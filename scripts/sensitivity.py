"""Sensitivity analysis of the central RQ2 and quality counts.

Recomputes the counts under alternative readings of the boundary cases and under R2's coding before
consensus, and checks whether conclusions A-E of the paper hold in every scenario.

Usage: python scripts/sensitivity.py
Output: reliability/sensitivity_analysis.md
Only the Python standard library is required. This is the repository version of
scripts/pipeline/sensibilidade.py, updated for amendment A27 (the oracle no longer sets the category
when another admissible reference exists, and SARA, V2-0111, is a tie with the best fixed rule).
"""
import csv
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rows(path):
    with open(ROOT / path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


E = {r['id']: r for r in rows('extraction/main_corpus.csv')}
Q = {r['id']: r for r in rows('extraction/quality_assessment.csv')}
R2 = {r['id']: r for r in rows('reliability/r2_round2_rq2_agreement.csv') if r['id'] in E}
R2Q = {}
for r in rows('reliability/r2_round2_quality_agreement.csv'):
    if r['id'] in Q:
        # "?" stays with R1's code, as in the original analysis
        R2Q.setdefault(r['id'], {})[r['criterion']] = r['r2'] if r['r2'] in ('S', 'P', 'N') else r['r1']

CAT = {'none': 'none', 'same-signal heuristic': 'same', 'fixed action': 'fixed', 'different-signal heuristic': 'other',
       'random': 'random', 'partial ablation': 'partial', 'oracle': 'oracle'}
R2CAT = {'nenhuma': 'none', 'mesmo': 'same', 'fixa': 'fixed', 'outro': 'other', 'aleatoria': 'random',
         'parcial': 'partial', 'oraculo': 'oracle'}
RESULT = {'tie': 'tie', 'narrow win': 'narrow', 'clear win': 'clear'}
R2RESULT = {'empate': 'tie', 'estreita': 'narrow', 'clara': 'clear'}

base = {k: CAT[r['rq2_category']] for k, r in E.items()}
RES = {k: RESULT[r['rq2_closest_result']] for k, r in E.items() if r['rq2_closest_result']}
# R1's results for the two studies whose category was revised to partial ablation in favour of R2 (A21);
# they matter only in scenarios that move V2-3243 back to the closest comparisons
RES.update({'V2-3243': 'clear', 'V2-3331': 'narrow'})
ORACLE = {k for k, r in E.items() if r['rq2_has_oracle'] == 'S'}
NO_TEST = set()  # no study applies a statistical test to its comparison with the same-signal heuristic (R1)


def counts(cat, res, test):
    n = lambda c: sum(1 for v in cat.values() if v == c)
    same = [k for k, v in cat.items() if v == 'same']
    closest = [k for k, v in cat.items() if v in ('same', 'fixed')]
    return {
        'no comparison': n('none'),
        'some comparison': sum(1 for v in cat.values() if v != 'none'),
        'fixed action, heuristic or oracle': sum(1 for k, v in cat.items()
                                                 if v in ('fixed', 'same', 'other', 'oracle') or k in ORACLE),
        'same-signal heuristic': len(same),
        'same signal with >= 3 seeds and variability': sum(1 for k in same if Q[k]['QA2'] == 'S'),
        'statistical test on the comparison': sum(1 for k in same if k in test),
        'closest comparisons': len(closest),
        'ties': sum(1 for k in closest if res.get(k) == 'tie'),
        'closest without a classified result': sum(1 for k in closest if k not in res),
    }


def scenario(**changes):
    return dict(base, **changes)


S = {}
S['S0. Final R1 coding (paper)'] = (base, RES, NO_TEST)
S['F1. V2-1102 and V2-0973: static threshold of 0.5 treated as a fixed action'] = (
    scenario(**{'V2-1102': 'fixed', 'V2-0973': 'fixed'}), RES, NO_TEST)
S['F2. V2-3243: trimmed mean over the same signals treated as a same-signal heuristic'] = (
    scenario(**{'V2-3243': 'same'}), RES, NO_TEST)
S['F3. V2-4059 and V2-0835: heuristics treated as same-signal'] = (
    scenario(**{'V2-4059': 'same', 'V2-0835': 'same'}), RES, NO_TEST)
S['F4. Power-of-Choice (V2-0542, V2-1140, V2-1199, V2-3215) not counted as a heuristic (random remains)'] = (
    scenario(**{k: 'random' for k in ('V2-0542', 'V2-1140', 'V2-1199', 'V2-3215')}), RES, NO_TEST)
S['F5. Broad definition: external aggregators count as non-learned policies (group C of A14)'] = (
    scenario(**{k: 'fixed' for k in ('V2-1042', 'V2-1185', 'V2-0918', 'V2-1231', 'V2-3175', 'V2-1001', 'V2-0530',
                                     'V2-3494')}), RES, NO_TEST)
S['F6. Comparisons rejected at reconciliation accepted (V2-0922, V2-1229)'] = (
    scenario(**{'V2-0922': 'random', 'V2-1229': 'random'}), RES, NO_TEST)
res_o1 = dict(RES, **{k: 'tie' for k, v in RES.items() if v == 'narrow'})
S['O1. Narrow wins (up to about 6 points, no variability) treated as ties'] = (base, res_o1, NO_TEST)
res_o2 = dict(RES, **{'V2-1327': 'narrow', 'V2-2103': 'narrow', 'V2-4540': 'narrow'})
S['O2. Ties in which some metric favours the agent treated as wins'] = (base, res_o2, NO_TEST)
# R2's "fixed action (no defense)" counts as no comparison (A20); "?" keeps R1's category
r2cat = dict(base, **{k: 'none' if r['r2_no_defense'] == 'S' else R2CAT[r['r2']] for k, r in R2.items() if r['r2'] in R2CAT})
r2res = {k: R2RESULT[r['r2_result']] for k, r in R2.items() if r['r2_result'] in R2RESULT}
r2test = {k for k, r in R2.items() if r['r2_test'] == 'S'}
S["R2. R2's categories and results (codebook v2) before consensus"] = (r2cat, r2res, r2test)
S['X1. Most favourable to learning (F2 + F3 + O2)'] = (
    scenario(**{'V2-3243': 'same', 'V2-4059': 'same', 'V2-0835': 'same'}), res_o2, NO_TEST)
S['X2. Least favourable to learning (F1 + O1)'] = (
    scenario(**{'V2-1102': 'fixed', 'V2-0973': 'fixed'}), res_o1, NO_TEST)

CONCLUSIONS = {
    'A': ('most studies do not compare with a same-signal heuristic', lambda k: k['same-signal heuristic'] < len(E) / 2),
    'B': ('fewer than 1/4 of the studies use a same-signal heuristic', lambda k: k['same-signal heuristic'] < len(E) / 4),
    'C': ('no same-signal comparison has a statistical test', lambda k: k['statistical test on the comparison'] == 0),
    'D': ('there are ties among the closest comparisons', lambda k: k['ties'] > 0),
    'E': ('fewer than 10% of the studies compare with the same signal using >= 3 seeds and variability',
          lambda k: k['same signal with >= 3 seeds and variability'] < len(E) / 10),
}

out = ['# Sensitivity analysis: RQ2 and quality', '',
       'Generated by `scripts/sensitivity.py` from the files of this repository. Each scenario changes only the items named; '
       'everything else follows R1\'s final coding. Scenario R2 uses R2\'s blind round-2 coding before consensus '
       '(`r2_round2_rq2_agreement.csv`, `r2_round2_quality_agreement.csv`); where R2 coded "?", R1\'s code is kept.', '',
       '## RQ2: central counts by scenario', '']
results = {name: counts(*args) for name, args in S.items()}
cols = list(results['S0. Final R1 coding (paper)'])
out += ['| scenario | ' + ' | '.join(cols) + ' |', '|---|' + '---|' * len(cols)]
out += [f'| {name} | ' + ' | '.join(str(k[c]) for c in cols) + ' |' for name, k in results.items()]
out += ['', '## RQ2: do the conclusions hold?', '', '| scenario | ' + ' | '.join(CONCLUSIONS) + ' |',
        '|---|' + '---|' * len(CONCLUSIONS)]
out += [f'| {name} | ' + ' | '.join('yes' if f(k) else '**no**' for _, f in CONCLUSIONS.values()) + ' |'
        for name, k in results.items()]
out += [''] + [f'- **{c}.** {text}' for c, (text, _) in CONCLUSIONS.items()]

score = {'S': 1, 'P': 0.5, 'N': 0}
r1_total = {k: sum(score[r[f'QA{i}']] for i in range(1, 10)) for k, r in Q.items()}
r2_total = dict(r1_total, **{k: sum(score[r[f'QA{i}']] for i in range(1, 10)) for k, r in R2Q.items()})
lenient = {k: sum(0.5 if i in (2, 3, 7, 9) and r[f'QA{i}'] == 'N' else score[r[f'QA{i}']] for i in range(1, 10))
           for k, r in Q.items()}


def qa_count(i, value, use_r2):
    return sum(1 for k, r in Q.items() if (R2Q[k][f'QA{i}'] if use_r2 and k in R2Q else r[f'QA{i}']) == value)


def quality_row(name, total, use_r2):
    return (f'| {name} | {st.mean(total.values()):.2f} | {st.median(total.values()):.1f} | '
            f'{sum(t >= 5 for t in total.values())} | {qa_count(2, "S", use_r2)} | {qa_count(3, "S", use_r2)} | '
            f'{qa_count(1, "N", use_r2)} |')


out += ['', '## Quality', '',
        '| scenario | mean | median | score >= 5 | QA2 = S (>= 3 seeds) | QA3 = S (test) | QA1 = N (uses the test set) |',
        '|---|---|---|---|---|---|---|',
        quality_row('Q0. Final R1 scores (paper)', r1_total, False),
        quality_row(f"Q1. R2's scores (codebook v2) on the {len(R2Q)} sampled studies, before consensus", r2_total, True),
        quality_row('Q2. Lenient convention: "not documented" counts 0.5 in QA2, QA3, QA7 and QA9', lenient, False),
        '', 'Q2 is an upper bound: it treats as partially met everything the article does not document.']

(ROOT / 'reliability' / 'sensitivity_analysis.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('written to reliability/sensitivity_analysis.md')
