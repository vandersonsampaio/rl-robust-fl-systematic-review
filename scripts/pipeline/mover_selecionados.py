"""Move os PDFs dos estudos incluídos (S1 e QP7) e os .tex gerados para selecionados/.

selecionados/artigos_S1/     78 estudos primários
selecionados/artigos_QP7/    32 estudos da QP7 (busca + snowballing) e canonicas/ (5 leituras do §13)
selecionados/paper_slr/      manuscrito (antes em paper_slr/)
selecionados/tese_cap_slr/   capítulo da tese (antes em tese_cap_slr/)
selecionados/indice.csv      id, grupo, título, arquivo e pasta de origem

Já executado em 2026-09-28 (é de uso único). Os nomes dos arquivos não mudam. O pipeline usa só triagem_v2/txt/, então mover os PDFs não o afeta.
"""
import csv
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
T = RAIZ / 'triagem_v2'
S = RAIZ / 'selecionados'


def rd(n):
    return list(csv.DictReader(open(T / n, encoding='utf-8-sig')))


titulo = {m['id']: m['titulo'] for m in rd('mapa_pdfs.csv')}
titulo.update({e['id']: e['titulo'] for e in rd('extracao_principal.csv')})
s1 = [e['id'] for e in rd('extracao_principal.csv')]
q7 = [x['id'] for x in rd('etapa2_arxiv.csv') + rd('etapa2_lote2.csv') if x['fluxo'] == 'QP7' and x['etapa2_decisao'] == 'Q7-I']

pdf = {}
for m in rd('mapa_pdfs.csv'):
    p = T / m['pasta'] / (m['arquivo'] + '.pdf')
    if p.exists():
        pdf[m['id']] = p
for x in rd('etapa2_arxiv.csv'):
    for p in (T / 'arXiv').glob(x['arxiv'] + '*.pdf'):
        pdf[x['id']] = p
# nomes que mapa_pdfs.csv registra de forma diferente do arquivo em disco
pdf['V2-3494'] = T / 'scopus' / '978-981-96-2409-6.pdf'  # livro de anais inteiro; o estudo é o cap. 37
pdf['V2-2188'] = next((T / 'scopus').glob('IET Communications - 2026 - Atebawone*.pdf'))

planos = [(i, 'S1', S / 'artigos_S1') for i in s1] + [(i, 'QP7', S / 'artigos_QP7') for i in q7]
faltam = [i for i, _, _ in planos if i not in pdf or not pdf[i].exists()]
if faltam:
    raise SystemExit(f'PDFs não encontrados: {faltam}')

indice = []
for i, grupo, destino in planos:
    destino.mkdir(parents=True, exist_ok=True)
    origem = pdf[i]
    indice.append({'id': i, 'grupo': grupo, 'titulo': titulo.get(i, ''), 'arquivo': origem.name,
                   'origem': str(origem.parent.relative_to(RAIZ))})
    shutil.move(str(origem), str(destino / origem.name))

can = S / 'artigos_QP7' / 'canonicas'
can.mkdir(parents=True, exist_ok=True)
for p in sorted((T / 'canonical').glob('*.pdf')):
    indice.append({'id': 'canonica', 'grupo': 'QP7-§13', 'titulo': '', 'arquivo': p.name,
                   'origem': str(p.parent.relative_to(RAIZ))})
    shutil.move(str(p), str(can / p.name))

for pasta in ('paper_slr', 'tese_cap_slr'):
    shutil.move(str(RAIZ / pasta), str(S / pasta))

with open(S / 'indice.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['id', 'grupo', 'titulo', 'arquivo', 'origem'])
    w.writeheader()
    w.writerows(indice)
print(f'{len(indice)} PDFs movidos; .tex em selecionados/paper_slr e selecionados/tese_cap_slr')
