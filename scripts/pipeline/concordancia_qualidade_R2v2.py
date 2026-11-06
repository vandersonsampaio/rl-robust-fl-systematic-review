"""Concordância R1 × R2 na qualidade (QA1–QA9), reclassificação cega com livro de códigos v2 (adendo A19).

Entrada: validacao/reclassificacao_R2/planilha_cega_R2_Qualidade.xlsx (aba Qualidade, 26 estudos),
         validacao/chave_amostra_R2_v2.csv, reclassificacao_R2/qualidade_R1_antes_A20.csv (R1 antes do consenso;
         a concordância reportada é contra ela) e triagem_v2/qualidade.csv (R1 depois do A20, só para comparação)
         e triagem_v2/revisor2/Qualidade.csv (R2 na rodada anterior, A16).
"?" do R2 fica fora do κ do critério (analisado à parte; cenário alternativo: "?" = P).
Saída: validacao/reclassificacao_R2/concordancia_qualidade_R2v2.csv (uma linha por estudo × critério)
       e validacao/reclassificacao_R2/concordancia_qualidade_R2v2.md.
"""
import csv
import statistics as st
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parent.parent
V = RAIZ / 'validacao'
D = V / 'reclassificacao_R2'
NUM = {'S': 1.0, 'P': 0.5, 'N': 0.0}
CAT = ['S', 'P', 'N']
QA = range(1, 10)
NOME = {1: 'recompensa sem teste', 2: '≥3 sementes + variab.', 3: 'teste estatístico', 4: 'código',
        5: 'política não aprendida', 6: 'ataques fiéis', 7: 'hiperparâm. do agente', 8: 'defesas fortes',
        9: 'ataque adaptativo'}


def rows(p):
    return list(csv.DictReader(open(p, encoding='utf-8-sig')))


def cod(x):
    x = (x or '').strip()
    return x[:1].upper() if x else ''


def kappa(pares, pesos=False):
    """κ de Cohen (S/P/N); com pesos=True, κ ponderado linear (escala ordinal)."""
    n = len(pares)
    if not n:
        return float('nan')
    idx = {c: i for i, c in enumerate(CAT)}
    w = lambda a, b: 1 - abs(idx[a] - idx[b]) / 2 if pesos else float(a == b)
    po = sum(w(a, b) for a, b in pares) / n
    m1, m2 = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(w(a, b) * m1[a] * m2[b] for a in CAT for b in CAT) / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')


def f(x, d=2):
    return '—' if x != x else f'{x:.{d}f}'.replace('.', ',')


chave = {r['id']: r for r in rows(V / 'chave_amostra_R2_v2.csv') if r['na_qualidade'] == 'True'}
R1 = {r['id']: r for r in rows(D / 'qualidade_R1_antes_A20.csv')}
R1n = {r['id']: r for r in rows(RAIZ / 'triagem_v2' / 'qualidade.csv')}
R2a = {r['id']: r for r in rows(RAIZ / 'triagem_v2' / 'revisor2' / 'Qualidade.csv')}
ws = load_workbook(D / 'planilha_cega_R2_Qualidade.xlsx')['Qualidade']
cab = [c.value for c in ws[1]]
R2 = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0]:
        R2[row[0]] = dict(zip(cab, row))

ids = sorted(chave)
assert set(ids) == set(R2), (set(ids) ^ set(R2))
vazios = [(i, k) for i in ids for k in QA if not cod(R2[i][f'QA{k}'])]
sem_onde = [(i, k) for i in ids for k in QA if not (R2[i][f'QA{k} onde'] or '').strip()]

linhas = []
for i in ids:
    for k in QA:
        a, b = cod(R1[i][f'qa{k}_r1']), cod(R2[i][f'QA{k}'])
        ant = cod(R2a[i][f'QA{k}']) if i in R2a else ''
        linhas.append({'id': i, 'origem': chave[i]['origem_qualidade'], 'categoria_qp2_r1': chave[i]['categoria_R1'],
                       'qa': f'QA{k}', 'r1': a, 'r2': b, 'concorda': a == b, 'r2_anterior': ant,
                       'r2_onde': R2[i][f'QA{k} onde'] or ''})
with open(D / 'concordancia_qualidade_R2v2.csv', 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(linhas[0]))
    w.writeheader()
    w.writerows(linhas)


def bloco(sel, interrog='fora'):
    """Retorna pares (r1, r2) válidos; '?' sai ou vira P."""
    out = []
    for x in sel:
        b = x['r2']
        if b == '?':
            if interrog == 'fora':
                continue
            b = 'P'
        out.append((x['r1'], b))
    return out


def resumo(sel, interrog='fora'):
    p = bloco(sel, interrog)
    n = len(p)
    return n, sum(a == b for a, b in p) / n if n else float('nan'), kappa(p), kappa(p, True)


out = ['# Concordância R1 × R2 na qualidade: reclassificação cega (livro de códigos v2)', '',
       'Gerado por `scripts/concordancia_qualidade_R2v2.py`. R1 = pontuação existente antes do consenso (`qualidade_R1_antes_A20.csv`); '
       'R2 = `planilha_cega_R2_Qualidade.xlsx`, antes de qualquer consenso. O "?" do R2 fica fora do κ do critério; '
       'o cenário "? = P" está na última coluna.', '',
       f'**Integridade:** {len(ids)} estudos, {len(ids) * 9} decisões; células vazias = {len(vazios)}; '
       f'decisões sem "onde" = {len(sem_onde)}; "?" = {sum(x["r2"] == "?" for x in linhas)}.', '']

n, po, k, kw = resumo(linhas)
n2, po2, k2, kw2 = resumo(linhas, 'P')
out += ['## Resultado geral', '',
        '| conjunto | n decisões | concordância | κ | κ ponderado | κ com "? = P" |', '|---|---|---|---|---|---|',
        f'| todos os 26 estudos | {n} | {f(po * 100, 1)}% | {f(k)} | {f(kw)} | {f(k2)} |']
for org, rot in (('amostra anterior', 'os 16 da amostra anterior'), ('nova', 'os 10 novos')):
    s = [x for x in linhas if x['origem'] == org]
    a, b, c, d = resumo(s)
    out.append(f'| {rot} | {a} | {f(b * 100, 1)}% | {f(c)} | {f(d)} | {f(resumo(s, "P")[2])} |')

# rodada anterior nos mesmos 16
s16 = [x for x in linhas if x['r2_anterior']]
pa = [(x['r1'], x['r2_anterior']) for x in s16 if x['r2_anterior'] in CAT]
out.append(f'| *referência: rodada anterior (A16), mesmos 16* | {len(pa)} | '
           f'{f(sum(a == b for a, b in pa) / len(pa) * 100, 1)}% | {f(kappa(pa))} | {f(kappa(pa, True))} | — |')

out += ['', '## Por critério', '',
        '| critério | concordância | κ | κ ponderado | R1 S/P/N | R2 S/P/N/? | R2 acima | R2 abaixo |',
        '|---|---|---|---|---|---|---|---|']
for q in QA:
    s = [x for x in linhas if x['qa'] == f'QA{q}']
    n, po, k, kw = resumo(s)
    c1, c2 = Counter(x['r1'] for x in s), Counter(x['r2'] for x in s)
    acima = sum(1 for x in s if x['r2'] in NUM and NUM[x['r2']] > NUM[x['r1']])
    abaixo = sum(1 for x in s if x['r2'] in NUM and NUM[x['r2']] < NUM[x['r1']])
    out.append(f'| QA{q}. {NOME[q]} | {sum(a == b for a, b in bloco(s))}/{n} ({f(po * 100, 0)}%) | {f(k)} | {f(kw)} | '
               f'{c1["S"]}/{c1["P"]}/{c1["N"]} | {c2["S"]}/{c2["P"]}/{c2["N"]}/{c2["?"]} | {acima} | {abaixo} |')

pn = [(cod(R1n[i][f'qa{k}_r1']), cod(R2[i][f'QA{k}'])) for i in ids for k in QA if cod(R2[i][f'QA{k}']) in CAT]
p7 = [(cod(R1n[i]['qa7_r1']), cod(R2[i]['QA7'])) for i in ids if cod(R2[i]['QA7']) in CAT]
out += ['', f'*Depois da regra do QA7 do A20 (só como referência, não é a concordância reportada):* geral '
        f'{f(sum(a == b for a, b in pn) / len(pn) * 100, 1)}%, κ = {f(kappa(pn))}; QA7 '
        f'{sum(a == b for a, b in p7)}/{len(p7)}, κ = {f(kappa(p7))}.']

# totais
t1 = {i: sum(NUM[R1[i][f'qa{k}_r1']] for k in QA) for i in ids}
t2 = {i: sum(NUM.get(cod(R2[i][f'QA{k}']), 0.5) for k in QA) for i in ids}  # "?" = P
dif = [t2[i] - t1[i] for i in ids]


def rank(v):
    o = sorted(range(len(v)), key=lambda j: v[j])
    r = [0.0] * len(v)
    j = 0
    while j < len(o):
        m = j
        while m + 1 < len(o) and v[o[m + 1]] == v[o[j]]:
            m += 1
        for t in range(j, m + 1):
            r[o[t]] = (j + m) / 2 + 1
        j = m + 1
    return r


def pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return num / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** 0.5


x1, x2 = [t1[i] for i in ids], [t2[i] for i in ids]
out += ['', '## Pontuação total (0–9; "?" = 0,5)', '',
        '| medida | R1 | R2 |', '|---|---|---|',
        f'| média | {f(st.mean(x1))} | {f(st.mean(x2))} |',
        f'| mediana | {f(st.median(x1), 1)} | {f(st.median(x2), 1)} |',
        f'| ≥ 5 pontos | {sum(v >= 5 for v in x1)} | {sum(v >= 5 for v in x2)} |', '',
        f'Diferença R2 − R1: média {f(st.mean(dif))}, dp {f(st.stdev(dif))}, '
        f'limites de concordância (Bland-Altman) {f(st.mean(dif) - 1.96 * st.stdev(dif))} a '
        f'{f(st.mean(dif) + 1.96 * st.stdev(dif))}; |diferença| ≤ 1 em {sum(abs(d) <= 1 for d in dif)}/{len(ids)}; '
        f'Spearman ρ = {f(pearson(rank(x1), rank(x2)))}.', '',
        '| estudo | origem | R1 | R2 | R2 − R1 | critérios divergentes |', '|---|---|---|---|---|---|']
for i in sorted(ids, key=lambda i: t2[i] - t1[i]):
    div = [f'QA{k} ({R1[i][f"qa{k}_r1"]}→{cod(R2[i][f"QA{k}"])})' for k in QA
           if R1[i][f'qa{k}_r1'] != cod(R2[i][f'QA{k}'])]
    out.append(f'| {i} | {chave[i]["origem_qualidade"]} | {f(t1[i], 1)} | {f(t2[i], 1)} | '
               f'{f(t2[i] - t1[i], 1)} | {", ".join(div)} |')

# mudança do R2 entre rodadas
mud = [x for x in s16 if x['r2_anterior'] and x['r2_anterior'] != x['r2']]
ap = sum(1 for x in mud if x['r2'] == x['r1'])
af = sum(1 for x in mud if x['r2_anterior'] == x['r1'])
out += ['', '## R2: rodada anterior × atual (16 estudos)', '',
        f'O R2 mudou {len(mud)} de {len(s16)} decisões. Em {ap} passou a concordar com o R1; em {af} deixou de concordar.', '',
        '| critério | mudanças | rumo ao R1 | afastou do R1 |', '|---|---|---|---|']
for q in QA:
    m = [x for x in mud if x['qa'] == f'QA{q}']
    out.append(f'| QA{q} | {len(m)} | {sum(x["r2"] == x["r1"] for x in m)} | {sum(x["r2_anterior"] == x["r1"] for x in m)} |')

out += ['', '## Decisões "?" do R2', '', '| estudo | critério | R1 | onde (R2) |', '|---|---|---|---|']
out += [f'| {x["id"]} | {x["qa"]} | {x["r1"]} | {x["r2_onde"]} |' for x in linhas if x['r2'] == '?']

(D / 'concordancia_qualidade_R2v2.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))
