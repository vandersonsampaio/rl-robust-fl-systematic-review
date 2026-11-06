"""Concordância entre revisor 1 e revisor 2 na amostra cega da etapa 1 (protocolo §8.7).

Entrada: triagem_v2/revisor2/triagem_cega_revisor2.xlsx (preenchida), chave_amostra.csv e triagem_final.csv.
Binário do protocolo: I e D = "segue"; E-* = "exclui".
Saída: triagem_v2/revisor2/comparacao_kappa.csv (uma linha por registro) e resumo no terminal.
"""
import csv
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parent.parent
D = RAIZ / 'triagem_v2' / 'revisor2'

r1 = {r['id']: r for r in csv.DictReader(open(RAIZ / 'triagem_v2' / 'triagem_final.csv', encoding='utf-8-sig'))}
chave = [r for r in csv.DictReader(open(D / 'chave_amostra.csv', encoding='utf-8-sig')) if r['conjunto'] == 'kappa']
ws = load_workbook(D / 'triagem_cega_revisor2.xlsx')['Amostra_kappa']
r2 = {row[1]: row for row in ws.iter_rows(min_row=2, values_only=True) if row[1]}


def binario(d):
    return 'segue' if d in ('I', 'D') else 'exclui'


# integridade: mesmos ids, mesma ordem, todos decididos
ordem_ok = [k['id'] for k in chave] == [row[1] for row in ws.iter_rows(min_row=2, values_only=True) if row[1]]
faltando = [k['id'] for k in chave if not (r2.get(k['id']) or [None] * 9)[8]]

linhas = []
for k in chave:
    i = k['id']
    if i in faltando:  # sem decisão do revisor 2 (pendente): fora do κ até ser decidido
        continue
    d1, d2 = r1[i]['s1_decisao'], r2[i][8]
    linhas.append({'id': i, 'ano': r1[i]['ano'], 'titulo': r1[i]['titulo'], 'r1': d1, 'r2': d2,
                   'r1_bin': binario(d1), 'r2_bin': binario(d2), 'concorda_bin': binario(d1) == binario(d2),
                   'concorda_codigo': d1 == d2, 'r1_metodo': r1[i]['s1_metodo'], 'r1_motivo': r1[i]['s1_motivo'],
                   'r2_motivo': r2[i][9] or '', 'r2_obs': r2[i][10] or '',
                   'etapa2_r1': r1[i].get('etapa2_decisao', '')})

n = len(linhas)
tab = Counter((x['r1_bin'], x['r2_bin']) for x in linhas)
a, b = tab[('segue', 'segue')], tab[('segue', 'exclui')]
c, d = tab[('exclui', 'segue')], tab[('exclui', 'exclui')]
po = (a + d) / n
pe = ((a + b) * (a + c) + (c + d) * (b + d)) / n ** 2
kappa = (po - pe) / (1 - pe)
pabak = 2 * po - 1
# acordo específico por classe (Cicchetti & Feinstein)
ppos = 2 * a / (2 * a + b + c) if (2 * a + b + c) else float('nan')
pneg = 2 * d / (2 * d + b + c)

with open(D / 'comparacao_kappa.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0]))
    w.writeheader()
    w.writerows(linhas)

print(f'integridade: ordem igual à chave = {ordem_ok}; sem decisão = {len(faltando)}')
print(f'n = {n}; tabela (R1 linhas × R2 colunas): segue/segue {a}, segue/exclui {b}, exclui/segue {c}, exclui/exclui {d}')
print(f'concordância = {po:.4f}; κ = {kappa:.3f}; PABAK = {pabak:.3f}; acordo positivo = {ppos:.3f}; negativo = {pneg:.3f}')
print(f'mesmo código exato: {sum(x["concorda_codigo"] for x in linhas)}/{n}')
