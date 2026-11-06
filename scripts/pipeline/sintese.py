"""Síntese §12 e PRISMA final (§11.4). Gera slr_resultado.md a partir das planilhas de triagem_v2/."""
import csv
import re
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parent.parent
B = R / 'triagem_v2'


def rows(n):
    return list(csv.DictReader(open(B / n, encoding='utf-8-sig')))


E = rows('extracao_principal.csv')
Q = {r['id']: r for r in rows('qualidade.csv')}
qc = lambda k, v: sum(Q[x['id']][f'qa{k}_r1'] == v for x in E)
A = rows('etapa2_arxiv.csv')
L = rows('etapa2_lote2.csv')
N92 = rows('extracao_adaptativo_nao_rl.csv')


def short(t, n=60):
    t = re.sub(r'\s+', ' ', t or '')
    return t if len(t) <= n else t[:n - 1] + '…'


def fam(a):
    a = a.lower()
    if re.search(r'bandit|ucb|thompson|exp3|mab', a): return 'bandit'
    if 'marl' in a or 'multiagente' in a or 'maddpg' in a: return 'MARL'
    if re.search(r'ddpg|td3|sac\b|soft actor', a): return 'DDPG/TD3/SAC'
    if re.search(r'ppo|a2c|a3c|ator-crítico|actor|policy gradient|trpo', a): return 'PG/ator-crítico'
    if re.search(r'dqn|ddqn|double', a): return 'DQN/DDQN'
    if re.search(r'q-learning|tabular', a): return 'Q-learning tabular'
    return 'outro'


def cmpcat(s):
    s = s.lower()
    if s.startswith('nenhuma'): return 'nenhuma'
    if 'mesmo sinal' in s or 'míope' in s: return 'heurística (mesmo sinal)'
    # o oráculo fica fora de Π0 e não desloca uma referência admissível (A27, 22/10/2026)
    if s.startswith('fixa') or re.search(r'\+ ?fixa', s): return 'fixa'
    if 'outro sinal' in s: return 'heurística (outro sinal)'
    if 'aleatór' in s and not s.startswith('p'): return 'aleatória'
    if 'oráculo' in s: return 'oráculo'
    return 'parcial/ablação'


def priv(p):
    p = p.lower()
    if p.startswith('só'): return 'só updates'
    if 'reconstru' in p: return 'reconstrução de dados do cliente'
    if 'teste' in p: return 'conjunto de teste no servidor'
    if re.search(r'root|validação|dataset|conjunto|entrevista|auxiliar|desafio|proxy', p): return 'dados no servidor'
    if re.search(r'tráfego|auditoria|atributos|evidências', p): return 'monitoramento do dispositivo'
    return 'outro'


gran = lambda g: re.split(r'[ (]', g)[0]
# pré-treino/offline; "sem pré-treino" não conta
offl = lambda x: bool(re.search(r'(?<!sem )(offline|pré-treino|pré-treinado)', x['modo'].lower()))
out = []
w = out.append

# ------------------------------------------------------------------ PRISMA
s1_busca = [x for x in A if x['fluxo'] == 'S1'] + [x for x in L if x['fluxo'] == 'S1' and x['via_snowballing'] == 'N']
s1_snow = [x for x in L if x['fluxo'] == 'S1' and x['via_snowballing'] == 'S']
q7_busca = [x for x in A if x['fluxo'] == 'QP7'] + [x for x in L if x['fluxo'] == 'QP7' and x['via_snowballing'] == 'N']
q7_snow = [x for x in L if x['fluxo'] == 'QP7' and x['via_snowballing'] == 'S']
nr = lambda xs: [x for x in xs if x['etapa2_decisao'] in ('nao_recuperado',) or (x['etapa2_decisao'] == 'E-IC5')]
exc = lambda xs: Counter(x['etapa2_decisao'] for x in xs if x['etapa2_decisao'].startswith('E-') and x['etapa2_decisao'] != 'E-IC5')
inc_b = sum(x['etapa2_decisao'] == 'I' for x in s1_busca)
inc_s = sum(x['etapa2_decisao'] == 'I' for x in s1_snow)
q7i_b = sum(x['etapa2_decisao'] == 'Q7-I' for x in q7_busca)
q7i_s = sum(x['etapa2_decisao'] == 'Q7-I' for x in q7_snow)

w('# Resultado da revisão sistemática: defesas de FL com RL/bandits e o que o aprendizado contribui\n')
w('**Protocolo:** `slr_protocolo_v1.1.md` (com os adendos A1–A17 do §15.3). **Busca:** 2026-09-28. **Revisores:** revisor 1 (autor) em todas as etapas; '
  'revisor 2 na calibração e numa amostra cega de 20% da etapa 1 (A12–A13) e na conferência da etapa 2, da QP2 e de 20% da qualidade (A16).  ')
w('**Arquivos-base:** `triagem_v2/` → `registros.csv`, `triagem_final.csv`, `etapa2_arxiv.csv`, `etapa2_lote2.csv`, `extracao_principal.csv`, '
  '`qualidade.csv`, `extracao_adaptativo_nao_rl.csv`, `extracao_qp7.csv`, `revisao_extracao.tsv`, `revisor2/consenso_etapa2.csv`; log em `triagem/log_buscas.csv`.\n')

w('## 1. Fluxo PRISMA 2020 (§11.4)\n')
w('| etapa | S1 (síntese principal) | QP7 |')
w('|---|---|---|')
w('| Registros identificados (brutos, todas as bases e strings) | 6.580 (IEEE 1.202; ACM 268; Scopus 4.875; arXiv 235) | (mesma base) |')
w('| Duplicatas removidas | 1.717 | |')
w('| Registros únicos triados na etapa 1 | 4.863 | 4.863 |')
w('| Excluídos na etapa 1 | ver `prisma_v2.md` (E-IC1 2.910; E-EC4 244; E-IC2 222; E-EC3 221; E-IC3 119; E-EC5 92; E-PER 67; E-EC1 20; E-IC4 6; E-EC6 3) | Q7-E 786 |')
w('| Para a ficha §9.2 já na etapa 1 (E-EC2) | 26 | |')
w(f'| Texto completo buscado (via busca) | {len(s1_busca)} | {len(q7_busca)} |')
w(f'| Não recuperados | {len(nr(s1_busca))} (sem acesso CAPES) | {len(nr(q7_busca))} (1 sem acesso; 1 tese → E-IC5) |')
w(f'| Texto completo avaliado (via busca) | {len(s1_busca) - len(nr(s1_busca))} | {len(q7_busca) - len(nr(q7_busca))} |')
ex = exc(s1_busca)
w('| Excluídos na etapa 2 | ' + f'{sum(ex.values())}: ' + ', '.join(f'{k} {v}' for k, v in ex.most_common()) +
  f' (E-EC2 → §9.2) | {sum(x["etapa2_decisao"] == "Q7-E" for x in q7_busca)} (Q7-E) |')
w(f'| **Incluídos via busca** | **{inc_b}** | **{q7i_b}** |')
w(f'| Snowballing: avaliados / não recuperados | {len(s1_snow)} / 1 (FedDive) | {len(q7_snow)} / 1 (Zhang et al. 2024) |')
w(f'| **Incluídos via snowballing** | **{inc_s}** (R2Fed, FedCHO) | **{q7i_s}** |')
w('| Leituras canônicas (§13, inclusão direta) | — | **5** |')
w(f'| **Total incluído** | **{inc_b + inc_s}** | **{q7i_b + q7i_s + 5}** |')
w(f'\nVersões anteriores excluídas por EC7 (mantida a publicada): OptiGradTrust (V2-4818 → V2-2103), FedDRL (V2-4778 → V2-2891), '
  'rDP (V2-4729 → V2-0530), DeSMP (V2-0423 → V2-0530), RAFRL (V2-1002 → V2-1001), DRL-trust IWCMC (V2-1038 → V2-1102). '
  f'Ficha §9.2 (adaptativos não-RL lidos no texto completo): {len(N92)}.\n')

# ------------------------------------------------------------------ QP1/QP4 mapeamento
w('## 2. Mapeamento (QP1 e QP4)\n')
c_alg = Counter(fam(x['algoritmo']) for x in E)
c_gran = Counter(gran(x['granularidade']) for x in E)
c_mem = Counter(x['memoria'][:1] for x in E)
c_dom = Counter(x['dominio'].split(' (')[0] for x in E)
c_ano = Counter(x['ano'] for x in E)
w(f'**{len(E)} estudos**; {sum(x["revisado_por_pares"] == "S" for x in E)} revisados por pares e '
  f'{sum(x["revisado_por_pares"] == "N" for x in E)} preprints. Por ano: ' + ', '.join(f'{k}: {v}' for k, v in sorted(c_ano.items())) + '. '
  'A área é recente: 2/3 dos estudos são de 2025–2026.\n')
w('| eixo | distribuição |')
w('|---|---|')
w('| algoritmo | ' + '; '.join(f'{k} {v}' for k, v in c_alg.most_common()) + ' |')
w('| granularidade | ' + '; '.join(f'{k} {v}' for k, v in c_gran.most_common()) + ' |')
w('| memória entre rodadas | ' + f'S {c_mem["S"]}; N {c_mem["N"]}; ? {c_mem["?"]}' + ' (reputação, confiança acumulada, posteriores, LSTM/ESN) |')
w('| domínio | ' + '; '.join(f'{k} {v}' for k, v in c_dom.most_common()) + ' |')
w('| modo de aprendizado | ' + f'online {sum(not offl(x) for x in E)}; com pré-treino/offline {sum(offl(x) for x in E)} |')
w('')
w(f'**Leitura:** a forma dominante é **seleção de clientes por agente** ({c_gran["selecao/cliente"]}/{len(E)}), seguida de **pesos por cliente** ({c_gran["peso/cliente"]}). A "escolha da regra de agregação por rodada", '
  f'que motiva o artigo de auditoria (AdaAggRL no QGS, SARA, FedStrategist, DTAG-FL; o TARS saiu por IC4, A22), é minoritária ({c_gran["regra/rodada"]}). Em quase todos os estudos o agente é acoplado a um '
  '**sinal de detecção próprio** (reputação, cosseno/distância, anomalia por autoencoder, Shapley, acurácia em validação); '
  f'em {c_mem["S"]} há memória explícita entre rodadas. '
  'Por isso, na maioria, o que o agente aprende é **como usar um escore que já separa bons e maus clientes**, e é exatamente essa separação que um limiar fixo sobre o mesmo escore também explora.\n')

# QP4: ablações por eixo
def has(x, pat): return re.search(pat, (x['ablacoes'] + ' ' + x['comparacao_nao_aprendida']).lower())
ab_learn = [x['id'] for x in E if cmpcat(x['comparacao_nao_aprendida']) != 'nenhuma']
# listas curadas na leitura (a busca por palavras-chave gerava falsos positivos)
ab_sig = ['V2-4728', 'V2-1231', 'V2-0634', 'V2-3555', 'V2-2188', 'V2-2103', 'V2-0495', 'V2-3243', 'V2-1483', 'V2-4812', 'SB-03']
ab_mem = []
ab_mem_ind = ['V2-3555', 'V2-2188']
ab_gran = []
w('**Ablações por eixo (QP4)** — contagem de estudos que isolam cada componente (texto de `ablacoes` e `comparacao_nao_aprendida`):\n')
w(f'- aprendizado (alguma política não aprendida ou remoção do agente): **{len(ab_learn)}**;')
w(f'- sinal: **{len(ab_sig)}** ({", ".join(ab_sig)});')
w(f'- memória: **0** dedicadas; {len(ab_mem_ind)} indiretas, que removem a confiança acumulada junto com outras coisas ({", ".join(ab_mem_ind)});')
w(f'- granularidade: **{len(ab_gran)}**. Nenhum estudo compara, com o mesmo sinal, decidir uma regra por rodada contra decidir pesos por cliente.\n')

# ------------------------------------------------------------------ QP2
w('## 3. QP2 (central): comparação com políticas não aprendidas\n')
c_cmp = Counter(cmpcat(x['comparacao_nao_aprendida']) for x in E)
w('| natureza da comparação | nº de estudos |')
w('|---|---|')
for k in ['nenhuma', 'aleatória', 'parcial/ablação', 'fixa', 'heurística (mesmo sinal)', 'heurística (outro sinal)', 'oráculo']:
    w(f'| {k} | {c_cmp.get(k, 0)} |')
w('')
w('Tabela de todos os estudos com alguma comparação não aprendida (ordem: fixa, mesmo sinal, outro sinal, aleatória, parcial, oráculo):\n')
w('| id | estudo | ano | comparação | resultado | discutido? |')
w('|---|---|---|---|---|---|')
order = {'fixa': 0, 'heurística (mesmo sinal)': 1, 'heurística (outro sinal)': 2, 'aleatória': 3, 'parcial/ablação': 4, 'oráculo': 5}
for x in sorted((x for x in E if cmpcat(x['comparacao_nao_aprendida']) != 'nenhuma'),
                key=lambda x: (order[cmpcat(x['comparacao_nao_aprendida'])], x['id'])):
    w(f"| {x['id']} | {short(x['titulo'], 45)} | {x['ano']} | {short(x['comparacao_nao_aprendida'], 70)} | "
      f"{short(x['resultado_comparacao'], 150)} | {x['discutido_como_achado'][:1] or 'N'} |")
w('')
nforte = sum(c_cmp.get(k, 0) for k in ('fixa', 'heurística (mesmo sinal)', 'oráculo', 'heurística (outro sinal)'))
w(f'**Contagem de votos (descritiva, sem meta-análise, §12.2):** entre os {nforte} estudos com comparação fixa, heurística ou oráculo, o agente')
w('- **empata ou perde** para política fixa ou de mesmo sinal em **7**: V2-4540 (o escore por reputação iguala ou supera o híbrido nos três regimes, Figs. 9–11, e o DRL puro perde nos três; execução única), V2-1179 (φ fixo a 1,1 p.p. do DDPG com k = 10 sob ataque; sem ataque, DDPG ≈ φ = 0), V2-1327 (peso fixo a ~1 p.p. do DRL sob envenenamento), '
  'V2-4789 (braço fixo empata ou vence; no ataque furtivo, FedAvg 39,43 × agente 38,82), '
  'V2-0350 (o local-only, λ = 0 fixo, supera o pFedMARL em F1 nos três cenários), V2-0111/SARA (comparável à melhor regra fixa: Median no ataque periódico, Krum no de fingimento no MNIST; A27), V2-2103 (regra de pesos iguais sobre os mesmos 6 sinais: acurácia final igual, 64,35 × 64,32, 3 sementes; o RL só melhora o F1 de detecção, e a variante sem RL faz o mesmo);')
w('- **iguala o oráculo** em 3 (o oráculo fica fora de Π0 e não define a categoria quando há referência admissível, A27): V2-0383 (≈ regra que conhece os modelos sem defeito), V2-1275 (≈ retreino do zero, a custo menor), V2-0111/SARA (escolhe a regra ótima em 27/30 rodadas);')
w('- **vence por margem pequena** (≤ ~6 p.p., sem teste estatístico) em V2-0973 (0,96 × 0,92), V2-1102 (limiar estático: 0,89 × 0,86 com k = 5 e 0,68 × 0,62 com k = 10), SB-03/FedCHO (61,6 × 58,5), V2-0351 (seleção direta por reputação: taxa de erro ~0,03–0,06 × ~0,04–0,12, de 1 a 6 p.p.);')
w('- **vence claramente** uma política fixa que já é uma defesa em V2-4812 (Meta-SG, parâmetros afinados; execução única),'
  'V2-2573 (execução única, 12 rodadas), V2-0160 e V2-1130 (auditoria fixa: CJR > 0,9 × 0,55-0,60, sem variância);')
w('- **vence heurísticas de outro sinal** em 6 (V2-0542, V2-1140, V2-1199, V2-3215: Pow-d, que colapsa quando o atacante infla a perda; V2-0835: gulosa por CPU; V2-4059: AMA, que não recebe o indicador de falha do RL).')
w(f'- Contra a **seleção aleatória** ({c_cmp.get("aleatória", 0)} estudos), o agente supera a aleatória em ao menos uma métrica relatada em 17, mas a vantagem nem sempre vem do aprendizado. '
  'Em 2 a métrica principal não melhora: em V2-1363 a acurácia passa de 97% com e sem o agente, porque a robustez vem da verificação e o DRL só reduz custo; em V2-0688 o ASR é o mesmo com e sem o bandit (a defesa vem da destilação, como os autores reconhecem). '
  'Há ressalvas em outros: V2-2475 relata que as variantes UCB-CS escolhem quase tantos maliciosos quanto a aleatória; em V2-4728 o DQN tem ASR pior que o aleatório (41 × 36).\n')
w('Contra uma política do **mesmo sinal**, o agente não vence claramente em nenhum dos 6 estudos: empata em 2 (V2-2103, V2-4540) e vence por margem pequena em 4. '
  'Só dois desses estudos usam várias sementes (SB-03 e V2-2103), e nenhum aplica teste estatístico a essa comparação. '
  'Onde a comparação existe com uma política fixa razoável (V2-1179, 1327, 2103, 4789, 4540), o resultado é empate, mas **nenhum conclui que o aprendizado é dispensável** (§9, Portão N).\n')

# ------------------------------------------------------------------ QP3
w('## 4. QP3: orçamento de aprendizado\n')
q7c = Counter(Q[x['id']]['qa7_r1'] for x in E)
n_off = sum(offl(x) for x in E)
w(f'- Aprendizado **online durante o FL** em {len(E) - n_off}/{len(E)}; pré-treino/offline em {n_off} (ex.: Meta-SG, rDP, RA-RL, V2-1103, V2-3243, V2-1327 pré-treinado).')
w(f'- Orçamento **calculável** (QA7 = S) em {q7c["S"]}; parcial em {q7c["P"]}; não reportado em {q7c["N"]}.')
w('- **Nenhum estudo compara agente e política não aprendida em horizontes diferentes** (critério do adendo A14). Dois variam o nº de rodadas só para o próprio método '
  '(V2-1483, T de 50 a 200; SB-03, T de 50 a 500); os demais mostram curvas de convergência, sensibilidade de γ ou limites teóricos de regret.')
w('- Orçamentos efetivos ínfimos aparecem com frequência: DTAG-FL (~12 passos de PPO), TD3-agg V2-3494 (20 rodadas), RL-FL V2-1025 (20 rodadas), '
  'OptiGradTrust (25–30 rodadas; nos experimentos de revisão o RL fica congelado), Trust-Aware DQN (ε decai em 5.000 passos com só 50 rodadas), FedStrategist (50–75 atualizações do LinUCB). '
  'No outro extremo, Meta-SG (~10⁴ passos de TD3 no pré-treino) e rDP (~60.000 episódios offline sobre perdas pré-medidas).')
w('- Implicação: em muitos estudos o agente mal sai da inicialização/exploração no horizonte avaliado. (Nota interna, fora do artigo: compatível com a observação do §1.2 de política que não se afasta da inicialização.)\n')

# ------------------------------------------------------------------ QP5
w('## 5. QP5: custo e exposição de privacidade do sinal\n')
c_priv = Counter(priv(x['privacidade_sinal']) for x in E)
w('| exigência do sinal | nº |')
w('|---|---|')
for k, v in c_priv.most_common():
    w(f'| {k} | {v} |')
w('')
w('- **Reconstrução de dados do cliente**: AdaAggRL (inversão de gradiente + MMD) e Meta-SG (inversão + cGAN/difusão).')
w(f'- **Dados no servidor** (root, validação, "entrevista", auxiliar, proxy ou teste): {c_priv["dados no servidor"] + c_priv["conjunto de teste no servidor"]} estudos; '
  f'em {c_priv["conjunto de teste no servidor"]} deles o dado declarado é o **conjunto de teste** ou foi retirado dele.')
w('- **Monitoramento do dispositivo**: tráfego de rede (V2-0391), auditoria de parâmetros e amostras (V2-1130), atributos sociais (V2-0634).')
w(f'- **Custo** reportado com números em {sum(x["custo"][:1] == "S" for x in E)}/{len(E)} (quase sempre tempo por rodada ou overhead relativo); '
  'poucos reportam o custo do treino do agente em si.\n')

# ------------------------------------------------------------------ QP6
w('## 6. QP6: qualidade da avaliação (QA1–QA9)\n')
w('Pontuação S = 1, P = 0,5, N = 0 (§10). QA1–QA5 e QA7–QA9 derivados por regra dos campos da extração (adendo A10); QA6 manual.\n')
tot = [float(Q[x['id']]['total_r1']) for x in E]
w(f'- Média **{sum(tot) / len(tot):.2f}**/9; mediana {sorted(tot)[len(tot) // 2]:.1f}; máximo {max(tot)} (V2-2103); '
  f'{sum(t >= 5 for t in tot)} estudos com ≥ 5.')
w('| critério | S | P | N |')
w('|---|---|---|---|')
nomes = ['QA1 sem teste na recompensa/seleção', 'QA2 ≥ 3 sementes com variância', 'QA3 teste estatístico ou IC', 'QA4 código disponível',
         'QA5 comparação não aprendida', 'QA6 ataques fiéis à definição', 'QA7 orçamento calculável', 'QA8 baselines estáticos fortes', 'QA9 ataque adaptativo']
for k, nm in enumerate(nomes, 1):
    c = Counter(Q[x['id']][f'qa{k}_r1'] for x in E)
    w(f'| {nm} | {c["S"]} | {c["P"]} | {c["N"]} |')
w('')
w('**Por que a qualidade é baixa:** a literatura é dominada por venues aplicados (IoT, veicular, blockchain) que avaliam um cenário contra FedAvg, '
  'com uma execução, sem código e sem ataque que conheça a defesa. A nota não reflete falta de informação na extração: depois da segunda passada, '
  f'"?" só resta onde o texto não diz em que dados a recompensa é calculada; esses casos e os que usam amostras do pool de teste ficam com QA1 = P ({qc(1, "P")} estudos).\n')
w('Mapa QA por estudo:\n')
w('| id | estudo | ano | alg. | gran. | QA1 | QA2 | QA3 | QA4 | QA5 | QA6 | QA7 | QA8 | QA9 | total |')
w('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for x in sorted(E, key=lambda x: -float(Q[x['id']]['total_r1'])):
    q = Q[x['id']]
    w(f"| {x['id']} | {short(x['titulo'], 40)} | {x['ano']} | {fam(x['algoritmo'])} | {gran(x['granularidade'])} | " +
      ' | '.join(q[f'qa{k}_r1'] for k in range(1, 10)) + f" | {q['total_r1']} |")
w('')

# ------------------------------------------------------------------ QP7
w('## 7. QP7: auditorias e baselines simples (síntese narrativa)\n')
# Composição a partir da ficha da QP7 (Questão 10 do parecer, 16/10/2026): os trabalhos da QP7 não fazem
# parte da população principal; o V2-3771 (MARL) está fora de FL e só serve de exemplo metodológico.
F7 = rows('extracao_qp7.csv')
f7_nc = [x for x in F7 if not x['id'].startswith('C-')]
f7_fl = [x for x in f7_nc if x['escopo'] != 'MARL']
f7_fora = [x['id'] for x in f7_nc if x['escopo'] == 'MARL']
esc = Counter(x['escopo'] for x in f7_fl)
f7_simples = sum(x['simples'] == 'S' for x in f7_fl)
f7_teste = [x['id'] for x in f7_fl if x['teste_estat'] == 'S']
w(f'**Corpus:** {q7i_b + q7i_s} estudos Q7-I ({q7i_b} pela busca, {q7i_s} pelo snowballing) + 5 leituras canônicas do §13. Ficha por estudo em `extracao_qp7.csv` (consenso com o autor, adendo A15). '
  'Esses trabalhos **não fazem parte da população principal**: não entram nas contagens das QP1–QP6 e servem só como fundamentação externa.\n')
w(f'**Composição:** {len(F7) - len(f7_nc)} leituras canônicas; {len(f7_fl)} trabalhos sobre FL '
  f'({esc["FL robusto"]} em FL horizontal, {esc["VFL"]} em FL vertical, {esc["DFL"]} em FL descentralizado e {esc["pFL"]} em FL personalizado); '
  f'e {len(f7_fora)} fora de FL ({", ".join(f7_fora)}, MARL com agentes bizantinos, citado só como exemplo metodológico). '
  f'Entre os {len(f7_fl)} trabalhos sobre FL, {f7_simples} mostram um baseline simples igualando ou superando um método mais sofisticado, '
  f'e {len(f7_teste)} aplicam teste estatístico ({", ".join(f7_teste)}).\n')
w('**Em RL em geral (§13):** Henderson et al. (2018) mostram que a variância entre sementes e detalhes de implementação mudam conclusões em deep RL; '
  'Agarwal et al. (2021) mostram que com poucas execuções as estimativas pontuais enganam e defendem intervalos e IQM; Mania, Guy e Recht (2018) e '
  'Rajeswaran et al. (2017) mostram que busca aleatória simples e políticas lineares igualam deep RL em benchmarks de controle. '
  'Fora de FL, **V2-3771** (MARL resiliente para controle de formação, 20 sementes pareadas por célula, correção de Holm) mostra esse rigor aplicado a um método aprendido sob falhas bizantinas: '
  'sem ataque, a mediana (MAPPO-CWMed) tem a menor taxa de violações, e após Holm nenhuma vantagem do RS-MARL se sustenta. Não trata de defesa de agregação em FL e não sustenta conclusões sobre o corpus principal.\n')
w('**Em FL robusto:** as auditorias convergem em cinco armadilhas: (i) datasets fáceis (≈ 30% só MNIST) e ataques simplistas (≈ 40%) (Decoding FL Defenses); '
  '(ii) não-IID quebra agregações robustas e defesas de backdoor (Li et al. TBD; Breaking the Illusion; BackDFL; Comprehensive Evaluation); '
  '(iii) adversários adaptativos quebram defesas de tipo único (Hammer & Anvil; survey de adversários adaptativos); (iv) bugs e métricas incompletas (BackFed; TFLlib; DPArena; aeronáutico); '
  '(v) em cenários de produção, **defesas simples bastam** (Back to the Drawing Board) e escolhas simples, como taxa de aprendizado do servidor baixa ou compartilhamento parcial do modelo, já dão robustez (BackFed; pFL/Simple-Tuning).\n')
w('**Baselines simples relevantes para o Portão N:** ABSA (V2-0116), que troca entre agregação leve e robusta por detecção de anomalia **sem aprendizado**, '
  'fica a cerca de 1 p.p. da melhor defesa estática (Multi-Krum: 83,1 × 84,1 com 30% de maliciosos), com 38% menos computação e teste estatístico. '
  'Por não aprender, não pertence à população principal; é o análogo não aprendido de SARA, FedStrategist e DTAG-FL.\n')
w(f'**Lacuna:** nenhum dos {len(f7_fl)} trabalhos sobre FL avalia experimentalmente defesas por RL/bandit em FL. Só citam ou catalogam: Decoding FL Defenses (V2-4764) inclui o GAAvernor na auditoria de 50 defesas e mostra que ele cai nas mesmas armadilhas; a SoK veicular (V2-4840) cataloga o DRL-PBFL; V2-1365 cita o FairFL (MARL de equidade). O survey de adversários adaptativos (ePrint 2025/510) não cita nenhuma defesa por RL.\n')

# ------------------------------------------------------------------ lacunas e portões
w('## 8. Agenda de lacunas\n')
w(f'1. **Isolamento do aprendizado:** {c_cmp["nenhuma"]}/{len(E)} sem nenhuma comparação não aprendida; {c_cmp.get("aleatória", 0)} só contra aleatória; '
  f'{c_cmp.get("heurística (mesmo sinal)", 0)} contra política do mesmo sinal, nenhuma com teste estatístico.')
w('2. **Horizonte:** nenhum estudo mede o ganho do agente sobre a política não aprendida em função do nº de rodadas; orçamentos efetivos frequentemente ínfimos.')
w(f'3. **Ataques que conhecem o agente:** {qc(9, "S")}/{len(E)} com ataque adaptativo real (Meta-SG, AdaAggRL com RL-attack, BR-DFL, OptiGradTrust white-box, MAB-RFL com divisão dos maliciosos contra o ISA); nenhum ataque mira a política do agente (envenenamento da recompensa ou do estado), exceto a discussão teórica do InfRA-FL.')
w(f'4. **Rigor estatístico:** {qc(2, "S")}/{len(E)} com ≥ 3 sementes e variância; {qc(3, "S")}/{len(E)} com teste estatístico ou IC.')
w(f'5. **Vazamento:** {qc(1, "N")}/{len(E)} usam o conjunto de teste na recompensa, no estado, na seleção ou na verificação; {qc(1, "P")}/{len(E)} não dizem em que dados a recompensa é calculada ou usam amostras do pool de teste; 2 usam rótulos de malicioso na recompensa (V2-4728, V2-2103).')
w(f'6. **Privacidade do sinal:** {c_priv["dados no servidor"] + c_priv["conjunto de teste no servidor"]}/{len(E)} exigem dados no servidor ({c_priv["conjunto de teste no servidor"]} deles o próprio conjunto de teste) e 2 reconstroem dados do cliente; raramente discutido como custo.')
w(f'7. **Reprodutibilidade:** código em {qc(4, "S")}/{len(E)}.')
w('8. **Granularidade e memória:** nenhum estudo separa o efeito da granularidade (regra × peso por cliente) nem o da memória do efeito do aprendizado.\n')

w('## 9. Decisões internas (fora do artigo)\n')
w('### Portão N: **parcialmente mostrado**\n')
w('Critério (§2): "já mostrado" exige um estudo em que política não aprendida com o **mesmo sinal** iguala ou supera o agente **e** isso é apresentado como achado. '
  'Há 7 empates contra o mesmo sinal ou a ação fixa (V2-1179, V2-1327, V2-4789, V2-0350, V2-2103, V2-4540, V2-0111; V2-0383 empata contra oráculo). '
  'Em 2 os autores não reconhecem o empate: V2-1327 atribui o ganho aos pesos maiores no rótulo especial, e V2-4789 não comenta a Mediana nem o FedAvg sob ataque furtivo. '
  'Em 4 reconhecem, mas enquadram a igualdade como virtude do agente: V2-1179 ("essentially similar" ao φ = 1 fixo, porque o agente acha sozinho a melhor fixa de cada regime), '
  'V2-0350 (o local-only fixo supera no local, lido como troca entre personalização e generalização), '
  'V2-2103 (acurácia "identical with and without RL", com o RL reposicionado como consistência da detecção; mesmo sinal, 3 sementes) e V2-4540. '
  'O mais próximo é V2-4540: o escore por reputação, sobre o mesmo sinal, iguala ou supera o híbrido e o DRL puro em acurácia (Figs. 9–11), e os autores atribuem a robustez ao próprio escore; '
  'mas defendem o híbrido pela adaptabilidade e pela imprevisibilidade, sem testar ataque adaptativo, com execução única, só MNIST e 30 rodadas. '
  'Nenhum conclui que o aprendizado é dispensável. '
  'Em V2-0688 os autores reconhecem que a defesa vem da destilação e não do bandit, mas a comparação é com seleção aleatória, não com o mesmo sinal. '
  '→ **A novidade do artigo de auditoria se mantém.** Citar e diferenciar esses estudos; a contribuição é tornar o teste sistemático '
  '(mesmo sinal, várias sementes, estatística, horizonte, ataque adaptativo) e generalizá-lo entre métodos.\n')
w('### Portão R: requisitos e baselines obrigatórios para o GRADF-v2\n')
w('**Requisitos (lacunas a cobrir):** ataques adaptativos que conhecem a defesa e o agente (incluindo manipulação do sinal e on-off); não-IID forte (Dirichlet ≤ 0,1); '
  'avaliação com ≥ 5 sementes, IC e teste; sem uso de teste na recompensa; custo por rodada e exposição de privacidade declarados; análise de horizonte.\n')
w('**Baselines obrigatórios:**')
w('- não aprendidos no **mesmo espaço de ação e mesmo sinal**: ação fixa por regra/peso, limiar fixo sobre o sinal, seleção aleatória;')
w('- adaptativos não-RL: **ABSA** (V2-0116), **FedLAW** (SB-04, ICLR 2026), SAGE, BRITE-FL e FLIDS (ficha §9.2);')
w('- estáticos fortes: FedAvg, Median, Trimmed Mean, Krum/Multi-Krum, **FLTrust**, **FLAME**, Bulyan/RFA;')
w('- por RL/bandit, como concorrentes: **SARA**, **FedStrategist** (regra por rodada; o TARS, V2-1120, saiu por IC4 e só se cita como trabalho relacionado); **AdaAggRL**, **FedAA** (pesos); **MAB-RFL** (seleção);')
w('- ataques: LIE, Min-Max/Min-Sum (AGR-tailored), IPM, LMP, RL-attack (Li et al. 2022), on-off/pretense, backdoor (DBA, scaling).\n')

w('## 10. Limitações a declarar\n')
w('- Triagem da etapa 1 com dois revisores numa amostra de 20% (κ = 0,737; concordância 98,6%; PABAK 0,973; adendo A13). '
  'Extração da S1 (QP1–QP6) feita com assistência de IA (adendo A10) e conciliada com o fichamento independente do autor em 77 dos 78 estudos então incluídos (adendo A14); o V2-1120 saiu depois por IC4 (adendo A22).')
w('- Conferência do revisor 2 na etapa 2 (A16): concordância antes do consenso baixa — inclusão/exclusão κ = 0,35 (65,4%; PABAK 0,31; n = 52), '
  'categoria da QP2 κ = 0,14 (n = 52), qualidade κ = 0,15 (16 × 9) — em parte porque a conferência foi feita sem o texto completo; o consenso manteve todas as decisões do revisor 1. '
  'QP7 conciliada com o fichamento do autor (A15); qualidade não codificada em dobro além da amostra de 20%.')
w('- Protocolo não pré-registrado (A2); Web of Science não consultado; ACM sem busca em Keywords (A5).')
w('- 5 estudos da S1/QP7 sem acesso pela CAPES, 1 tese e 2 do snowballing não recuperados.')
w('- Campos "?" mantidos onde o texto não informa (sobretudo o dado da recompensa); nada foi inferido (§14).')

(R / 'slr_resultado.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('slr_resultado.md', len(out), 'linhas')
