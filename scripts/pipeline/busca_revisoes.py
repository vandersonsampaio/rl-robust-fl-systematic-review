"""Consolida a busca complementar por revisões anteriores (sem o bloco B), 15/10/2026.

Fontes: SLR_Related/acm_title.bib, acm_abstract.bib, ieee.csv, Scopus/*.pdf (texto extraído)
e arXiv (API; SLR_Related/arxiv_api.csv).
Saída: SLR_Related/revisoes_consolidado.csv

Uso: python scripts/busca_revisoes.py <pasta_txt_scopus>
"""
import csv
import hashlib
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
REL = os.path.join(BASE, 'SLR_Related')


def norm(t):
    t = unicodedata.normalize('NFKD', t or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', t)


def ndoi(d):
    d = (d or '').strip().lower()
    return re.sub(r'^https?://(dx\.)?doi\.org/', '', d)


def parse_bib(path):
    txt = open(path, encoding='utf-8').read()
    out = []
    for ent in re.split(r'\n(?=@)', txt):
        if not ent.strip().startswith('@'):
            continue
        f = {}
        for m in re.finditer(r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}', ent):
            f[m.group(1).lower()] = re.sub(r'\s+', ' ', m.group(2).replace('{', '').replace('}', '')).strip()
        out.append(f)
    return out


RL = re.compile(r'reinforcement|bandit|\bDQN\b|q-learning|\bDRL\b|\bMARL\b|\bRL\b|\bPPO\b|\bDDPG\b|thompson|\bUCB\b', re.I)
REV = re.compile(r'survey|review|systemati[sz]|\bSoK\b|overview|state of the art|state-of-the-art|taxonomy', re.I)
ADV = re.compile(r'byzantin|poison|backdoor|malicious|robust aggregation', re.I)

# PDFs do Scopus que não casam com nenhum registro do ACM, IEEE, arXiv ou S1:
# título, ano e DOI conferidos à mão na primeira página (16/10/2026)
SCOPUS_MANUAL = {
    '033_2025_2107_V31.pdf': ('Secure And Distributed Edge Intelligence For Consumer-Grade Smart Agriculture', '2026', '10.6180/jase.202608_31.033'),
    '1-s2.0-S0169260726002087-main.pdf': ('Federated learning: A new frontier in the exploration of multi-institutional medical imaging data', '2026', ''),
    '1-s2.0-S1877050925003503-main.pdf': ('Addressing Heterogeneity in Federated Learning: Challenges and Solutions for a Shared Production Environment', '2025', ''),
    '130631G.pdf': ('Privacy Preserving Machine Learning in Energy Services: A Survey', '2024', '10.1117/12.3021531'),
    '2842-Article+Text-14675-3-10-20260313.pdf': ('Framing Adversarial Federated Learning Threats through MITRE ATLAS', '2026', '10.19139/soic-2310-5070-2842'),
    'EBSCO-FullText-10_16_2026.pdf': ('Byzantine fault tolerance in distributed machine learning: a survey', '2025', '10.1080/0952813x.2024.2391778'),
    'EWS-Kovářová-143.pdf': ('Exploring Zero-Day Attacks on Machine Learning and Deep Learning Algorithms', '2024', ''),
    'FilePdf20260223457512024020845751.pdf': ('Federated Learning for Privacy-Preserving Intrusion Detection: A Systematic Review, Taxonomy, Challenges and Future Directions', '2025', ''),
    'IJMECS-V17-N2-4.pdf': ('Unlocking Educational Excellence: Leveraging Federated Learning for Enhanced Instructor Evaluation and Student Success', '2025', '10.5815/ijmecs.2025.02.04'),
    'International Journal of Intelligent Systems - 2026 - Wynn - Blockchain‐Based AI Intelligent Systems in Healthcare  A.pdf': ('Blockchain-Based AI Intelligent Systems in Healthcare: A Decentralized Federated Learning Framework With Zero Trust', '2026', ''),
    'Navigating the Void_ Uncovering Research Gaps in the Detection of.pdf': ('Navigating the Void: Uncovering Research Gaps in the Detection of Data Poisoning Attacks in Federated Learning-Based Big Data Processing', '2023', '10.58496/mjbd/2023/019'),
    'Paper_54-A_Review_of_Federated_Learning_Attacks.pdf': ('A Review of Federated Learning Attacks: Threat Models and Defence Strategies', '2025', ''),
    'Secure_Waveform_Computation_for_Federated_6G_Network_Challenges_and_Standardization.pdf': ('Secure Waveform Computation for Federated 6G Network: Challenges and Standardization', '2025', '10.1109/mcomstd.2025.3624308'),
    'applsci-12-09901-v2.pdf': ('Privacy and Security in Federated Learning: A Survey', '2022', '10.3390/app12199901'),
    'article_ijocta0254802191_ef35d5.pdf': ('TrustFCL: Task-grained model assessment and aggregation for secure federated continual learning', '2026', '10.36922/ijocta025480219'),
    'electronics-14-03816.pdf': ('Privacy-Preserving Federated Review Analytics with Data Quality Optimization for Heterogeneous IoT Platforms', '2025', '10.3390/electronics14193816'),
    'epjconf_icetsf2025_01066.pdf': ('Privacy-Preserving Federated Learning in Healthcare, E-Commerce, and Finance: A Taxonomy of Security Threats and Mitigation Strategies', '2025', '10.1051/epjconf/202532801066'),
    'mathematics-12-00901.pdf': ('Challenges and Countermeasures of Federated Learning Data Poisoning Attack Situation Prediction', '2024', '10.3390/math12060901'),
    's10462-024-10797-0.pdf': ('Robust and privacy-preserving collaborative training: a comprehensive survey', '2024', '10.1007/s10462-024-10797-0'),
    's10462-024-11082-w.pdf': ('Advancements in securing federated learning with IDS: a comprehensive review of neural networks and feature engineering techniques', '2025', '10.1007/s10462-024-11082-w'),
    's10462-026-11519-4.pdf': ('A survey of privacy-preserving federated learning for intrusion detection systems', '2026', '10.1007/s10462-026-11519-4'),
    's11227-025-08146-1.pdf': ('A survey on privacy issues and mitigation strategies for LLMs in healthcare', '2026', '10.1007/s11227-025-08146-1'),
    's12083-025-02167-6.pdf': ('A systematic review of secure federated learning based on blockchain and Multi-Party computation', '2026', '10.1007/s12083-025-02167-6'),
    's40537-025-01099-5.pdf': ('Adapting security and decentralized knowledge enhancement in federated learning using blockchain technology: literature review', '2025', '10.1186/s40537-025-01099-5'),
    's40747-024-01664-0.pdf': ('A survey of security threats in federated learning', '2025', '10.1007/s40747-024-01664-0'),
    's42400-021-00105-6.pdf': ('Threats, attacks and defenses to federated learning: issues, taxonomy and perspectives', '2022', '10.1186/s42400-021-00105-6'),
    'sensors-25-07619.pdf': ('IoT Authentication in Federated Learning: Methods, Challenges, and Future Directions', '2025', '10.3390/s25247619'),
}


def texto_pdf(pdf, txtdir):
    """Extrai o texto do PDF (pdftotext) para txtdir, com nome derivado do arquivo."""
    h = hashlib.md5(os.path.basename(pdf).encode('utf-8')).hexdigest()[:10]
    out = os.path.join(txtdir, h + '.txt')
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        tmp = os.path.join(txtdir, h + '.pdf')  # cópia com nome ASCII, para o pdftotext no Windows
        shutil.copyfile(pdf, tmp)
        subprocess.run(['pdftotext', '-q', tmp, out])
        os.remove(tmp)
    return open(out, encoding='utf-8', errors='ignore').read() if os.path.exists(out) else ''


# Triagem por título e resumo (revisor 1 assistido, 15/10/2026): registros novos que são revisões,
# surveys ou SoKs com a segurança de FL contra clientes adversários como tema central.
REVISOES_CENTRAIS = {
    'R-001', 'R-002', 'R-003', 'R-004', 'R-005', 'R-015', 'R-031', 'R-032', 'R-042', 'R-101', 'R-128',
    'R-133', 'R-154', 'R-159', 'R-174', 'R-222', 'R-223', 'R-229', 'R-231', 'R-232', 'R-233', 'R-239',
    'R-241', 'R-245', 'R-250', 'R-279', 'R-283', 'R-284', 'R-293', 'R-298', 'R-304', 'R-355', 'R-364',
    'R-366', 'R-371',
    # só no Scopus (16/10/2026)
    'R-377', 'R-378', 'R-384', 'R-385', 'R-388', 'R-391', 'R-393', 'R-394', 'R-402', 'R-403',
}
# Leitura das menções a RL no corpo do texto completo (PDFs do Scopus), fora das referências
CATALOGA_RL = {'R-394', 'R-355'}                      # descreve uma defesa por RL no catálogo (R-394: GAAvernor; R-355: R2Fed, lido em 22/10/2026, Q22)
# Lidos no texto completo do arXiv em 22/10/2026 (Q22), sem RL como defesa no corpo: R-004, R-128 (só RL federado), R-154, R-364, R-366, R-371
# Lidos no texto completo (PDFs obtidos pelo autor) em 22/10/2026 (Q22), sem RL como defesa no corpo: R-015, R-101 (RL só como aplicação de FL), R-223, R-233, R-284, R-298 (RL só nas referências)
SUGERE_RL = {'R-222', 'R-385', 'R-376'}      # sugere defesas por RL como direção futura, sem analisá-las
# R-232 saiu em 22/10/2026 (Q19): o RL aparece só como técnica de ataque (Henger et al.), não como defesa


def main(txtdir):
    recs = []

    def add(fonte, titulo, ano, autores, venue, doi, arxiv, resumo, rl_texto=''):
        recs.append(dict(fonte=fonte, titulo=titulo, ano=ano, autores=autores, venue=venue,
                         doi=ndoi(doi), arxiv=arxiv, resumo=resumo, rl_texto=rl_texto))

    for nome, fonte in [('acm_title.bib', 'ACM-titulo'), ('acm_abstract.bib', 'ACM-resumo')]:
        for f in parse_bib(os.path.join(REL, nome)):
            add(fonte, f.get('title', ''), f.get('year', ''), f.get('author', ''),
                f.get('journal') or f.get('booktitle', ''), f.get('doi', ''), '', f.get('abstract', ''))

    for x in csv.DictReader(open(os.path.join(REL, 'ieee.csv'), encoding='utf-8-sig')):
        add('IEEE', x['Document Title'], x['Publication Year'], x['Authors'], x['Publication Title'],
            x['DOI'], '', x['Abstract'])

    for x in csv.DictReader(open(os.path.join(REL, 'arxiv_api.csv'), encoding='utf-8')):
        add('arXiv', x['titulo'], x['ano'], x['autores'], 'arXiv', x['doi'],
            re.sub(r'v\d+$', '', x['arxiv']), x['resumo'])

    # Export CSV do Scopus (qualquer .csv em SLR_Related com "scopus" no nome), quando existir
    for nome in sorted(os.listdir(REL)):
        if 'scopus' in nome.lower() and nome.lower().endswith('.csv'):
            for x in csv.DictReader(open(os.path.join(REL, nome), encoding='utf-8-sig')):
                add('Scopus', x.get('Title', ''), x.get('Year', ''), x.get('Authors', ''),
                    x.get('Source title', ''), x.get('DOI', ''), '', x.get('Abstract', ''))

    # PDFs do Scopus (SLR_Related/Scopus): casados pelo DOI ou pelo título com os registros
    # das outras bases e da S1; os demais vêm de SCOPUS_MANUAL. Contam RL no texto completo.
    s1 = list(csv.DictReader(open(os.path.join(BASE, 'triagem_v2', 'triagem_final.csv'), encoding='utf-8-sig')))
    conhecidos = [(r['titulo'], r['ano'], r['doi']) for r in recs] + \
                 [(x['titulo'], x['ano'], ndoi(x['doi'])) for x in s1]
    conhecidos = [c for c in conhecidos if len(norm(c[0])) > 25]
    pasta = os.path.join(REL, 'Scopus')
    for arq in sorted(os.listdir(pasta)):
        if not arq.lower().endswith('.pdf'):
            continue
        t = texto_pdf(os.path.join(pasta, arq), txtdir)
        head = t[:6000]
        nh = norm(head)
        dois = [d.rstrip('.,;)').lower() for d in re.findall(r'10\.\d{4,5}/[^\s"<>]+', head)][:3]
        if arq in SCOPUS_MANUAL:
            tit, ano, doi = SCOPUS_MANUAL[arq]
        else:
            c = next((c for c in conhecidos if c[2] and any(d == c[2] or d.startswith(c[2]) for d in dois)), None)
            c = c or next((c for c in conhecidos if norm(c[0])[:60] in nh), None)
            if c is None:
                print('PDF do Scopus sem identificação:', arq)
                continue
            tit, ano, doi = c
        add('Scopus', tit, ano, '', '', doi, '', head[:3000], str(len(RL.findall(t))))

    by_doi = {ndoi(x['doi']): x for x in s1 if x['doi']}
    by_tit = {norm(x['titulo']): x for x in s1}
    by_arx = {re.sub(r'v\d+$', '', x['arxiv']): x for x in s1 if x['arxiv']}

    seen, out = {}, []
    for r in recs:
        keys = [k for k in ('doi:' + r['doi'] if r['doi'] else '',
                            'ax:' + r['arxiv'] if r['arxiv'] else '',
                            't:' + norm(r['titulo'])) if k]
        hit = next((seen[k] for k in keys if k in seen), None)
        if hit is not None:
            hit['fontes'] += ';' + r['fonte']
            if not hit['resumo'] and r['resumo']:
                hit['resumo'] = r['resumo']
            if r['rl_texto']:
                hit['rl_texto'] = r['rl_texto']
            for k in keys:
                seen[k] = hit
            continue
        r['fontes'] = r['fonte']
        m = by_doi.get(r['doi']) if r['doi'] else None
        m = m or (by_arx.get(r['arxiv']) if r['arxiv'] else None) or by_tit.get(norm(r['titulo']))
        r['s1_id'] = m['id'] if m else ''
        r['s1_decisao'] = (m['s1_decisao'] + ' ' + m['q7_decisao']).strip() if m else ''
        for k in keys:
            seen[k] = r
        out.append(r)

    for i, r in enumerate(out, 1):
        tx = r['titulo'] + ' ' + r['resumo']
        r['rid'] = 'R-%03d' % i
        r['rl_resumo'] = 'S' if RL.search(tx) else 'N'
        r['revisao_titulo_resumo'] = 'S' if REV.search(tx) else 'N'
        r['adversario'] = 'S' if ADV.search(tx) else 'N'
        r['ano_ok'] = 'S' if r['ano'].isdigit() and int(r['ano']) >= 2017 else 'N'
        if r['s1_id']:
            r['triagem'] = 'ja_na_S1'
        else:
            r['triagem'] = 'revisao_central' if r['rid'] in REVISOES_CENTRAIS else 'fora'
        if r['rid'] in CATALOGA_RL:
            r['rl_objeto'] = 'cataloga'
        elif r['rid'] in SUGERE_RL:
            r['rl_objeto'] = 'sugere_como_direcao'
        else:
            r['rl_objeto'] = 'N' if r['triagem'] == 'revisao_central' else ''
        r['texto_completo'] = 'S' if 'Scopus' in r['fontes'] else 'N'

    cols = ['rid', 'fontes', 'titulo', 'ano', 'ano_ok', 'autores', 'venue', 'doi', 'arxiv', 's1_id', 's1_decisao',
            'triagem', 'rl_objeto', 'texto_completo', 'revisao_titulo_resumo', 'adversario', 'rl_resumo', 'rl_texto', 'resumo']
    with open(os.path.join(REL, 'revisoes_consolidado.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        w.writerows(out)

    print('brutos', len(recs), dict(Counter(r['fonte'] for r in recs)))
    print('únicos', len(out))
    print('já na S1', sum(1 for r in out if r['s1_id']), dict(Counter(r['s1_decisao'] for r in out if r['s1_id'])))
    novos = [r for r in out if not r['s1_id']]
    print('novos', len(novos), '| com RL no título/resumo', sum(1 for r in novos if r['rl_resumo'] == 'S'))
    print('triagem', dict(Counter(r['triagem'] for r in out)))


if __name__ == '__main__':
    main(sys.argv[1])
