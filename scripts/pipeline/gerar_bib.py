"""Gera refs.bib (paper e capítulo) a partir das planilhas da SLR.

Chaves = ids da SLR (V2-xxxx, SB-xx), para rastrear cada citação até o material suplementar.
Entradas fixas (diretrizes, leituras canônicas, defesas clássicas) ficam em FIXAS.
ATENÇÃO: metadados vêm das exportações das bases; reconfirmar autores, venue e DOI antes da submissão.
"""
import csv
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
T = RAIZ / 'triagem_v2'
SAIDAS = [RAIZ / 'selecionados' / 'paper_slr' / 'refs.bib', RAIZ / 'selecionados' / 'tese_cap_slr' / 'refs.bib']


def ler(nome):
    return list(csv.DictReader(open(T / nome, encoding='utf-8-sig')))


REG = {r['id']: r for r in ler('registros.csv')}
Q7_TSV = {l.split('\t')[0]: l.split('\t')[1] for l in open(T / 'etapa2_lote2_q7.tsv', encoding='utf-8').read().splitlines()[1:]}


def autores_bib(s):
    s = s.strip()
    if ' and ' in s:
        return s
    partes = [p.strip() for p in s.split(';') if p.strip()]
    out = []
    for p in partes:
        if p in ('...', '…'):
            continue
        p = p.replace('...', '').strip()
        m = re.match(r'^(.+?)\s+((?:[A-Z][a-z]?\.[\s-]?)+)$', p)  # "Yang N." -> "Yang, N."
        out.append(f'{m.group(1)}, {m.group(2).strip()}' if m else p)
    if '...' in s or '…' in s:
        out.append('others')
    return ' and '.join(out)


ESC = str.maketrans({'&': r'\&', '%': r'\%', '_': r'\_', '#': r'\#', '$': r'\$'})


def esc(s):
    return (s or '').translate(ESC).replace('R\\$^{2}\\$', 'R$^{2}$')


def tipo(venue):
    v = venue.lower()
    if v == 'arxiv':
        return 'misc'
    conf = ('proceedings', 'conference', 'symposium', 'globecom', 'icc ', 'infocom', 'icassp', 'ijcai', 'workshop',
            'lecture notes', 'iclr', 'kdd', 'raid')
    return 'inproceedings' if any(c in v for c in conf) else 'article'


def entrada(key, titulo, autores, ano, venue, doi, nota=''):
    t = tipo(venue)
    campos = [('title', '{' + esc(titulo) + '}'), ('author', esc(autores_bib(autores)) if autores else 'others'),
              ('year', ano)]
    if t == 'misc':
        campos.append(('howpublished', 'arXiv preprint'))
    elif t == 'inproceedings':
        campos.append(('booktitle', esc(venue)))
    else:
        campos.append(('journal', esc(venue)))
    doi = (doi or '').strip()
    if doi.lower().startswith('arxiv:'):
        campos += [('eprint', doi[6:]), ('archiveprefix', 'arXiv')]
    elif doi:
        campos.append(('doi', doi))
    if nota:
        campos.append(('note', nota))
    corpo = ',\n'.join(f'  {k} = {{{v}}}' for k, v in campos)
    return f'@{t}{{{key},\n{corpo}\n}}\n'


def doi_de(id_, doi):
    if doi:
        return doi
    r = REG.get(id_, {})
    return r.get('doi') or (('arXiv:' + r['arxiv']) if r.get('arxiv') else '')


bib = ['% Gerado por scripts/gerar_bib.py. Reconfirmar metadados antes da submissão (pendência 3 do handoff).\n']
vistos = set()

# S1: 78 incluídos
for e in ler('extracao_principal.csv'):
    bib.append(entrada(e['id'], e['titulo'], e['autores'], e['ano'], e['venue'], doi_de(e['id'], e['doi_arxiv'])))
    vistos.add(e['id'])

# §9.2: adaptativos não-RL
for e in ler('extracao_adaptativo_nao_rl.csv'):
    if e['id'] in vistos or e['id'].startswith('SB-'):
        continue
    r = REG.get(e['id'], {})
    bib.append(entrada(e['id'], e['titulo'], r.get('autores', ''), e['ano'], e['venue'], doi_de(e['id'], e['doi_arxiv'])))
    vistos.add(e['id'])

# QP7 via busca
q7 = [x for x in ler('etapa2_arxiv.csv') + ler('etapa2_lote2.csv')
      if x['fluxo'] == 'QP7' and x['etapa2_decisao'] == 'Q7-I' and not x['id'].startswith('SB-')]
for x in q7:
    if x['id'] in vistos:
        continue
    r = REG[x['id']]
    bib.append(entrada(x['id'], r['titulo'], r['autores'], r['ano'], r['venue'] or 'arXiv', doi_de(x['id'], '')))
    vistos.add(x['id'])

FIXAS = r"""
@inproceedings{SB-04,
  title = {Byzantine-Robust Federated Learning with Learnable Aggregation Weights},
  author = {Parsa, J. and Daghestani, A. H. and Teixeira, A. M. H. and Johansson, M.},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2026},
  eprint = {2511.03529}, archiveprefix = {arXiv}
}
@inproceedings{SB-05,
  title = {{FedSecurity}: A Benchmark for Attacks and Defenses in Federated Learning and Federated {LLMs}},
  author = {Han, Shanshan and Jin, Han and Wang, Xiaoyang and Yao, Yuhang and Zhang, Yuhui and Buyukates, Baturalp and others},
  booktitle = {Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining},
  year = {2024},
  doi = {10.1145/3637528.3671545}
}
@inproceedings{SB-06,
  title = {A comparative study of defense strategies for managing malicious participants and its effects in Federated Learning systems},
  author = {Joseph, Jovi and others},
  booktitle = {2025 6th International Conference on Control, Communication and Computing (ICCC)},
  year = {2025},
  doi = {10.1109/ICCC64910.2025.11077213}
}
@article{SB-07,
  title = {Survey on federated learning threats: Concepts, taxonomy on attacks and defences, experimental study and challenges},
  author = {Rodr{\'i}guez-Barroso, Nuria and Jim{\'e}nez-L{\'o}pez, Daniel and Luz{\'o}n, M. Victoria and Herrera, Francisco and Mart{\'i}nez-C{\'a}mara, Eugenio},
  journal = {Information Fusion},
  volume = {90}, pages = {148--173},
  year = {2023}
}
@article{SB-08,
  title = {{SoK}: Understanding backdoor attacks \& defenses in federated learning},
  author = {Bellachia, Ahmed Ayoub and Bouchiha, Mouhamed Amine and Ghamri-Doudane, Yacine},
  journal = {Expert Systems with Applications},
  volume = {325}, pages = {132558},
  year = {2026}
}
@inproceedings{SB-09,
  title = {{SoK}: Systematizing Attack Studies in Federated Learning -- From Sparseness to Completeness},
  author = {Sharma, Geetanjli and Baruwal Chhetri, Mohan and others},
  booktitle = {Proceedings of the ACM Asia Conference on Computer and Communications Security (AsiaCCS)},
  year = {2023},
  doi = {10.1145/3579856.3590328}
}
@inproceedings{henderson2018,
  title = {Deep Reinforcement Learning that Matters},
  author = {Henderson, Peter and Islam, Riashat and Bachman, Philip and Pineau, Joelle and Precup, Doina and Meger, David},
  booktitle = {Proceedings of the AAAI Conference on Artificial Intelligence},
  year = {2018}
}
@inproceedings{agarwal2021,
  title = {Deep Reinforcement Learning at the Edge of the Statistical Precipice},
  author = {Agarwal, Rishabh and Schwarzer, Max and Castro, Pablo Samuel and Courville, Aaron and Bellemare, Marc G.},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2021}
}
@inproceedings{mania2018,
  title = {Simple random search of static linear policies is competitive for reinforcement learning},
  author = {Mania, Horia and Guy, Aurelia and Recht, Benjamin},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2018}
}
@inproceedings{rajeswaran2017,
  title = {Towards Generalization and Simplicity in Continuous Control},
  author = {Rajeswaran, Aravind and Lowrey, Kendall and Todorov, Emanuel and Kakade, Sham},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2017}
}
@misc{szelag2025,
  title = {Adaptive Adversaries in {Byzantine}-Robust Federated Learning: A Survey},
  author = {Szel{\k{a}}g, Jakub Kacper and Chin, Ji-Jian and Yip, Sook-Chin},
  howpublished = {IACR Cryptology ePrint Archive, Paper 2025/510},
  year = {2025}
}
@techreport{kitchenham2007,
  title = {Guidelines for performing Systematic Literature Reviews in Software Engineering},
  author = {Kitchenham, Barbara and Charters, Stuart},
  institution = {Keele University and Durham University},
  number = {EBSE-2007-01},
  year = {2007}
}
@article{page2021prisma,
  title = {The {PRISMA} 2020 statement: an updated guideline for reporting systematic reviews},
  author = {Page, Matthew J. and McKenzie, Joanne E. and Bossuyt, Patrick M. and others},
  journal = {BMJ},
  volume = {372}, pages = {n71},
  year = {2021}
}
@inproceedings{wohlin2014,
  title = {Guidelines for snowballing in systematic literature studies and a replication in software engineering},
  author = {Wohlin, Claes},
  booktitle = {Proceedings of the 18th International Conference on Evaluation and Assessment in Software Engineering (EASE)},
  year = {2014}
}
@inproceedings{mcmahan2017,
  title = {Communication-Efficient Learning of Deep Networks from Decentralized Data},
  author = {McMahan, Brendan and Moore, Eider and Ramage, Daniel and Hampson, Seth and Ag{\"u}era y Arcas, Blaise},
  booktitle = {Proceedings of the 20th International Conference on Artificial Intelligence and Statistics (AISTATS)},
  year = {2017}
}
@inproceedings{blanchard2017,
  title = {Machine Learning with Adversaries: {Byzantine} Tolerant Gradient Descent},
  author = {Blanchard, Peva and El Mhamdi, El Mahdi and Guerraoui, Rachid and Stainer, Julien},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2017}
}
@inproceedings{yin2018,
  title = {{Byzantine}-Robust Distributed Learning: Towards Optimal Statistical Rates},
  author = {Yin, Dong and Chen, Yudong and Kannan, Ramchandran and Bartlett, Peter},
  booktitle = {Proceedings of the 35th International Conference on Machine Learning (ICML)},
  year = {2018}
}
@inproceedings{cao2021fltrust,
  title = {{FLTrust}: {Byzantine}-robust Federated Learning via Trust Bootstrapping},
  author = {Cao, Xiaoyu and Fang, Minghong and Liu, Jia and Gong, Neil Zhenqiang},
  booktitle = {Network and Distributed System Security Symposium (NDSS)},
  year = {2021}
}
@inproceedings{nguyen2022flame,
  title = {{FLAME}: Taming Backdoors in Federated Learning},
  author = {Nguyen, Thien Duc and Rieger, Phillip and Chen, Huili and others},
  booktitle = {31st USENIX Security Symposium},
  year = {2022}
}
@inproceedings{fang2020,
  title = {Local Model Poisoning Attacks to {Byzantine}-Robust Federated Learning},
  author = {Fang, Minghong and Cao, Xiaoyu and Jia, Jinyuan and Gong, Neil},
  booktitle = {29th USENIX Security Symposium},
  year = {2020}
}
@inproceedings{baruch2019,
  title = {A Little Is Enough: Circumventing Defenses For Distributed Learning},
  author = {Baruch, Gilad and Baruch, Moran and Goldberg, Yoav},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2019}
}
@inproceedings{shejwalkar2021,
  title = {Manipulating the {Byzantine}: Optimizing Model Poisoning Attacks and Defenses for Federated Learning},
  author = {Shejwalkar, Virat and Houmansadr, Amir},
  booktitle = {Network and Distributed System Security Symposium (NDSS)},
  year = {2021}
}
@inproceedings{li2022attack,
  title = {Learning to Attack Federated Learning: A Model-based Reinforcement Learning Attack Framework},
  author = {Li, Henger and Sun, Xiaolu and Zheng, Zizhan},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  year = {2022}
}
@article{cohen1960,
  title = {A Coefficient of Agreement for Nominal Scales},
  author = {Cohen, Jacob},
  journal = {Educational and Psychological Measurement},
  volume = {20}, number = {1}, pages = {37--46},
  year = {1960}
}
"""
bib.append(FIXAS)

texto = '\n'.join(bib)
for s in SAIDAS:
    s.parent.mkdir(exist_ok=True)
    s.write_text(texto, encoding='utf-8')
print(f'{texto.count("@")} entradas ->', ', '.join(str(s.relative_to(RAIZ)) for s in SAIDAS))
