"""Associa cada PDF (acm/ieee/scopus) a um registro das listas de download, por DOI ou título normalizado."""
import csv, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from triagem_ieee import norm_title
B = Path(__file__).resolve().parent.parent / 'triagem_v2'
rows = []
for src in ('ieee', 'acm', 'scopus', 'arxiv'):
    for r in csv.DictReader(open(B / f'download_{src}.csv', encoding='utf-8-sig')):
        r['lista'] = src; rows.append(r)
MANUAL = {  # PDFs do snowballing (novos/) sem registro na base: id SB-xx
    'R2Fed_Resilient_Reinforcement_Federated_Learning_for_Industrial_Applications': ('V2-0945', 'R2Fed: Resilient Reinforcement Federated Learning for Industrial Applications'),
    's00607-022-01078-1': ('SB-01', 'Trust-driven reinforcement selection strategy for federated learning on IoT devices'),
    's10796-022-10307-z': ('SB-02', 'Trust-Augmented Deep Reinforcement Learning for Federated Learning Client Selection'),
    '1-s2.0-S0020025526011254-main': ('SB-03', 'FedCHO: Closed-Loop Hierarchical Orchestration for Blockchain-based Byzantine-Robust Federated Learning'),
    '2511.03529v2': ('SB-04', 'Byzantine-Robust Federated Learning with Learnable Aggregation Weights'),
    '3637528.3671545': ('SB-05', 'FedSecurity: A Benchmark for Attacks and Defenses in Federated Learning and Federated LLMs'),
    'A_comparative_study_of_defense_strategies_for_managing_malicious_participants_and_its_effects_in_Federated_Learning_systems': ('SB-06', 'A comparative study of defense strategies for managing malicious participants and its effects in Federated Learning systems'),
    '1-s2.0-S1566253522001439-main': ('SB-07', 'Survey on federated learning threats: Concepts, taxonomy on attacks and defences, experimental study and challenges'),
    '1-s2.0-S0957417426014715-main': ('SB-08', 'SoK: Understanding backdoor attacks & defenses in federated learning'),
    '3579856.3590328': ('SB-09', 'SoK: Systematizing Attack Studies in Federated Learning - From Sparseness to Completeness'),
}
res, usados = [], set()
for d in ('acm', 'ieee', 'scopus', 'novos'):
    for t in sorted((B / 'txt' / d).glob('*.txt')):
        txt = t.read_text(encoding='utf-8', errors='ignore')
        head = txt[:15000]
        nh = norm_title(head)
        hit = None
        for r in rows:
            doi = (r['doi'] or '').lower()
            if doi and doi in head.lower():
                hit = (r, 'doi'); break
        if not hit:
            for r in rows:
                nt = norm_title(r['titulo'])
                if len(nt) > 20 and nt in nh:
                    hit = (r, 'titulo'); break
        if not hit:  # título pelo começo (título quebrado/abreviado)
            for r in rows:
                nt = norm_title(r['titulo'])
                if len(nt) > 40 and nt[:40] in nh:
                    hit = (r, 'titulo40'); break
        if t.stem in MANUAL:
            hit = ({'id': MANUAL[t.stem][0], 'lista': 'snowball', 'titulo': MANUAL[t.stem][1]}, 'manual')
        r = hit[0] if hit else {}
        res.append([d, t.stem, r.get('id', ''), r.get('lista', ''), hit[1] if hit else '', r.get('titulo', '')[:80], len(txt)])
        if hit: usados.add(r['id'])
w = csv.writer(open(B / 'mapa_pdfs.csv', 'w', newline='', encoding='utf-8-sig'))
w.writerow(['pasta', 'arquivo', 'id', 'lista', 'metodo', 'titulo', 'chars']); w.writerows(res)
for x in res:
    if not x[2]: print('SEM MATCH:', x[0], x[1])
print('pdfs', len(res), 'mapeados', sum(1 for x in res if x[2]), 'ids distintos', len(usados))
dup = {}
for x in res:
    if x[2]: dup.setdefault(x[2], []).append(x[1])
print('ids repetidos:', {k: v for k, v in dup.items() if len(v) > 1})
for src in ('ieee', 'acm', 'scopus'):
    falt = [r for r in rows if r['lista'] == src and r['id'] not in usados]
    print(f'\n== faltando {src}: {len(falt)}')
    for r in falt: print('  ', r['id'], r['ano'], r['titulo'][:90], '|', r['doi'])
