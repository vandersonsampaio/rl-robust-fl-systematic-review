"""Gera o heatmap TikZ da avaliação de qualidade (Figura 5) a partir de triagem_v2/qualidade.csv.

Saída: paper_latex/figures/Fig-Heatmap.tex. Colunas ordenadas pela nota total (decrescente);
nos empates, mantém a ordem da versão anterior da figura (ORDEM_ANTERIOR) e depois o id.
"""
import csv
from pathlib import Path

R = Path(__file__).resolve().parent.parent
Q = {r['id']: r for r in csv.DictReader(open(R / 'triagem_v2' / 'qualidade.csv', encoding='utf-8-sig'))}

ORDEM_ANTERIOR = ('2103 3243 4812 0688 2188 1483 4789 SB-03 1057 1105 1120 1231 0350 0922 0987 2573 4059 0160 0542 0837 1041 '
                  '1130 1178 3215 3555 4728 0351 0391 0918 1126 1199 1254 1327 3265 3331 4540 0111 0383 0530 0634 1030 1102 1229 '
                  '4266 4339 0506 0945 0973 1001 1140 1179 1294 2890 2891 4233 0495 0835 0940 0946 1012 1103 1185 1275 1450 2475 '
                  '3175 3494 3789 3830 4727 0065 0550 1025 1042 1261 1363 0368 0590').split()
rot = lambda i: i if i.startswith('SB-') else 'V2-' + i
pos = {rot(i): k for k, i in enumerate(ORDEM_ANTERIOR)}
ids = sorted(Q, key=lambda i: (-float(Q[i]['total_r1']), pos.get(i, 999), i))
N = len(ids)  # 77 desde o A22 (V2-1120 excluído por IC4)

cor = {'S': 'qaS', 'P': 'qaP', 'N': 'qaN'}
fmt = lambda v: f'{v:.1f}'.replace('.', ',')
L = [r'\begin{figure*}[!ht]', r'  \centering',
     r'  \definecolor{qaS}{HTML}{1F4E8C}', r'  \definecolor{qaP}{HTML}{8DB0DE}', r'  \definecolor{qaN}{HTML}{EEF2F7}',
     r'  \begin{tikzpicture}[x=0.19cm,y=0.36cm,font=\scriptsize]']
for k in range(1, 10):
    L.append(rf'    \node[anchor=east] at (-0.3,-{k - 1}.45) {{QA{k}}};')
marcas, ant = [], None
for c, i in enumerate(ids):
    for k in range(1, 10):
        L.append(rf'    \fill[{cor[Q[i][f"qa{k}_r1"]]}] ({c},-{k - 1}) rectangle ++(0.9,-0.9);')
    lab = i.replace('V2-', '')
    L.append(rf'    \node[rotate=90,anchor=east,font=\fontsize{{4.5}}{{5}}\selectfont] at ({c}.45,-9.2) {{{lab}}};')
    t = float(Q[i]['total_r1'])
    if t != ant:
        marcas.append((c, t)); ant = t
for n, (c, t) in enumerate(marcas):
    h = '0.4' if n % 2 == 0 else '1.4'
    L.append(rf'    \draw[black!50] ({c}.45,0.15) -- ++(0,{h}) node[above,font=\tiny,inner sep=1pt] {{{fmt(t)}}};')
L += r'''    \node[anchor=west,font=\tiny,text=black!60] at (78.3,0.6) {Total};
    \begin{scope}[shift={(13,-11.9)}]
      \fill[qaS] (0,0) rectangle ++(1.5,-0.9);
      \node[anchor=west] at (1.8,-0.45) {meets (S = 1)};

      \fill[qaP] (14,0) rectangle ++(1.5,-0.9);
      \node[anchor=west] at (15.8,-0.45) {partially meets (P = 0.5)};

      \fill[qaN] (30,0) rectangle ++(1.5,-0.9);
      \draw[black!30] (30,0) rectangle ++(1.5,-0.9);
      \node[anchor=west] at (31.8,-0.45) {does not meet or not reported (N = 0)};
    \end{scope}
  \end{tikzpicture}
  \revflutuante{5}% [Q5]
  \caption{\revtag{5}Quality assessment of the 78 studies across nine criteria.}
  \label{fig:qa-heatmap}
\end{figure*}'''.split('\n')  # legenda e legenda da figura iguais às do paper
L = [l.replace('(78.3,', f'({N}.3,').replace('the 78 studies', f'the {N} studies') for l in L]
out = R / 'paper_latex' / 'figures' / 'Fig-Heatmap.tex'
out.write_text('\n'.join(L) + '\n', encoding='utf-8')
print(out, '| ordem:', ' '.join(i.replace('V2-', '') for i in ids[:12]), '...')
print('marcas:', [(c, fmt(t)) for c, t in marcas])
