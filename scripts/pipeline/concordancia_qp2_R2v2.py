"""Concordância R1 × R2 na QP2, reclassificação cega com livro de códigos v2 (adendo A19).

Entrada: validacao/reclassificacao_R2/planilha_cega_R2_QP2.xlsx (aba QP2, 52 estudos),
         validacao/chave_amostra_R2_v2.csv, reclassificacao_R2/extracao_principal_R1_antes_A20.csv (R1 antes do
         consenso; a concordância reportada é contra ela), triagem_v2/extracao_principal.csv (R1 depois do A20, só
         para comparação) e a aba Qualidade do R2 (coerência entre o QA5 e a categoria que o próprio R2 deu).
O livro do R2 tem o subtipo "não defender" dentro de ação fixa: no κ ele conta como "fixa".
"?" do R2 fica fora do κ. O resultado do R1 vem de RES em scripts/sensibilidade.py (comparações mais próximas).
Saída: validacao/reclassificacao_R2/concordancia_qp2_R2v2.csv (uma linha por estudo)
       e validacao/reclassificacao_R2/concordancia_qp2_R2v2.md.
"""
import csv
import re
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parent.parent
V = RAIZ / 'validacao'
D = V / 'reclassificacao_R2'
CAT = ['mesmo', 'oraculo', 'fixa', 'outro', 'aleatoria', 'parcial', 'nenhuma']
NOME = {'mesmo': 'mesmo sinal', 'oraculo': 'oráculo', 'fixa': 'ação fixa', 'outro': 'outro sinal',
        'aleatoria': 'aleatória', 'parcial': 'ablação parcial', 'nenhuma': 'nenhuma'}
FORTE = {'mesmo', 'oraculo', 'fixa', 'outro'}  # "referência forte", como no funil do paper
RES_R2 = {'empate': 'empate', 'vitória estreita': 'estreita', 'vitória clara': 'clara', 'derrota': 'derrota'}
# resultados do R1 já existentes antes do A20 (Tab-QP2); V2-0350 e V2-1130 foram lidos no A20 e ficam à parte
RES_R1 = {'V2-1102': 'empate', 'V2-2103': 'empate', 'SB-03': 'estreita', 'V2-0973': 'estreita',
          'V2-3331': 'estreita', 'V2-4540': 'clara', 'V2-0351': 'clara',
          'V2-1179': 'empate', 'V2-1327': 'empate', 'V2-4789': 'empate', 'V2-1120': 'estreita',
          'V2-3243': 'clara', 'V2-4812': 'clara', 'V2-2573': 'clara', 'V2-0160': 'clara'}
RES_R1_A20 = {'V2-0350': 'empate', 'V2-1130': 'clara'}


def rows(p):
    return list(csv.DictReader(open(p, encoding='utf-8-sig')))


def cmpcat(s):  # mesma regra do sintese.py
    s = s.lower()
    if s.startswith('nenhuma'): return 'nenhuma'
    if 'mesmo sinal' in s or 'míope' in s: return 'mesmo'
    if 'oráculo' in s: return 'oraculo'
    if s.startswith('fixa') or re.search(r'\+ ?fixa', s): return 'fixa'
    if 'outro sinal' in s: return 'outro'
    if 'aleatór' in s and not s.startswith('p'): return 'aleatoria'
    return 'parcial'


def cat_r2(s):
    s = (s or '').strip().lower()
    if s == '?': return '?'
    for chave, c in (('mesmo sinal', 'mesmo'), ('oráculo', 'oraculo'), ('ação fixa', 'fixa'), ('outro sinal', 'outro'),
                     ('aleatória', 'aleatoria'), ('ablação parcial', 'parcial'), ('nenhuma', 'nenhuma')):
        if s.startswith(chave): return c
    raise ValueError(s)


def cod(x):
    x = (x or '').strip()
    return x[:1].upper() if x else ''


def kappa(pares, cats):
    n = len(pares)
    if not n:
        return float('nan')
    po = sum(a == b for a, b in pares) / n
    m1, m2 = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(m1[c] * m2[c] for c in cats) / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')


def f(x, d=2):
    return '—' if x != x else f'{x:.{d}f}'.replace('.', ',')


def linha_k(rot, pares, cats):
    n = len(pares)
    ok = sum(a == b for a, b in pares)
    return f'| {rot} | {n} | {ok}/{n} ({f(ok / n * 100, 1)}%) | {f(kappa(pares, cats))} |'


chave = {r['id']: r for r in rows(V / 'chave_amostra_R2_v2.csv') if r['na_QP2'] == 'True'}
R1 = {r['id']: r for r in rows(D / 'extracao_principal_R1_antes_A20.csv')}
R1n = {r['id']: r for r in rows(RAIZ / 'triagem_v2' / 'extracao_principal.csv')}
ws = load_workbook(D / 'planilha_cega_R2_QP2.xlsx')['QP2']
cab = [c.value for c in ws[1]]
R2 = {row[0]: dict(zip(cab, row)) for row in ws.iter_rows(min_row=2, values_only=True) if row[0]}
wq = load_workbook(D / 'planilha_cega_R2_Qualidade.xlsx')['Qualidade']
cq = [c.value for c in wq[1]]
R2Q = {row[0]: dict(zip(cq, row)) for row in wq.iter_rows(min_row=2, values_only=True) if row[0]}

ids = sorted(chave)
assert set(ids) == set(R2), (set(ids) ^ set(R2))
C_CAT, C_RES = 'categoria da referência mais forte', 'resultado'
C_DISC, C_VAR, C_TES = 'discutido como achado (S/P/N)', 'variabilidade da própria comparação (S/N)', \
    'teste estatístico na própria comparação (S/N)'

L = []
for i in ids:
    r2 = R2[i]
    c2 = cat_r2(r2[C_CAT])
    res2 = (r2[C_RES] or '').strip().lower()
    L.append({'id': i, 'origem': chave[i]['origem_qualidade'] or 'só QP2',
              'r1': cmpcat(R1[i]['comparacao_nao_aprendida']), 'r1_A20': cmpcat(R1n.get(i, R1[i])['comparacao_nao_aprendida']),  # V2-1120 saiu (A22)
              'r2': c2, 'r2_nd': 'não defender' in (r2[C_CAT] or '').lower(),
              'r1_res': RES_R1.get(i, ''), 'r1_res_A20': RES_R1_A20.get(i, ''),
              'r2_res': RES_R2.get(res2, '?' if res2 == '?' else ''),
              'r1_disc': cod(R1[i]['discutido_como_achado']), 'r2_disc': cod(r2[C_DISC]),
              'r2_var': cod(r2[C_VAR]), 'r2_teste': cod(r2[C_TES]),
              'r2_metrica': (r2['métrica principal'] or '').strip(), 'r2_categoria_texto': r2[C_CAT] or ''})
for x in L:
    x['concorda'] = x['r1'] == x['r2']
with open(D / 'concordancia_qp2_R2v2.csv', 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(L[0]))
    w.writeheader()
    w.writerows(L)

val = [x for x in L if x['r2'] != '?']
pares = [(x['r1'], x['r2']) for x in val]
bin_ = lambda c: 'com' if c != 'nenhuma' else 'sem'
forte = lambda c: 'forte' if c in FORTE else 'fraca'
out = ['# Concordância R1 × R2 na QP2: reclassificação cega (livro de códigos v2)', '',
       'Gerado por `scripts/concordancia_qp2_R2v2.py`. R1 = extração antes do consenso (`extracao_principal_R1_antes_A20.csv`); '
       'R2 = `planilha_cega_R2_QP2.xlsx`, antes de qualquer consenso. O subtipo "não defender" do R2 conta como ação fixa, '
       'como no livro que ele recebeu. O "?" fica fora do κ.', '',
       f'**Integridade:** {len(ids)} estudos; categoria vazia = {sum(1 for x in L if not x["r2_categoria_texto"])}; '
       f'"?" na categoria = {sum(x["r2"] == "?" for x in L)}; "não defender" = {sum(x["r2_nd"] for x in L)}.', '',
       '## Categoria da referência mais forte', '',
       '| agregação | n | concordância | κ |', '|---|---|---|---|',
       linha_k('7 categorias', pares, CAT),
       linha_k('referência forte (mesmo sinal, oráculo, fixa, outro sinal) × fraca', [(forte(a), forte(b)) for a, b in pares], ['forte', 'fraca']),
       linha_k('com × sem comparação não aprendida', [(bin_(a), bin_(b)) for a, b in pares], ['com', 'sem'])]
for org in ('amostra anterior', 'nova', 'só QP2'):
    s = [(x['r1'], x['r2']) for x in val if x['origem'] == org]
    if s:
        out.append(linha_k(f'7 categorias, só "{org}"', s, CAT))
# rodada anterior do R2 (A16, sem livro de códigos), mesmos estudos
R2MAP = {'fixa': 'fixa', 'heurística (mesmo sinal)': 'mesmo', 'heurística (outro sinal)': 'outro',
         'parcial/ablação': 'parcial', 'aleatória': 'aleatoria', 'Nenhuma': 'nenhuma', 'oráculo': 'oraculo'}
R2a = {r['id']: r for r in rows(RAIZ / 'triagem_v2' / 'revisor2' / 'QP2.csv')}
pa = [(x['r1'], R2MAP[R2a[x['id']]['comparação']]) for x in L if x['id'] in R2a]
out.append(linha_k('*referência: rodada anterior (A16), mesmos estudos*', pa, CAT))
pn =[(x['r1_A20'], 'nenhuma' if x['r2_nd'] else x['r2']) for x in val]
out += ['', f'*Depois do consenso (A20–A22; só como referência, não é a concordância reportada): R1 atual × R2 com "não defender" = nenhuma:* '
        f'{sum(a == b for a, b in pn)}/{len(pn)}, κ = {f(kappa(pn, CAT))}.', '',
        '### Matriz (linhas R1, colunas R2)', '',
        '| R1 \\ R2 | ' + ' | '.join(NOME[c] for c in CAT) + ' | ? | total |', '|---' * (len(CAT) + 3) + '|']
for a in CAT:
    lin = [sum(1 for x in L if x['r1'] == a and x['r2'] == b) for b in CAT + ['?']]
    out.append(f'| {NOME[a]} | ' + ' | '.join(str(v) if v else '·' for v in lin) + f' | {sum(lin)} |')
tot = [sum(1 for x in L if x['r2'] == b) for b in CAT + ['?']]
out.append('| total | ' + ' | '.join(map(str, tot)) + f' | {len(L)} |')

out += ['', '### Divergências', '', '| estudo | origem | R1 | R2 (texto) |', '|---|---|---|---|']
out += [f'| {x["id"]} | {x["origem"]} | {NOME[x["r1"]]} | {x["r2_categoria_texto"]} |' for x in L if not x['concorda']]

# resultado: só onde o R1 tem resultado classificado e ambos usam a mesma categoria
rr = [x for x in L if x['r1_res'] and x['r2_res'] in RES_R2.values()]
mesma = [x for x in rr if x['concorda']]
out += ['', '## Resultado da comparação', '',
        f'O R1 só classificou o resultado das comparações mais próximas ({len(RES_R1)} estudos antes do A20). '
        f'Destes, {len(rr)} têm resultado do R2 e {len(mesma)} têm também a mesma categoria nos dois revisores.', '',
        '| conjunto | n | concordância | κ |', '|---|---|---|---|',
        linha_k('resultado, todos com resultado nos dois', [(x['r1_res'], x['r2_res']) for x in rr], ['empate', 'estreita', 'clara', 'derrota']),
        linha_k('resultado, mesma categoria', [(x['r1_res'], x['r2_res']) for x in mesma], ['empate', 'estreita', 'clara', 'derrota']),
        linha_k('empate × vitória, mesma categoria', [(x['r1_res'] == 'empate', x['r2_res'] == 'empate') for x in mesma], [True, False]),
        '', '| estudo | categoria R1 | categoria R2 | R1 | R2 | métrica principal (R2) |', '|---|---|---|---|---|---|']
for x in sorted([x for x in L if x['r1_res'] or x['r1_res_A20']], key=lambda x: x['r1_res'] == x['r2_res']):
    r1r = x['r1_res'] or f'{x["r1_res_A20"]} (A20)'
    out.append(f'| {x["id"]} | {NOME[x["r1"]]} | {x["r2_categoria_texto"]} | {r1r} | {x["r2_res"] or "—"} | {x["r2_metrica"][:70]} |')
cr = Counter(x['r2_res'] or '—' for x in L)
out += ['', f'Distribuição do resultado do R2 nos 52: ' + ', '.join(f'{k} {v}' for k, v in cr.most_common()) + '.']

# discutido
dd = [(x['r1_disc'], x['r2_disc']) for x in L if x['r1_disc'] in 'SPN' and x['r2_disc'] in ('S', 'P', 'N') and x['r1_disc']]
c1, c2 = Counter(a for a, _ in dd), Counter(b for _, b in dd)
out += ['', '## Discutido como achado', '', '| n | concordância | κ | R1 S/P/N | R2 S/P/N |', '|---|---|---|---|---|',
        f'| {len(dd)} | {sum(a == b for a, b in dd)}/{len(dd)} ({f(sum(a == b for a, b in dd) / len(dd) * 100, 1)}%) | '
        f'{f(kappa(dd, ["S", "P", "N"]))} | {c1["S"]}/{c1["P"]}/{c1["N"]} | {c2["S"]}/{c2["P"]}/{c2["N"]} |']

# variabilidade e teste: o R1 não tem esses campos por comparação
cv, ct = Counter(x['r2_var'] or '—' for x in L), Counter(x['r2_teste'] or '—' for x in L)
out += ['', '## Variabilidade e teste estatístico na própria comparação', '',
        'O R1 não registrou esses dois campos por comparação (só o de sementes do estudo e, no caso do mesmo sinal, o QA2). '
        f'R2, variabilidade: {", ".join(f"{k} {v}" for k, v in cv.most_common())}. '
        f'R2, teste: {", ".join(f"{k} {v}" for k, v in ct.most_common())} '
        f'({", ".join(x["id"] for x in L if x["r2_teste"] == "S")}).']

# coerência QA5 × categoria do próprio R2 (livro do R2: nenhuma→N; mesmo/oráculo/fixa→S; demais→P)
esp = lambda c: 'N' if c == 'nenhuma' else ('S' if c in ('mesmo', 'oraculo', 'fixa') else 'P')
coer = [(x['id'], x['r2'], esp(x['r2']) if x['r2'] != '?' else '?', cod(R2Q[x['id']]['QA5'])) for x in L if x['id'] in R2Q]
inc = [c for c in coer if c[2] != c[3]]
out += ['', '## Coerência interna do R2: QA5 × categoria da QP2', '',
        f'{len(coer) - len(inc)} de {len(coer)} estudos coerentes. Divergências:', '',
        '| estudo | categoria R2 | QA5 esperado | QA5 do R2 |', '|---|---|---|---|']
out += [f'| {a} | {NOME.get(b, b)} | {c} | {d} |' for a, b, c, d in inc]

(D / 'concordancia_qp2_R2v2.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))
