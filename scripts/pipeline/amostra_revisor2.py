"""Planilha cega da etapa 1 para o revisor 2 (protocolo §8.5 e §8.7).

População: os 4.054 registros triados pelos critérios da S1 (triagem_final.csv com s1_decisao preenchida).
- Calibração (§8.5, adendo A12): 20 registros, estratificados em 10 "segue" (I/D) e 10 "exclui" pela decisão
  do revisor 1; não entram no κ.
- Amostra do κ (§8.7): 20% da população (mínimo 30), sorteada entre os demais.
Semente fixa: o sorteio é reprodutível.

Saídas (triagem_v2/revisor2/):
- triagem_cega_revisor2.xlsx: vai para o revisor 2. Não tem decisões, motivos, bases nem strings.
- chave_amostra.csv: id, conjunto e ordem. Fica com o revisor 1, para calcular o κ depois.
"""
import csv
import math
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

SEMENTE = 20261005
N_CALIB = 20
FRACAO = 0.20

RAIZ = Path(__file__).resolve().parent.parent
T = RAIZ / 'triagem_v2'
OUT = T / 'revisor2'

tri = [r for r in csv.DictReader(open(T / 'triagem_final.csv', encoding='utf-8-sig')) if r['s1_decisao']]
kw = {r['id']: r['keywords'] for r in csv.DictReader(open(T / 'registros.csv', encoding='utf-8-sig'))}

rng = random.Random(SEMENTE)
ids = sorted(r['id'] for r in tri)
# Calibração estratificada pela decisão do revisor 1 (adendo A12): metade "segue" (I/D), metade "exclui".
# O sorteio simples deu 20 exclusões, o que não serve para discutir a fronteira dos critérios.
dec = {r['id']: r['s1_decisao'] for r in tri}
segue = [i for i in ids if dec[i] in ('I', 'D')]
exclui = [i for i in ids if dec[i] not in ('I', 'D')]
calib = rng.sample(segue, N_CALIB // 2) + rng.sample(exclui, N_CALIB // 2)
rng.shuffle(calib)
resto = [i for i in ids if i not in set(calib)]
n_kappa = max(30, math.ceil(FRACAO * len(ids)))
kappa = rng.sample(resto, n_kappa)  # rng.sample já devolve em ordem aleatória
por_id = {r['id']: r for r in tri}

CODIGOS = ['I', 'D', 'E-IC1', 'E-IC2', 'E-IC3', 'E-IC4', 'E-IC5',
           'E-EC1', 'E-EC2', 'E-EC3', 'E-EC4', 'E-EC5', 'E-EC6', 'E-EC7', 'E-PER']
COLS = [('Nº', 6), ('id', 10), ('Título', 45), ('Autores', 25), ('Ano', 7), ('Venue', 25),
        ('Palavras-chave', 25), ('Resumo', 90), ('Decisão', 11), ('Motivo (obrigatório se E-*)', 30), ('Observação', 25)]

ARIAL = Font(name='Arial', size=10)
NEGRITO = Font(name='Arial', size=10, bold=True)
CAB = Font(name='Arial', size=10, bold=True, color='FFFFFF')
FUNDO_CAB = PatternFill('solid', start_color='305496')
AMARELO = PatternFill('solid', start_color='FFFF00')
FINA = Side(style='thin', color='BFBFBF')
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
TOPO = Alignment(vertical='top', wrap_text=True)


def aba_triagem(wb, nome, lista):
    ws = wb.create_sheet(nome)
    for c, (titulo, larg) in enumerate(COLS, 1):
        cel = ws.cell(row=1, column=c, value=titulo)
        cel.font, cel.fill, cel.alignment, cel.border = CAB, FUNDO_CAB, TOPO, BORDA
        ws.column_dimensions[cel.column_letter].width = larg
    for n, i in enumerate(lista, 1):
        r = por_id[i]
        valores = [n, i, r['titulo'], r['autores'], r['ano'], r['venue'], kw.get(i, ''), r['resumo'], None, None, None]
        for c, v in enumerate(valores, 1):
            cel = ws.cell(row=n + 1, column=c, value=v)
            cel.font, cel.alignment, cel.border = ARIAL, TOPO, BORDA
            if c >= 9:
                cel.fill = AMARELO
        ws.row_dimensions[n + 1].height = 150
    ultima = len(lista) + 1
    dv = DataValidation(type='list', formula1='"' + ','.join(CODIGOS) + '"', allow_blank=True,
                        showErrorMessage=True, errorTitle='Código inválido',
                        error='Use um dos códigos da aba Instruções.')
    ws.add_data_validation(dv)
    dv.add(f'I2:I{ultima}')
    ws.cell(row=1, column=9).comment = Comment('Escolha um código na lista (ver aba Instruções).', 'Revisor 1')
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = f'A1:K{ultima}'
    return ultima


wb = Workbook()
ins = wb.active
ins.title = 'Instruções'
ins.column_dimensions['A'].width = 16
ins.column_dimensions['B'].width = 110

linhas = [
    ('Triagem cega por título e resumo: revisor 2', None),
    ('Revisão', 'Defesas de aprendizado federado (FL) baseadas em RL e bandits (protocolo v1.1, §7 e §8).'),
    ('Como trabalhar', 'Trie sozinho, sem consultar o revisor 1 nem as decisões dele. Decida só por título, resumo e palavras-chave. '
                       'Preencha apenas as células amarelas (colunas Decisão, Motivo e Observação).'),
    ('Ordem', '1) Aba Calibração (20 registros). Depois, discuta as divergências com o revisor 1; se a redação dos '
              'critérios mudar, a mudança é registrada no protocolo. Esses 20 não entram no κ. '
              '2) Aba Amostra_kappa, sem nova discussão até terminar.'),
    ('Regra de dúvida', 'Na dúvida, marque D (segue para o texto completo). Nunca exclua por dúvida.'),
    (None, None),
    ('Códigos', None),
    ('I', 'Inclui: atende a IC1–IC5 e a nenhum EC.'),
    ('D', 'Dúvida: segue para o texto completo.'),
    ('E-IC1', 'O sistema não é de aprendizado federado.'),
    ('E-IC2', 'Não propõe nem avalia uma defesa contra clientes adversários (bizantinos, envenenamento de dados ou de modelo, backdoor, free-riding malicioso).'),
    ('E-IC3', 'A defesa não tem componente de decisão aprendido por RL ou bandit que afete pesos de agregação, seleção/exclusão de clientes, escolha da regra de agregação ou parâmetros da defesa.'),
    ('E-IC4', 'Não há avaliação empírica (simulação ou sistema real).'),
    ('E-IC5', 'Não é artigo completo revisado por pares nem preprint com texto completo (ex.: tese, dissertação).'),
    ('E-EC1', 'O RL é usado só pelo atacante.'),
    ('E-EC2', 'Defesa adaptativa sem RL ou bandit (heurística, meta-regra fixa, otimização de uma etapa).'),
    ('E-EC3', 'RL em FL só para eficiência, energia, justiça ou comunicação, sem adversários.'),
    ('E-EC4', 'RL federado (FL para treinar agentes de RL): a robustez é do treino do RL, não uma defesa da agregação de um modelo supervisionado.'),
    ('E-EC5', 'Revisão ou survey.'),
    ('E-EC6', 'Resumo estendido, pôster, menos de 4 páginas, sem texto completo ou fora do inglês.'),
    ('E-EC7', 'Duplicata ou versão anterior de outro registro.'),
    ('E-PER', 'Publicado antes de 2017.'),
    (None, None),
    ('Exemplo', 'Decisão: E-EC3 | Motivo: DQN seleciona clientes para reduzir latência e energia; não há atacantes | Observação: (vazio)'),
    (None, None),
    ('Progresso', None),
]
for r, (a, b) in enumerate(linhas, 1):
    ca, cb = ins.cell(row=r, column=1, value=a), ins.cell(row=r, column=2, value=b)
    ca.font = NEGRITO
    cb.font = ARIAL
    ca.alignment = cb.alignment = TOPO
ins['A1'].font = Font(name='Arial', size=13, bold=True)
ins.cell(row=6, column=1).fill = AMARELO
ins.cell(row=6, column=2, value='Célula amarela = preencher.').font = ARIAL

u_cal = aba_triagem(wb, 'Calibração', calib)
u_kap = aba_triagem(wb, 'Amostra_kappa', kappa)

p = len(linhas) + 1
for k, (rotulo, aba, ultima) in enumerate((('Calibração', 'Calibração', u_cal), ('Amostra_kappa', 'Amostra_kappa', u_kap))):
    ins.cell(row=p + k, column=1, value=rotulo).font = NEGRITO
    ins.cell(row=p + k, column=2,
             value=f"=COUNTA('{aba}'!I2:I{ultima})&\" de {ultima - 1} registros decididos\"").font = ARIAL
ins.cell(row=p + 3, column=1, value='Sorteio').font = NEGRITO
ins.cell(row=p + 3, column=2,
         value=f'Sorteio aleatório com semente {SEMENTE} entre os {len(ids)} registros triados pelos critérios da S1 '
               f'(busca de 28/09/2026, já deduplicada): {N_CALIB} para calibração e {n_kappa} '
               f'(20%) para o κ. A ordem das linhas é aleatória.').font = ARIAL
ins.cell(row=p + 3, column=2).alignment = TOPO

wb.calculation.fullCalcOnLoad = True  # o Excel calcula o progresso ao abrir
OUT.mkdir(exist_ok=True)
wb.save(OUT / 'triagem_cega_revisor2.xlsx')
with open(OUT / 'chave_amostra.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'conjunto', 'ordem'])
    w.writerows([(i, 'calibracao', n) for n, i in enumerate(calib, 1)])
    w.writerows([(i, 'kappa', n) for n, i in enumerate(kappa, 1)])
print(f'população {len(ids)}; calibração {len(calib)}; κ {len(kappa)} -> {OUT.relative_to(RAIZ)}')
