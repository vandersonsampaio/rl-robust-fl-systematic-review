"""Análise de sensibilidade da QP2 e da qualidade (resposta ao parecer: baixa concordância R1 × R2).

Recalcula as contagens centrais do paper sob classificações alternativas dos casos ambíguos
e sob as codificações originais do revisor 2 (antes do consenso), e verifica se as conclusões mudam.

Fontes: triagem_v2/extracao_principal.csv, triagem_v2/qualidade.csv,
        validacao/reclassificacao_R2/planilha_cega_R2_QP2.xlsx (QP2 do R2, livro v2, antes do consenso A21)
        e planilha_cega_R2_Qualidade.xlsx (qualidade do R2, livro v2, antes do consenso A20).
Os resultados das 15 comparações mais próximas (empate / vitória estreita / vitória clara)
vêm da Tab-QP2 do paper (paper_latex/tables/Tab-QP2.tex), que é a classificação do R1.
Saída: validacao/sensibilidade_qp2_qa.md
"""
import csv
import re
import statistics as st
from pathlib import Path

R = Path(__file__).resolve().parent.parent
B = R / 'triagem_v2'
rows = lambda p: list(csv.DictReader(open(p, encoding='utf-8-sig')))

E = {r['id']: r for r in rows(B / 'extracao_principal.csv')}
Q = {r['id']: r for r in rows(B / 'qualidade.csv')}
# R2: reclassificação cega com o livro de códigos v2 (antes do consenso A21); só estudos ainda incluídos (A22)
from openpyxl import load_workbook
_ws = load_workbook(R / 'validacao' / 'reclassificacao_R2' / 'planilha_cega_R2_QP2.xlsx')['QP2']
_cab = [c.value for c in _ws[1]]
R2 = {x[0]: dict(zip(_cab, x)) for x in _ws.iter_rows(min_row=2, values_only=True) if x[0] in E}
# qualidade do R2: reclassificação cega com o livro v2; "?" ou vazio fica com o código do R1
_wq = load_workbook(R / 'validacao' / 'reclassificacao_R2' / 'planilha_cega_R2_Qualidade.xlsx')['Qualidade']
_cq = [c.value for c in _wq[1]]
R2Q = {}
for _x in _wq.iter_rows(min_row=2, values_only=True):
    if _x[0] not in Q:
        continue
    _d = dict(zip(_cq, _x))
    R2Q[_x[0]] = {f'QA{i}': (str(_d[f'QA{i}'] or '').strip()[:1].upper() if str(_d[f'QA{i}'] or '').strip()[:1].upper() in 'SPN' and str(_d[f'QA{i}'] or '').strip()
                             else Q[_x[0]][f'qa{i}_r1']) for i in range(1, 10)}


def cmpcat(s):  # mesma regra do sintese.py
    s = s.lower()
    if s.startswith('nenhuma'): return 'nenhuma'
    if 'mesmo sinal' in s or 'míope' in s: return 'mesmo'
    if 'oráculo' in s: return 'oraculo'
    if s.startswith('fixa') or re.search(r'\+ ?fixa', s): return 'fixa'
    if 'outro sinal' in s: return 'outro'
    if 'aleatór' in s and not s.startswith('p'): return 'aleatoria'
    return 'parcial'


# "ação fixa (não defender)" do livro do R2 conta como nenhuma (A20); "?" fica com a categoria do R1
R2MAP = {'mesmo sinal': 'mesmo', 'oráculo': 'oraculo', 'ação fixa': 'fixa', 'ação fixa (não defender)': 'nenhuma',
         'outro sinal': 'outro', 'aleatória': 'aleatoria', 'ablação parcial': 'parcial', 'nenhuma': 'nenhuma'}
R2RES = {'empate': 'empate', 'vitória estreita': 'estreita', 'vitória clara': 'clara'}

# resultado das comparações mais próximas, classificação do R1 (Tab-QP2)
RES = {'V2-1102': 'estreita', 'V2-2103': 'empate', 'SB-03': 'estreita', 'V2-0973': 'estreita',
       'V2-3331': 'estreita', 'V2-4540': 'empate', 'V2-0351': 'estreita',
       'V2-1179': 'empate', 'V2-1327': 'empate', 'V2-4789': 'empate',
       'V2-3243': 'clara', 'V2-4812': 'clara', 'V2-2573': 'clara', 'V2-0160': 'clara',
       'V2-0350': 'empate', 'V2-1130': 'clara'}  # A20: o grupo "não defender" deixou de existir; A22: V2-1120 excluído por IC4
# nenhum estudo aplica teste estatístico à própria comparação com a heurística (R1)
TESTE_NA_COMPARACAO = set()

base = {k: cmpcat(v['comparacao_nao_aprendida']) for k, v in E.items()}


def contagens(cat, res=RES, teste=TESTE_NA_COMPARACAO):
    n = lambda c: sum(1 for v in cat.values() if v == c)
    com = sum(1 for v in cat.values() if v != 'nenhuma')
    forte = n('fixa') + n('mesmo') + n('outro') + n('oraculo')  # como no funil: fixa, heurística ou oráculo
    mesmo = [k for k, v in cat.items() if v == 'mesmo']
    sem2 = [k for k in mesmo if Q[k]['qa2_r1'] == 'S']
    proximas = [k for k, v in cat.items() if v in ('mesmo', 'fixa')]
    emp = sum(1 for k in proximas if res.get(k) == 'empate')
    sem_res = sum(1 for k in proximas if k not in res)
    return {'sem comparação': n('nenhuma'), 'com comparação': com, 'referência forte': forte,
            'mesmo sinal': len(mesmo), 'mesmo sinal com ≥3 sementes e variab.': len(sem2),
            'teste na comparação': len([k for k in mesmo if k in teste]),
            'comparações mais próximas': len(proximas), 'empates': emp,
            'sem resultado classificado': sem_res}


def cenario(**mud):
    c = dict(base)
    c.update(mud)
    return c


C = {}
C['S0. Classificação final do R1 (paper)'] = (base, RES)
# 1. casos-limite de categoria, um a um
C['F1. V2-1102 e V2-0973: limiar estático 0,5 tratado como ação fixa'] = (cenario(**{'V2-1102': 'fixa', 'V2-0973': 'fixa'}), RES)
C['F2. V2-3243: trimmed mean sobre os mesmos sinais tratado como heurística do mesmo sinal'] = (cenario(**{'V2-3243': 'mesmo'}), RES)
C['F3. V2-4059 e V2-0835: heurísticas tratadas como do mesmo sinal'] = (cenario(**{'V2-4059': 'mesmo', 'V2-0835': 'mesmo'}), RES)
C['F4. Pow-d (V2-0542, 1140, 1199, 3215) não conta como heurística (fica a aleatória)'] = (
    cenario(**{k: 'aleatoria' for k in ('V2-0542', 'V2-1140', 'V2-1199', 'V2-3215')}), RES)
C['F5. Definição ampla: agregadores externos contam como política não aprendida (grupo C do A14)'] = (
    cenario(**{k: 'fixa' for k in ('V2-1042', 'V2-1185', 'V2-0918', 'V2-1231', 'V2-3175', 'V2-1001', 'V2-0530', 'V2-3494')}), RES)
C['F6. Comparações rejeitadas na reconciliação aceitas (V2-0922, V2-1229)'] = (
    cenario(**{'V2-0922': 'aleatoria', 'V2-1229': 'aleatoria'}), RES)
# 2. casos-limite de resultado
res_o1 = dict(RES, **{k: 'empate' for k, v in RES.items() if v == 'estreita'})
C['O1. Vitórias estreitas (≤ ~6 p.p., sem variabilidade) tratadas como empate'] = (base, res_o1)
res_o2 = dict(RES, **{'V2-1327': 'estreita', 'V2-2103': 'estreita', 'V2-4540': 'estreita'})
C['O2. Empates em que alguma métrica favorece o agente tratados como vitória'] = (base, res_o2)
# 3. revisor 2 antes do consenso
_c2 = lambda v: (v['categoria da referência mais forte'] or '').strip()
r2cat = dict(base, **{k: R2MAP[_c2(v)] for k, v in R2.items() if _c2(v) in R2MAP})
r2res = {k: R2RES[v['resultado']] for k, v in R2.items() if v['resultado'] in R2RES}
r2teste = {k for k, v in R2.items() if str(v['teste estatístico na própria comparação (S/N)'] or '').strip().upper().startswith('S')}
C['R2. Categorias e resultados do R2 (livro v2) antes do consenso'] = (r2cat, r2res)
# 4. extremos
melhor = cenario(**{'V2-3243': 'mesmo', 'V2-4059': 'mesmo', 'V2-0835': 'mesmo'})
C['X1. Mais favorável ao aprendizado (F2 + F3 + O2)'] = (melhor, res_o2)
pior = cenario(**{'V2-1102': 'fixa', 'V2-0973': 'fixa'})
C['X2. Menos favorável ao aprendizado (F1 + O1)'] = (pior, res_o1)

out = ['# Análise de sensibilidade: QP2 e qualidade', '',
       'Gerado por `scripts/sensibilidade.py`. Cada cenário altera só os itens indicados; o resto segue a classificação final do R1.', '',
       '## QP2: contagens centrais por cenário', '']
cols = list(contagens(base).keys())
out.append('| cenário | ' + ' | '.join(cols) + ' |')
out.append('|---|' + '---|' * len(cols))
res_all = {}
for nome, (cat, res) in C.items():
    t = r2teste if nome.startswith('R2') else TESTE_NA_COMPARACAO
    k = contagens(cat, res, t)
    res_all[nome] = k
    out.append(f'| {nome} | ' + ' | '.join(str(k[c]) for c in cols) + ' |')

# conclusões
def concl(k):
    return {'A. a maioria não compara com heurística do mesmo sinal': k['mesmo sinal'] < len(E) / 2,
            'B. menos de 1/4 dos estudos usa heurística do mesmo sinal': k['mesmo sinal'] < len(E) / 4,
            'C. nenhuma comparação com o mesmo sinal tem teste estatístico': k['teste na comparação'] == 0,
            'D. há empates entre as comparações mais próximas': k['empates'] > 0,
            'E. menos de 10% dos estudos comparam com o mesmo sinal usando ≥3 sementes e variabilidade': k['mesmo sinal com ≥3 sementes e variab.'] < len(E) / 10}

out += ['', '## QP2: as conclusões se mantêm?', '']
cn = list(concl(res_all['S0. Classificação final do R1 (paper)']).keys())
out.append('| cenário | ' + ' | '.join(c.split('.')[0] for c in cn) + ' |')
out.append('|---|' + '---|' * len(cn))
for nome, k in res_all.items():
    out.append(f'| {nome} | ' + ' | '.join('sim' if v else '**não**' for v in concl(k).values()) + ' |')
out += [''] + [f'- **{c}**' for c in cn]

# qualidade
v = {'S': 1, 'P': 0.5, 'N': 0}
def tot(r, pre): return sum(v[r[f'{pre}{i}'].strip()[:1].upper()] for i in range(1, 10))
base_t = {k: tot(r, 'qa') if False else sum(v[r[f'qa{i}_r1']] for i in range(1, 10)) for k, r in Q.items()}
r2_t = dict(base_t)
for k, r in R2Q.items():
    r2_t[k] = sum(v[r[f'QA{i}'].strip()[:1].upper()] for i in range(1, 10))
def qa_count(i, val, src):
    return sum(1 for k, r in Q.items()
               if (R2Q[k][f'QA{i}'].strip()[:1].upper() if (src == 'r2' and k in R2Q) else r[f'qa{i}_r1']) == val)
conv = {k: sum(v[r[f'qa{i}_r1']] if not (i in (2, 3, 7, 9) and r[f'qa{i}_r1'] == 'N') else 0.5 for i in range(1, 10))
        for k, r in Q.items()}
out += ['', '## Qualidade', '',
        '| cenário | média | mediana | ≥ 5 pontos | QA2 = S (≥3 sementes) | QA3 = S (teste) | QA1 = N (usa teste) |',
        '|---|---|---|---|---|---|---|']
def linha(nome, t, src):
    out.append(f'| {nome} | {st.mean(t.values()):.2f} | {st.median(t.values()):.1f} | {sum(x >= 5 for x in t.values())} | '
               f'{qa_count(2, "S", src)} | {qa_count(3, "S", src)} | {qa_count(1, "N", src)} |')
linha('Q0. Pontuação final do R1 (paper)', base_t, 'r1')
linha(f'Q1. Pontuação do R2 (livro v2) nos {len(R2Q)} estudos da amostra, antes do consenso', r2_t, 'r2')
linha('Q2. Convenção generosa: "não documentado" vale 0,5 em QA2, QA3, QA7 e QA9', conv, 'r1')
out += ['', 'Q2 é um limite superior: trata como parcialmente atendido tudo o que o artigo não documenta.']

(R / 'validacao' / 'sensibilidade_qp2_qa.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))
