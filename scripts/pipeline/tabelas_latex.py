"""Gera as tabelas LaTeX da SLR (apêndice do paper e capítulo da tese).

Saída: selecionados/paper_slr/tab_estudos_en.tex; selecionados/tese_cap_slr/tab_{estudos,qp2,qa,nao_rl}_pt.tex (longtable).
Fonte: triagem_v2/extracao_principal.csv, qualidade.csv e extracao_adaptativo_nao_rl.csv.
As categorias (algoritmo, comparação, granularidade) usam as mesmas funções do sintese.py.
"""
import csv
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
T = RAIZ / 'triagem_v2'
E = list(csv.DictReader(open(T / 'extracao_principal.csv', encoding='utf-8-sig')))
Q = {q['id']: q for q in csv.DictReader(open(T / 'qualidade.csv', encoding='utf-8-sig'))}

ALG = {'en': {'outro': 'other', 'Q-learning tabular': 'tabular Q', 'PG/ator-crítico': 'PG/AC'},
       'pt': {'outro': 'outro', 'Q-learning tabular': 'Q tabular', 'PG/ator-crítico': 'PG/AC'}}
GRAN = {'en': {'selecao/cliente': 'selection', 'peso/cliente': 'weight', 'parametro': 'parameter', 'regra/rodada': 'rule/round'},
        'pt': {'selecao/cliente': 'seleção', 'peso/cliente': 'peso', 'parametro': 'parâmetro', 'regra/rodada': 'regra/rodada'}}
COMP = {'en': {'nenhuma': 'none', 'aleatória': 'random', 'fixa': 'fixed', 'parcial/ablação': 'partial', 'oráculo': 'oracle',
               'heurística (mesmo sinal)': 'same-signal heur.', 'heurística (outro sinal)': 'other-signal heur.'},
        'pt': {'nenhuma': 'nenhuma', 'aleatória': 'aleatória', 'fixa': 'fixa', 'parcial/ablação': 'parcial', 'oráculo': 'oráculo',
               'heurística (mesmo sinal)': 'heur. mesmo sinal', 'heurística (outro sinal)': 'heur. outro sinal'}}
MEM = {'en': {'S': 'Y', 'N': 'N', '?': '?'}, 'pt': {'S': 'S', 'N': 'N', '?': '?'}}
BS = '\\'
FIM = ' ' + BS + BS  # fim de linha de tabela


def _funcoes_sintese():
    """Importa fam/cmpcat do sintese.py sem executar o resto do script (ele escreve slr_resultado.md)."""
    src = (RAIZ / 'scripts' / 'sintese.py').read_text(encoding='utf-8')
    ns = {'re': re}
    for nome in ('fam', 'cmpcat'):
        i = src.index(f'def {nome}(')
        j = src.index('\n\n\n', i)
        exec(src[i:j], ns)
    return ns['fam'], ns['cmpcat'], (lambda g: re.split(r'[ (]', g)[0])


algoritmo, comparacao, granularidade = _funcoes_sintese()

UNI = {'Δ': r'$\Delta$', 'α': r'$\alpha$', 'ε': r'$\varepsilon$', 'φ': r'$\phi$', '−': '--', '≈': r'$\approx$',
       '≥': r'$\geq$', '≤': r'$\leq$', '±': r'$\pm$', '→': r'$\to$', '×': r'$\times$', '…': r'\ldots{}',
       '&': r'\&', '%': r'\%', '_': r'\_', '#': r'\#', '$': r'\$', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
       '<': r'$<$', '>': r'$>$', BS: r'\textbackslash{}', '{': r'\{', '}': r'\}'}


def esc(t):
    t = ''.join(UNI.get(c, c) for c in re.sub(r'\s+', ' ', t or '').strip())
    return re.sub(r'"([^"]*)"', r"``\1''", t).replace('"', "''")  # aspas retas quebram o babel (brazil)


def cite(i):
    return BS + 'citep{' + i + '}'


def longtable(spec, cap, label, cab, linhas, tam=r'\footnotesize'):
    return '\n'.join([
        '{' + tam, r'\begin{longtable}{' + spec + '}',
        r'\caption{' + cap + r'}\label{' + label + '}' + BS + BS, r'\toprule', cab + FIM, r'\midrule', r'\endfirsthead',
        r'\toprule', cab + FIM, r'\midrule', r'\endhead', r'\bottomrule', r'\endlastfoot',
        *linhas, r'\end{longtable}', '}', ''])


def por_qa(e):
    return -float(Q[e['id']]['total_r1']), e['id']


CAB = {
    'en': ('Primary studies: algorithm, granularity, memory, strongest non-learned comparison and quality score (QA, 0--9).',
           'Study & Year & Algorithm & Granularity & Mem. & Non-learned comparison & QA'),
    'pt': ('Estudos primários: algoritmo, granularidade, memória, comparação não aprendida mais forte e nota de qualidade (QA, 0--9).',
           'Estudo & Ano & Algoritmo & Granularidade & Mem. & Comparação não aprendida & QA'),
}


def estudos(lang):
    linhas = []
    for e in sorted(E, key=por_qa):
        alg = algoritmo(e['algoritmo'])
        g = granularidade(e['granularidade'])
        c = comparacao(e['comparacao_nao_aprendida'])
        linhas.append(' & '.join([
            cite(e['id']), e['ano'], ALG[lang].get(alg, alg), GRAN[lang].get(g, g),
            MEM[lang].get(e['memoria'][:1], '?'), COMP[lang][c], Q[e['id']]['total_r1']]) + FIM)
    cap, cab = CAB[lang]
    return longtable('llllcll', cap, f'tab:estudos-{lang}', cab, linhas)


ORDEM = {'fixa': 0, 'heurística (mesmo sinal)': 1, 'heurística (outro sinal)': 2, 'aleatória': 3,
         'parcial/ablação': 4, 'oráculo': 5}


def qp2_pt():
    sel = sorted((e for e in E if comparacao(e['comparacao_nao_aprendida']) != 'nenhuma'),
                 key=lambda e: (ORDEM[comparacao(e['comparacao_nao_aprendida'])], e['id']))
    # a coluna "discutido" saiu (A21): com a leitura literal do §2.5, todos os estudos com comparação têm S
    linhas = [' & '.join([cite(e['id']), e['ano'], esc(e['comparacao_nao_aprendida']), esc(e['resultado_comparacao'])]) + FIM
              for e in sel]
    return longtable(r'llp{0.33\linewidth}p{0.45\linewidth}',
                     f'Os {len(sel)} estudos com alguma comparação não aprendida: natureza e resultado relatado.',
                     'tab:qp2-completa', 'Estudo & Ano & Comparação & Resultado relatado', linhas, r'\scriptsize')


def qa_pt():
    ks = [f'qa{i}_r1' for i in range(1, 10)]
    linhas = [' & '.join([cite(e['id'])] + [Q[e['id']][k] for k in ks] + [Q[e['id']]['total_r1']]) + FIM
              for e in sorted(E, key=por_qa)]
    return longtable('l' + 'c' * 9 + 'r', 'Avaliação de qualidade por estudo (S = 1; P = 0,5; N = 0).', 'tab:qa-completa',
                     'Estudo & QA1 & QA2 & QA3 & QA4 & QA5 & QA6 & QA7 & QA8 & QA9 & Total', linhas)


def nao_rl_pt():
    N = list(csv.DictReader(open(T / 'extracao_adaptativo_nao_rl.csv', encoding='utf-8-sig')))
    linhas = [' & '.join([cite(n['id']), n['ano'], esc(n['mecanismo_adaptativo']),
                          GRAN['pt'].get(granularidade(n['granularidade']), esc(n['granularidade'])),
                          esc(n['privacidade_sinal']), esc(n['resultado_principal'])]) + FIM for n in N]
    return longtable(r'llp{0.3\linewidth}lp{0.14\linewidth}p{0.25\linewidth}',
                     'Defesas adaptativas sem RL ou bandit lidas no texto completo (ficha reduzida).', 'tab:nao-rl',
                     'Estudo & Ano & Mecanismo adaptativo & Granul. & Exigência do sinal & Resultado principal',
                     linhas, r'\scriptsize')


if __name__ == '__main__':
    saidas = [(RAIZ / 'selecionados' / 'paper_slr' / 'tab_estudos_en.tex', estudos('en')),
              (RAIZ / 'selecionados' / 'tese_cap_slr' / 'tab_estudos_pt.tex', estudos('pt')),
              (RAIZ / 'selecionados' / 'tese_cap_slr' / 'tab_qp2_pt.tex', qp2_pt()),
              (RAIZ / 'selecionados' / 'tese_cap_slr' / 'tab_qa_pt.tex', qa_pt()),
              (RAIZ / 'selecionados' / 'tese_cap_slr' / 'tab_nao_rl_pt.tex', nao_rl_pt())]
    for destino, texto in saidas:
        destino.parent.mkdir(exist_ok=True)
        destino.write_text(texto, encoding='utf-8')
        print(destino.relative_to(RAIZ))
