"""Gera o pacote da reclassificação cega do revisor 2 (adendo A19).

- QP2: os 52 estudos com alguma comparação não aprendida (classificação final do R1).
- Qualidade: 26 estudos = os 16 da amostra anterior + 10 novos, estratificados pela categoria da QP2
  (alvo de cerca de 1/3 por categoria), sorteados com semente fixa.
Saídas em validacao/reclassificacao_R2/:
  planilha_cega_R2.xlsx (para o R2), pdfs/ (textos completos), livro_codigos_v2.md (cópia),
  chave_amostra_R1.csv (fica com o R1: estudos, categoria do R1 e estrato).
"""
import csv
import random
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from pypdf import PdfReader, PdfWriter

R = Path(__file__).resolve().parent.parent
B = R / 'triagem_v2'
OUT = R / 'validacao' / 'reclassificacao_R2'
SEMENTE = 20261017
rows = lambda p: list(csv.DictReader(open(p, encoding='utf-8-sig')))

E = {r['id']: r for r in rows(B / 'extracao_principal.csv')}
IDX = {r['id']: r for r in rows(R / 'selecionados' / 'indice.csv')}
ANT = [r['id'] for r in rows(B / 'revisor2' / 'Qualidade.csv')]


def cmpcat(s):  # mesma regra do sintese.py
    s = s.lower()
    if s.startswith('nenhuma'): return 'nenhuma'
    if 'mesmo sinal' in s or 'míope' in s: return 'mesmo sinal'
    if 'oráculo' in s: return 'oráculo'
    if s.startswith('fixa') or re.search(r'\+ ?fixa', s): return 'fixa'
    if 'outro sinal' in s: return 'outro sinal'
    if 'aleatór' in s and not s.startswith('p'): return 'aleatória'
    return 'parcial'


cat = {k: cmpcat(v['comparacao_nao_aprendida']) for k, v in E.items()}
qp2 = sorted(k for k, c in cat.items() if c != 'nenhuma')
assert len(qp2) == 52

# amostra da qualidade
tot = Counter(cat.values())
alvo = {c: round(n / 3) for c, n in tot.items()}
falta = 26 - sum(alvo.values())
for c, _ in tot.most_common(abs(falta)):
    alvo[c] += 1 if falta > 0 else -1
ja = Counter(cat[k] for k in ANT)
rng = random.Random(SEMENTE)
novos = []
for c in sorted(tot):
    pool = sorted(k for k in E if cat[k] == c and k not in ANT)
    n = max(0, alvo[c] - ja[c])
    novos += rng.sample(pool, min(n, len(pool)))
while len(ANT) + len(novos) < 26:  # completa, se algum estrato já estava acima do alvo
    pool = sorted(k for k in E if k not in ANT and k not in novos)
    novos.append(rng.choice(pool))
qa = sorted(ANT + novos)
assert len(qa) == 26 and len(set(qa)) == 26

# PDFs
pdfdir = OUT / 'pdfs'
pdfdir.mkdir(parents=True, exist_ok=True)
precisa = sorted(set(qp2) | set(qa))
for k in precisa:
    src = R / 'selecionados' / 'artigos_S1' / IDX[k]['arquivo']
    dst = pdfdir / f'{k}.pdf'
    if k == 'V2-3494':  # livro de anais inteiro: extrai o capítulo 37 (pp. 375-383)
        rd = PdfReader(str(src))
        pags = [i for i, p in enumerate(rd.pages)
                if 'Malicious Node Detection and Robust Federated Aggregation' in (p.extract_text() or '')]
        w = PdfWriter()
        for i in range(min(pags), max(pags) + 1):
            w.add_page(rd.pages[i])
        with open(dst, 'wb') as f:
            w.write(f)
    else:
        shutil.copyfile(src, dst)

# planilha
wb = Workbook()
cab = Font(bold=True)
quebra = Alignment(wrap_text=True, vertical='top')
cinza = PatternFill('solid', fgColor='EEEEEE')

ins = wb.active
ins.title = 'Instruções'
for linha in [
    'Reclassificação cega da QP2 e da qualidade (revisor 2)',
    '',
    '1. Leia o livro de códigos (livro_codigos_v2.md) antes de começar.',
    '2. Use o texto completo de cada estudo, na pasta pdfs/ (arquivo <id>.pdf).',
    '3. Decida pelos números das tabelas e figuras, e não pela conclusão dos autores do artigo.',
    '4. Em cada decisão, preencha a coluna "onde" com a seção, a tabela ou a figura.',
    '5. Não consulte a extração do revisor 1 nem decisões anteriores.',
    '6. Use "?" só quando o texto permitir mais de uma leitura, e explique nas notas.',
    '7. Ao terminar, envie a planilha sem alterações posteriores.',
]:
    ins.append([linha])
ins['A1'].font = Font(bold=True, size=12)
ins.column_dimensions['A'].width = 110

q = wb.create_sheet('QP2')
colq = ['id', 'título', 'arquivo', 'categoria da referência mais forte', 'outras referências não aprendidas',
        'descrição da referência mais forte', 'onde (comparação)', 'métrica principal', 'resultado',
        'valores (agente × referência)', 'variabilidade da própria comparação (S/N)',
        'teste estatístico na própria comparação (S/N)', 'discutido como achado (S/P/N)', 'onde (resultado)', 'notas']
q.append(colq)
for k in qp2:
    q.append([k, E[k]['titulo'], f'{k}.pdf'] + [''] * (len(colq) - 3))
dv_cat = DataValidation(type='list', formula1='"mesmo sinal,oráculo,ação fixa,ação fixa (não defender),outro sinal,aleatória,ablação parcial,nenhuma,?"', allow_blank=True)
dv_res = DataValidation(type='list', formula1='"empate,vitória estreita,vitória clara,derrota,métricas divergentes,?"', allow_blank=True)
dv_sn = DataValidation(type='list', formula1='"S,N,?"', allow_blank=True)
dv_spn = DataValidation(type='list', formula1='"S,P,N,?"', allow_blank=True)
for dv in (dv_cat, dv_res, dv_sn, dv_spn):
    q.add_data_validation(dv)
n = len(qp2) + 1
dv_cat.add(f'D2:D{n}'); dv_res.add(f'I2:I{n}'); dv_sn.add(f'K2:L{n}'); dv_spn.add(f'M2:M{n}')

ql = wb.create_sheet('Qualidade')
colqa = ['id', 'título', 'arquivo']
for i in range(1, 10):
    colqa += [f'QA{i}', f'QA{i} onde']
colqa.append('notas')
ql.append(colqa)
for k in qa:
    ql.append([k, E[k]['titulo'], f'{k}.pdf'] + [''] * (len(colqa) - 3))
dv_qa = DataValidation(type='list', formula1='"S,P,N,?"', allow_blank=True)
ql.add_data_validation(dv_qa)
for i in range(9):
    col = 4 + 2 * i
    letra = ql.cell(row=1, column=col).column_letter
    dv_qa.add(f'{letra}2:{letra}{len(qa) + 1}')

for ws in (q, ql):
    for c in ws[1]:
        c.font = cab
        c.fill = cinza
        c.alignment = quebra
    ws.freeze_panes = 'D2'
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 45
    ws.column_dimensions['C'].width = 13
    for col in ws.iter_cols(min_col=4, max_col=ws.max_column):
        ws.column_dimensions[col[0].column_letter].width = 16
wb.save(OUT / 'planilha_cega_R2.xlsx')

shutil.copyfile(R / 'validacao' / 'livro_codigos_v2.md', OUT / 'livro_codigos_v2.md')

estrato = {k: ('amostra anterior' if k in ANT else 'nova') for k in qa}
with open(R / 'validacao' / 'chave_amostra_R2_v2.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'na_QP2', 'na_qualidade', 'categoria_R1', 'origem_qualidade'])
    for k in sorted(set(qp2) | set(qa)):
        w.writerow([k, k in qp2, k in qa, cat[k], estrato.get(k, '')])

print('QP2:', len(qp2), '| qualidade:', len(qa), '(anteriores', len(ANT), '+ novos', len(novos), ')')
print('alvo por categoria:', dict(alvo), '| amostra:', dict(Counter(cat[k] for k in qa)))
print('PDFs:', len(list(pdfdir.glob('*.pdf'))))
