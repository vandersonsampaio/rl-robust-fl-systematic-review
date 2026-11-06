"""Etapa 2 (§8.8), extração (§9.1/§9.2), qualidade (§10) e snowballing (§8.9) do lote 2:
PDFs de ACM, IEEE (parcial) e Scopus em triagem_v2/{acm,ieee,scopus}. Decisões por leitura do texto completo,
registradas em triagem_v2/etapa2_lote2_decisoes.tsv (S1) e etapa2_lote2_q7.tsv (QP7).
Reescreve extracao_principal.csv e qualidade.csv juntando o lote arXiv (etapa2_arxiv.py) e este lote."""
import csv
import contextlib
import io
from pathlib import Path

with contextlib.redirect_stdout(io.StringIO()):
    import etapa2_arxiv as ARX  # regrava os arquivos do lote arXiv (conteúdo idêntico)
from etapa2_lote2_dados import CAMPOS, D, NAO_RL
import etapa2_lote3_dados as L3
D = D + L3.D
NAO_RL = NAO_RL + L3.NAO_RL
SB_BIB = L3.SB_BIB

B = Path(__file__).resolve().parent.parent / 'triagem_v2'


def load(name, key='id'):
    return {r[key]: r for r in csv.DictReader(open(B / name, encoding='utf-8-sig'))}


def tsv(name):
    lines = open(B / name, encoding='utf-8').read().splitlines()
    head = lines[0].split('\t')
    return [dict(zip(head, l.split('\t') + [''] * (len(head) - len(l.split('\t'))))) for l in lines[1:] if l.strip()]


def write(name, header, rows):
    with open(B / name, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(name, len(rows))


REG = load('registros.csv')
for k, (t, a, y, v, d) in SB_BIB.items():
    REG[k] = {'titulo': t, 'autores': a, 'ano': y, 'venue': v, 'doi': d, 'arxiv': ''}
FIN = load('triagem_final.csv')
MAPA = {r['id']: r for r in csv.DictReader(open(B / 'mapa_pdfs.csv', encoding='utf-8-sig')) if r['id']}
S1 = tsv('etapa2_lote2_decisoes.tsv')
Q7 = tsv('etapa2_lote2_q7.tsv')

# ---------------------------------------------------------------- não recuperados
NAO_REC = {
    'V2-1189': ('ACM', 'nao_recuperado', 'Sem acesso via CAPES (Springer, ICIC 2026)'),
    'V2-1211': ('ACM', 'nao_recuperado', 'Sem acesso via CAPES (Springer, ECML-PKDD 2025)'),
    'V2-1212': ('ACM', 'nao_recuperado', 'Sem acesso via CAPES (Springer, WASA 2022)'),
    'V2-1216': ('ACM', 'nao_recuperado', 'Sem acesso via CAPES (Springer, APWeb-WAIM 2024)'),
    'V2-1348': ('ACM', 'E-IC5', 'Tese (não é artigo revisado por pares nem preprint); fora do escopo de IC5'),
    'V2-3947': ('Scopus', 'nao_recuperado', 'Sem acesso via CAPES (Springer CCIS 2026)'),
}
lista = {s: [r for r in csv.DictReader(open(B / f'download_{s}.csv', encoding='utf-8-sig'))] for s in ('ieee', 'acm', 'scopus')}
lidos = set(MAPA)
pend_ieee = [r for r in lista['ieee'] if r['id'] not in lidos]

rows = []
SNOW_ORIG = {'V2-0945': 'para trás: FedDRL (V2-2891/4778); reclassificado de E-EC4', 'SB-01': 'para trás: V2-2891, V2-0493, V2-3215',
             'SB-02': 'para trás: V2-2891, V2-0493, V2-0550', 'SB-03': 'para frente: FedAA (V2-1254)', 'SB-04': 'baixado no lugar de Zhang et al. (Neurocomputing 2024)?',
             'SB-05': 'para trás: V2-4668/V2-2053', 'SB-06': 'para frente: AdaAggRL (V2-1231)', 'SB-07': 'para trás: Meta-SG, V2-4764, V2-2103',
             'SB-08': 'para trás: BackDFL (V2-4735)', 'SB-09': 'para trás: V2-4839'}
for fluxo, lista_dec in (('S1', S1), ('QP7', Q7)):
    for r in lista_dec:
        i = r['id']; f = FIN.get(i, {})
        e1 = (f.get('s1_decisao') if fluxo == 'S1' else f.get('q7_decisao')) or f.get('s1_decisao') or '-'
        sb = 'S' if i in SNOW_ORIG else 'N'
        rows.append([i, MAPA[i]['pasta'], MAPA[i]['arquivo'], fluxo, e1, r['decisao'], r['motivo'],
                     r.get('versao_relacionada', ''), 'N', sb, SNOW_ORIG.get(i, '')])
for i, (src, dec, mot) in NAO_REC.items():
    f = FIN[i]
    rows.append([i, src.lower(), '', 'S1' if f['s1_decisao'] else 'QP7', f['s1_decisao'] or f['q7_decisao'], dec, mot, '', 'N', 'N', ''])
for r in pend_ieee:
    rows.append([r['id'], 'ieee', '', 'S1' if r['s1_decisao'] else 'QP7', r['s1_decisao'] or r['q7_decisao'], 'pendente_download',
                 'Download IEEE bloqueado temporariamente; ler depois', '', 'N', 'N', ''])
write('etapa2_lote2.csv', ['id', 'fonte', 'arquivo', 'fluxo', 'etapa1_decisao', 'etapa2_decisao', 'etapa2_motivo',
                           'versao_relacionada', 'conferido_r2', 'via_snowballing', 'origem_snowballing'], rows)

# ---------------------------------------------------------------- §9.1 e §10 (arXiv + lotes 2 e 3)
import re
ext_rows = [list(r) for r in ARX.EXTR]
qa6_manual = {r[0]: r[6] for r in ARX.rows}          # QA6 (fidelidade dos ataques) é julgamento manual
for d in D:
    rec = dict(zip(CAMPOS, d))
    i = rec['id']; g = REG[i]
    pares = 'N' if (g['venue'] or '').lower().startswith('arxiv') else 'S'
    doi = g.get('doi') or (('arXiv:' + g['arxiv']) if g.get('arxiv') else '')
    row = [i, g['titulo'], g['autores'], g['ano'], g['venue'], doi, pares, rec['dominio'], rec['cenario_fl']]
    row += [rec[c] for c in ARX.F91[9:-1]]
    row.append(rec['notas'])
    ext_rows.append(row)
    qa6_manual[i] = rec['QA'][5]

# estudos excluídos depois da extração saem da síntese (A22: V2-1120 por IC4); a ficha fica nos dados
excl_extr = {r['id'] for r in S1 if r['decisao'] != 'I'}
ext_rows = [r for r in ext_rows if r[0] not in excl_extr]

# segunda passada (revisao_extracao.tsv): sobrescreve campos após busca exaustiva no texto integral
REV = tsv('revisao_extracao.tsv')
col = {c: k for k, c in enumerate(ARX.F91)}
idx = {r[0]: r for r in ext_rows}
for r in REV:
    if r['id'] in idx:
        idx[r['id']][col[r['campo']]] = r['valor']

def qa(r):
    f = lambda c: (r[col[c]] or '').strip()
    low = lambda c: f(c).lower()
    q1 = {'S': 'N', 'N': 'S'}.get(f('vazamento_teste')[:1], 'P')
    sem = low('sementes_estatistica')
    n = [int(x) for x in re.findall(r'(\d+)\s*(?:sementes|execu|repeti|ensaios|runs|seeds)', sem)]
    var = re.search(r'dp|±|ic |ic$|ic 95|desvio|variância reportada', sem) and 'sem variância' not in sem
    cod = re.match(r'^([spn])(\s|\(|$)', sem)  # código explícito S/P/N no início do campo
    cod = cod.group(1) if cod else ''
    if cod == 's' or (not cod and n and max(n) >= 3 and var):
        q2 = 'S'
    elif cod == 'p' or (not cod and n and max(n) >= 2):
        q2 = 'P'
    else:
        q2 = 'N'
    q3 = 'S' if re.search(r'teste t|anova|ic 95|wilcoxon|testes? (estat|pareado)|p ?<|tukey|compara[çc][ãa]o estat', sem) else 'N'
    q4 = {'S': 'S', 'P': 'P'}.get(f('codigo')[:1], 'N')
    cmp_ = low('comparacao_nao_aprendida')
    if cmp_.startswith('nenhuma'):
        q5 = 'N'
    # o oráculo usa informação indisponível ao agente e fica fora de Π0: conta como P (A23, 22/10/2026)
    elif 'mesmo sinal' in cmp_ or 'míope' in cmp_ or cmp_.startswith('fixa') or re.search(r'\+ ?fixa', cmp_):
        q5 = 'S'
    else:
        q5 = 'P'
    q6 = qa6_manual.get(r[0], 'P')
    orc = re.sub(r'[^;]*não (?:reportad|localizad|informad)[^;]*', '', low('orcamento')).strip(' ;') or low('orcamento')
    if orc in ('', '?') or orc.startswith('não reportado'):
        q7 = 'N'
    # S exige volume (passos, episódios, rodadas...) e um parâmetro de otimização do agente (A20, 19/10/2026)
    elif (re.search(r'epis[óo]dio|passo|itera|rodada|slot|[ée]poca|atualiza|\bt ?=', orc)
          and re.search(r'\blr\b|taxa de aprendizado|α|γ|desconto|replay|batch', orc)):
        q7 = 'S'
    else:
        q7 = 'P'
    bl = low('baselines_estaticos') + ' ' + low('ataques') * 0
    trust = re.search(r'fltrust|zeno|root', bl)  # só defesas com dados no servidor (FLAME, FLDetector e FLGuard saíram em 17/10/2026, A19)
    stat = re.search(r'krum|median|mediana|trimmed|tm|bulyan|rfa|clipping|clipmed|normbound|cclip|signguard', bl)
    q8 = 'S' if (trust and stat) else ('P' if (trust or stat) else 'N')
    q9 = {'S': 'S', 'P': 'P'}.get(f('ataque_adaptativo')[:1], 'N')
    return [q1, q2, q3, q4, q5, q6, q7, q8, q9]

qa_val = {'S': 1, 'P': 0.5, 'N': 0}
qa_rows = []
for r in ext_rows:
    v = qa(r)
    qa_rows.append([r[0]] + v + [sum(qa_val[x] for x in v)] + [''] * 10 +
                   ['derivado por regra dos campos da extração (QA6 manual); ver notas_etapa2_lote2.md'])
write('extracao_principal.csv', ARX.F91, ext_rows)
write('qualidade.csv', ['id'] + [f'qa{k}_r1' for k in range(1, 10)] + ['total_r1'] + [f'qa{k}_r2' for k in range(1, 10)]
      + ['total_r2', 'justificativa_r1'], qa_rows)

# ---------------------------------------------------------------- §9.2
F92 = ['id', 'titulo', 'ano', 'venue', 'doi_arxiv', 'mecanismo_adaptativo', 'granularidade', 'sinal', 'memoria',
       'privacidade_sinal', 'ataques', 'ataque_adaptativo', 'codigo', 'resultado_principal', 'origem']
r92 = []
for (i, mec, gran, sinal, mem, priv, atq, adap, cod, res) in NAO_RL:
    base = i.rstrip('*'); g = REG[base]
    r92.append([base, g['titulo'], g['ano'], g['venue'], g['doi'], mec, gran, sinal, mem, priv, atq, adap, cod, res,
                'QP7 (seria EC2 na S1)' if i.endswith('*') else 'S1: E-EC2'])
write('extracao_adaptativo_nao_rl.csv', F92, r92)

# ---------------------------------------------------------------- lista de download (novos)
NOVOS = [
    ('V2-3055', 'HICSS 2023 Gradient Coupling (reenvio)', 'recebido; PDF ainda corrompido, texto recuperado dos streams', 'Q7-E'),
    ('V2-0945', 'R2Fed', 'recebido', 'I'),
    ('SB-01', 'Rjoub et al., Computing 2024', 'recebido', 'E-IC2'),
    ('SB-02', 'Rjoub et al., ISF 2024', 'recebido', 'E-IC2'),
    ('SB-03', 'FedCHO', 'recebido', 'I'),
    ('-', 'FedDive (KAIS 2025)', 'NÃO recebido', 'pendente (D)'),
    ('-', 'Zhang et al., Byzantine-robust aggregation in FL: benchmarks and analysis (Neurocomputing 2024)', 'NÃO recebido; veio 2511.03529 (FedLAW) no lugar?', 'pendente (Q7-D)'),
    ('SB-04', 'FedLAW (ICLR 2026, arXiv 2511.03529)', 'recebido (não estava na lista)', 'E-EC2 (§9.2)'),
    ('SB-05', 'FedSecurity (KDD 2024)', 'recebido', 'Q7-I'),
    ('SB-06', 'Comparative study (ICCC 2025)', 'recebido', 'Q7-I'),
    ('SB-07', 'Rodríguez-Barroso et al. (Inf. Fusion 2023)', 'recebido', 'Q7-I'),
    ('SB-08', 'Bellachia et al. SoK (ESWA 2026)', 'recebido', 'Q7-I'),
    ('SB-09', 'Sharma et al. SoK (AsiaCCS 2023)', 'recebido', 'Q7-I'),
]
write('download_lote3_status.csv', ['id', 'referencia', 'status', 'decisao'], NOVOS)
write('download_ieee_pendentes.csv', ['id', 'titulo', 'ano', 'doi', 's1_decisao', 'q7_decisao'],
      [[r['id'], r['titulo'], r['ano'], r['doi'], r['s1_decisao'], r['q7_decisao']] for r in pend_ieee])
