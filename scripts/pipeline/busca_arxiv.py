"""Executa uma string de busca na API do arXiv e salva todos os resultados (Atom) + CSV.

Uso: python busca_arxiv.py <rotulo> "<search_query na sintaxe da API>"
Respeita o limite da API (3 s entre requisições). Resultados em validacao/arxiv_<rotulo>.csv.
"""
import csv, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

NS = {'a': 'http://www.w3.org/2005/Atom', 'os': 'http://a9.com/-/spec/opensearch/1.1/'}
OUT = Path(__file__).resolve().parent.parent / 'validacao'


def fetch(q, start, n=500):
    url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode(
        {'search_query': q, 'start': start, 'max_results': n, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
    for tent in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return ET.fromstring(r.read())
        except Exception as e:  # noqa: BLE001 - reintenta erros transitórios da API
            print('erro', e, '— nova tentativa'); time.sleep(10)
    raise SystemExit('API do arXiv indisponível')


def main(label, q):
    OUT.mkdir(exist_ok=True)
    rows, start, total = [], 0, None
    while total is None or start < total:
        root = fetch(q, start)
        total = int(root.find('os:totalResults', NS).text)
        es = root.findall('a:entry', NS)
        if not es:
            break
        for e in es:
            rows.append({'arxiv_id': e.find('a:id', NS).text.split('/abs/')[-1],
                         'titulo': ' '.join(e.find('a:title', NS).text.split()),
                         'publicado': e.find('a:published', NS).text[:10],
                         'categorias': ' '.join(c.get('term') for c in e.findall('a:category', NS)),
                         'resumo': ' '.join(e.find('a:summary', NS).text.split())})
        start += len(es)
        time.sleep(3)
    with open(OUT / f'arxiv_{label}.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['arxiv_id', 'titulo', 'publicado', 'categorias', 'resumo'])
        w.writeheader(); w.writerows(rows)
    print(f'{label}: totalResults={total}, baixados={len(rows)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
