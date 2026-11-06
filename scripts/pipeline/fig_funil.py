"""Gera a Figura do funil de evidências da QP2 (paper_latex/figures/Fig-Funnel.tex)
diretamente da extração (triagem_v2/extracao_principal.csv e qualidade.csv).

Questão 3 do parecer: a figura antiga foi escrita à mão e tinha valores deslocados.
Cada etapa é um subconjunto da anterior, e cada contagem é de estudos únicos.

Etapas:
  1. estudos incluídos;
  2. alguma comparação com política não aprendida (categoria != nenhuma);
  3. há comparação com ação fixa, heurística (mesmo sinal ou outro sinal) ou oráculo,
     isto é, exclui os que só comparam com seleção aleatória ou ablação parcial (Tab. QP2);
  4. heurística sobre o mesmo sinal do agente;
  5. idem, com três ou mais sementes e variabilidade relatada (critério QA2 = S);
  6. idem, com teste estatístico aplicado à própria comparação com a heurística.

A etapa 6 exige verificação no texto completo, porque o QA3 da qualidade é do estudo inteiro.
Uso: python scripts/fig_funil.py
"""
import csv
import re
from pathlib import Path

R = Path(__file__).resolve().parent.parent
B = R / 'triagem_v2'
SAIDA = R / 'paper_latex' / 'figures' / 'Fig-Funnel.tex'

# Estudos com QA3 = S cujo teste estatístico NÃO se aplica à comparação com a heurística do mesmo sinal.
# V2-2103: os testes pareados (t, Wilcoxon) comparam o método com FedAvg, Krum e FLTrust; a comparação
# com a regra de pesos iguais sobre os mesmos seis sinais (Tab. 14 do artigo) traz 3 sementes, média ± dp
# e nenhum teste (conferido no texto completo em 16/10/2026).
TESTE_FORA_DA_COMPARACAO = {'V2-2103'}


def rows(n):
    return list(csv.DictReader(open(B / n, encoding='utf-8-sig')))


def cmpcat(s):
    """Mesma regra de scripts/sintese.py: categoria da referência mais forte."""
    s = s.lower()
    if s.startswith('nenhuma'): return 'nenhuma'
    if 'mesmo sinal' in s or 'míope' in s: return 'heurística (mesmo sinal)'
    # o oráculo fica fora de Π0 e não desloca uma referência admissível (A27, 22/10/2026)
    if s.startswith('fixa') or re.search(r'\+ ?fixa', s): return 'fixa'
    if 'outro sinal' in s: return 'heurística (outro sinal)'
    if 'aleatór' in s and not s.startswith('p'): return 'aleatória'
    if 'oráculo' in s: return 'oráculo'
    return 'parcial/ablação'


def etapas():
    E = rows('extracao_principal.csv')
    Q = {r['id']: r for r in rows('qualidade.csv')}
    assert len({x['id'] for x in E}) == len(E), 'ids repetidos na extração'
    cat = {x['id']: cmpcat(x['comparacao_nao_aprendida']) for x in E}

    s1 = {x['id'] for x in E}
    s2 = {i for i in s1 if cat[i] != 'nenhuma'}
    # etapa 3: alguma comparação com ação fixa, heurística ou oráculo, mesmo quando o oráculo não é a categoria (A27)
    ora = {x['id'] for x in E if 'oráculo' in x['comparacao_nao_aprendida'].lower()}
    s3 = {i for i in s2 if cat[i] in ('fixa', 'heurística (mesmo sinal)', 'heurística (outro sinal)', 'oráculo') or i in ora}
    s4 = {i for i in s3 if cat[i] == 'heurística (mesmo sinal)'}
    s5 = {i for i in s4 if Q[i]['qa2_r1'] == 'S'}
    s6 = {i for i in s5 if Q[i]['qa3_r1'] == 'S' and i not in TESTE_FORA_DA_COMPARACAO}
    S = [s1, s2, s3, s4, s5, s6]
    for a, b in zip(S, S[1:]):
        assert b <= a, 'etapas não aninhadas'
    # estudos da etapa 4 com várias execuções, mas só a média (QA2 = P)
    so_media = {i for i in s4 if Q[i]['qa2_r1'] == 'P'}
    return S, so_media


ROTULOS = [
    'Estudos incluídos',
    'Alguma política não aprendida',
    'Ação fixa, heurística ou oráculo',
    'Heurística sobre o mesmo sinal',
    'Mesmo sinal, com $\\geq$ 3 sementes e variabilidade',
    'Mesmo sinal, com teste estatístico na comparação',
]


def tex(S, so_media):
    n = [len(s) for s in S]
    extenso = {0: 'nenhum', 1: 'um', 2: 'dois', 3: 'três', 4: 'quatro'}
    letras = 'abcdef'
    coords = '\n'.join(f'        ({v},{letras[i]})' for i, v in reversed(list(enumerate(n))))
    rot = ',\n'.join(f'          {{{r}}}' for r in reversed(ROTULOS))
    return f"""% [Q3] figura gerada por scripts/fig_funil.py a partir da extração; não editar à mão
\\begin{{figure}}[!ht]
  \\revflutuante{{3}}% [Q3]
  \\centering
  \\definecolor{{barra}}{{HTML}}{{1F4E8C}}
  \\begin{{tikzpicture}}
    \\begin{{axis}}[
        xbar,
        bar width=9pt,
        width=0.82\\linewidth,
        height=6.2cm,
        xmin=0, xmax=88,
        enlarge y limits=0.10,
        axis x line=none,
        axis y line*=left,
        y axis line style={{draw=none}},
        ytick style={{draw=none}},
        symbolic y coords={{f,e,d,c,b,a}},
        ytick={{f,e,d,c,b,a}},
        yticklabels={{
{rot}
        }},
        yticklabel style={{
          font=\\footnotesize,
          align=right,
          text width=5.0cm
        }},
        nodes near coords,
        nodes near coords style={{
          font=\\footnotesize,
          anchor=west,
          text=black,
          xshift=1pt
        }},
        clip=false
      ]
      \\addplot[
        fill=barra,
        draw=none
      ] coordinates {{
{coords}
      }};
    \\end{{axis}}
  \\end{{tikzpicture}}
  \\caption{{\\revtag{{3}}Funil de evidências para a contribuição incremental do aprendizado.}}
  \\label{{fig:funil}}
\\end{{figure}}
"""


if __name__ == '__main__':
    S, so_media = etapas()
    for r, s in zip(ROTULOS, S):
        print(f'{len(s):3d}  {r}  {sorted(s) if len(s) <= 7 else ""}')
    print('só média na etapa 4:', sorted(so_media))
    SAIDA.write_text(tex(S, so_media), encoding='utf-8')
    print('gravado:', SAIDA)
