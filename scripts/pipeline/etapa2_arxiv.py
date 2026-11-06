"""Etapa 2 (texto completo, §8.8), fichas §9.1/§10 e snowballing para trás (§8.9)
dos 21 PDFs do arXiv (triagem_v2/arXiv). Decisões por leitura manual do texto completo."""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'triagem_v2'


def write(name, header, rows):
    with open(OUT / name, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(name, len(rows))


# ---------------------------------------------------------------- etapa 2
ETAPA2 = [
    # id, arxiv, fluxo, etapa1, etapa2, motivo, versao_relacionada
    ('V2-4727', '2602.20003', 'S1', 'I', 'I',
     'PPO (GNN-RNN) por dispositivo escolhe vizinhos e pesos de agregação contra bizantinos em DFL', ''),
    ('V2-4728', '2510.01261', 'S1', 'I', 'I',
     'DQN ajusta confiança/peso por cliente contra poisoning/backdoor; compara com agente aleatório', ''),
    ('V2-4729', '2204.02654', 'S1', 'I', 'E-EC7',
     'Versão anterior de "Exploiting Gaussian Noise Variance for Dynamic Differential Poisoning in FL" (2025); '
     'manter a publicada. Obs.: Q-learning tabular avaliado só por convergência da recompensa (IC4 fraco)', 'V2-0530'),
    ('V2-4778', '2307.13716', 'S1', 'I', 'E-EC7',
     'Preprint de FedDRL publicado (2024, Scopus); manter a publicada', 'V2-2891'),
    ('V2-4789', '2507.14322', 'S1', 'I', 'I',
     'LinUCB escolhe a regra de agregação por rodada (FedAvg/Mediana/Krum) contra poisoning (QGS Q5)', ''),
    ('V2-4812', '2410.17431', 'S1', 'I', 'I',
     'Meta-RL (TD3+Reptile) em jogo de Stackelberg bayesiano ajusta parâmetros de defesa contra ataques adaptativos e mistos. '
     'Versões anteriores (2306.13800, 2306.13273) ficam absorvidas por EC7', ''),
    ('V2-4818', '2507.23638', 'S1', 'I', 'E-EC7',
     'Versão anterior do artigo publicado na Scientific Reports (2026), que tem ablação do RL e 3 sementes; manter a publicada', 'V2-2103'),
    ('V2-4731', '2302.07173', 'QP7', 'Q7-I', 'Q7-I',
     'Estudo experimental de 8 agregações robustas x 5 ataques; todas falham sob não-IID, algumas sem ataque (IEEE TBD 2024)', ''),
    ('V2-4735', '2608.21137', 'QP7', 'Q7-D', 'Q7-I',
     'BackDFL: benchmark de backdoor em DFL; defesas falham com 15% de maliciosos e variam com a topologia', ''),
    ('V2-4739', '2507.04903', 'QP7', 'Q7-D', 'Q7-I',
     'BackFed: benchmark padronizado; bugs em códigos oficiais inflam ataques; LR do servidor baixo e mais amostragem de '
     'clientes (escolhas simples, não aprendidas) aumentam a robustez', ''),
    ('V2-4743', '2509.05833', 'QP7', 'Q7-D', 'Q7-E',
     'Benchmark para mercados de gradiente; escopo tangencial (não é defesa de FL robusto nem prática de avaliação)', ''),
    ('V2-4753', '2505.24802', 'QP7', 'Q7-D', 'Q7-E',
     'ByzFL: biblioteca, sem achados empíricos sobre prática de avaliação (guardar como recurso para o GRADF)', ''),
    ('V2-4761', '2409.13004', 'QP7', 'Q7-D', 'Q7-E',
     'Capítulo de livro de caráter tutorial (vazamento e poisoning); observações empíricas ilustrativas, '
     'sem contribuição sobre prática de avaliação', ''),
    ('V2-4764', '2502.05211', 'QP7', 'Q7-I', 'Q7-I',
     'Decoding FL Defenses: 50 artigos de defesa auditados; 6 armadilhas (30% só MNIST, 40% ataques simplistas); reavaliação de 3 defesas', ''),
    ('V2-4797', '2509.08089', 'QP7', 'Q7-D', 'Q7-I',
     'Hammer and Anvil: adversário adaptativo de informação completa quebra defesas de tipo único e combinações não principiadas', ''),
    ('V2-4831', '2608.04045', 'QP7', 'Q7-D', 'Q7-I',
     'Avaliação controlada de 4 agregações x 5 ataques em prognóstico aeronáutico; acurácia limpa não detecta backdoor (ASR 94,9%)', ''),
    ('V2-4839', '2502.03801', 'QP7', 'Q7-I', 'Q7-I',
     'SoK: benchmark unificado de 17 defesas x 15 ataques (DPA e MPA)', ''),
    ('V2-4840', '2607.10914', 'QP7', 'Q7-D', 'Q7-I',
     'SoK FL-IDS veicular: auditoria de 60+ artigos; armadilhas (IID artificial, benchmarks triviais, avaliação adversarial fraca)', ''),
    ('V2-4856', '2503.23288', 'QP7', 'Q7-D', 'Q7-E',
     'GeminiGuard: propõe defesa não-RL; o benchmark sob não-IID só motiva o método (na S1 seria E-IC3)', ''),
    ('V2-4857', '2608.12962', 'QP7', 'Q7-D', 'Q7-I',
     'Backdoor em VFL: achados publicados não se sustentam em condições realistas; lacuna entre pesquisa e prática', ''),
    ('V2-4859', '2603.20615', 'QP7', 'Q7-D', 'Q7-I',
     'Medição de segurança de FL (TFLlib): modelos de ameaça idealizados, heterogeneidade híbrida omitida e métricas incompletas distorcem o risco', ''),
]
write('etapa2_arxiv.csv',
      ['id', 'arxiv', 'fluxo', 'etapa1_decisao', 'etapa2_decisao', 'etapa2_motivo', 'versao_relacionada',
       'conferido_r2', 'via_snowballing', 'origem_snowballing'],
      [r + ('N', 'N', '') for r in ETAPA2])

# ---------------------------------------------------------------- §9.1
F91 = ['id', 'titulo', 'autores', 'ano', 'venue', 'doi_arxiv', 'revisado_por_pares', 'dominio', 'cenario_fl',
       'algoritmo', 'estado', 'acao', 'granularidade', 'recompensa', 'vazamento_teste', 'modo', 'orcamento',
       'analise_horizonte', 'sinal', 'memoria', 'ablacoes', 'privacidade_sinal', 'custo',
       'comparacao_nao_aprendida', 'resultado_comparacao', 'discutido_como_achado', 'ataques', 'ataque_adaptativo',
       'datasets_modelos', 'clientes', 'baselines_estaticos', 'sementes_estatistica', 'codigo', 'notas']
EXTR = [
    ['V2-4727', 'A Secure and Private Distributed Bayesian Federated Learning Design',
     'Yang N.; Wang S.; Yang Z.; Chen M.; Yin C.; Huang K.', 2026, 'arXiv', 'arXiv:2602.20003', 'N',
     'geral/benchmark', 'DFL (sem servidor), cross-device, horizontal',
     'PPO (GNN + RNN), um agente por dispositivo',
     'divergência (KL) entre prior e posteriores recebidos dos vizinhos + pesos históricos + posições; GNN sobre o grafo (invariante a permutação via GNN)',
     'contínua: probabilidades de conexão com vizinhos + pesos de agregação',
     'peso/cliente + selecao/cliente (vizinhos)',
     '-erro - soma B*A (B = identificação bizantina por limiar) - termo de privacidade; dado: perdas locais/validação local (não detalhado)',
     '?', 'pré-treino offline (dados históricos)', 'não reportado (passos, episódios e taxas ausentes)', 'N',
     'divergência bayesiana entre posteriores', 'S: pesos históricos no estado (RNN)', 'não há ablação do agente',
     'só updates (posteriores); ataque de privacidade DLG avaliado', 'N',
     'aleatória (conexão aleatória)', 'agente supera conexão aleatória; sem Δ contra heurística de limiar com o mesmo sinal; sem significância', 'N',
     'bizantino de modelo aleatório; DLG (privacidade)', 'N',
     'MNIST, EMNIST, CIFAR-10', '6-12 dispositivos; % de bizantinos variada', 'THDFL, PT-DFL (criptográfico)',
     'não reportado', 'N',
     'Ataque trivial (modelo aleatório): a própria regra de limiar B já o detecta, então o ganho do RL não é isolado'],
    ['V2-4728', 'Adaptive Federated Learning Defences via Trust-Aware Deep Q-Networks', 'Palit V.', 2025, 'arXiv',
     'arXiv:2510.01261', 'N', 'geral/benchmark', 'cross-device, horizontal',
     'DQN',
     'por cliente: cosseno ao global, desvio da norma à mediana, impacto na validação + crença bayesiana; concatenado (não invariante a permutação)',
     'discreta {aumentar, reduzir, manter} confiança por cliente', 'peso/cliente',
     'acurácia de validação + "trust accuracy" (penalizar maliciosos corretamente; exige rótulo de malicioso) - custo - ASR; dado: validação no servidor + rótulos de ground truth',
     '? (usa rótulos privilegiados de malicioso, não o teste)', 'online durante o FL',
     '50 rodadas; ε 1->0,01 em 5.000 passos (incompatível com 50 rodadas x 10 clientes); replay 10k; lr 1e-3; atualizações efetivas não calculáveis',
     'N (curvas por rodada, sem ganho vs horizonte)', 'cosseno, norma, impacto na validação',
     'S: crença bayesiana + confiança multiplicativa',
     'orçamento de sinal (Full / No-Validation / Directional): cai sem validação',
     'conjunto de validação no servidor', 'N',
     'aleatória (+ Linear-Q e PG, aprendidos)',
     'DQN 61,48±4,09 vs aleatório 16,28±3,60 de acurácia; ASR aleatório 36 vs DQN 41 (DQN pior em ASR); baselines perto do acaso; regra de confiança sem DQN (mesmo sinal) não testada', 'N',
     'backdoor (varreduras de sign-flip, gradient-push e colusão no apêndice)', 'N',
     'CIFAR-10 (CNN)', '10 clientes, 5 por rodada, 20% maliciosos, Dirichlet 0,5', 'nenhum estático reportado',
     '5 sementes, desvio padrão; sem teste', 'N (usa AIJack)',
     'Recompensa usa rótulos de malicioso (oráculo). A comparação só contra aleatório infla o ganho do aprendizado'],
    ['V2-4789', 'FedStrategist: A Meta-Learning Framework for Adaptive and Robust Aggregation in Federated Learning',
     'Haque M.R.; Kamal A.R.M.; Hossain M.A.', 2025, 'arXiv', 'arXiv:2507.14322', 'N',
     'geral/benchmark', 'cross-silo (participação total), horizontal',
     'bandit (LinUCB)',
     'R^3: variância das normas, cosseno médio par a par, norma média dos updates; invariante a permutação',
     'discreta, 3 braços {FedAvg, Mediana, Krum}', 'regra/rodada',
     'ΔAcc em validação proxy no servidor - λ*custo', 'N', 'online durante o FL',
     '50-75 rodadas = 50-75 atualizações do LinUCB; α do UCB não localizado', 'N',
     'estatísticas de norma e cosseno', 'N', 'só λ (o agente escolhe FedAvg em 92-94% das rodadas para todo λ)',
     'conjunto de validação no servidor', 'S (custo por regra entra na recompensa)',
     'fixa (cada braço sozinho)',
     'α=0,1: 28,73 vs Mediana 27,38; ataque furtivo: 38,82 vs FedAvg 39,43 (fixa vence); α=10: 44,31 vs Mediana 44,39 (texto diz Krum, tabela diz Mediana); 1 execução', 'N',
     'scaling x5 personalizado; furtivo com norma casada', 'P (furtivo casa a norma, mas não otimiza contra o agente)',
     'CIFAR-10', '20 clientes, 5 maliciosos, participação total', 'FedAvg, Mediana, Krum', '1 execução aparente; sem variância',
     'S (GitHub/Zenodo 10.5281/zenodo.16068113)',
     'QGS Q5. A tabela de política contradiz a alegação de controlabilidade e a política fixa empata ou vence sem discussão: evidência para o Portão N ("parcialmente mostrado")'],
    ['V2-4812', 'Meta Stackelberg Game: Robust Federated Learning against Adaptive and Mixed Poisoning Attacks',
     'Li T.; Li H.; Pan Y.; Xu T.; Zheng Z.; Zhu Q.', 2024, 'arXiv', 'arXiv:2410.17431', 'N',
     'geral/benchmark', 'cross-device, horizontal',
     'TD3 + Reptile (meta-RL) em jogo de Stackelberg bayesiano',
     'últimas duas camadas ocultas do modelo global', 'contínua 3-D: limite de norma, taxa do trimmed mean, parâmetro NeuroClip/Prun',
     'parametro',
     '-perda após pós-treino, em dados autogerados (root 100/200 + cGAN/difusão + inversão de gradiente dos updates + Neural Cleanse)',
     'N', 'ambos (pré-treino offline + adaptação online)',
     'pré-treino T=100 x K=10 ataques x H=200/500 passos, 10 passos TD3 cada (~10^4 atualizações); online 100 passos TD3; FL 300 rodadas',
     'N', 'perda em dados autogerados', 'N (política markoviana sobre o estado)',
     'pré-treino apenas / online apenas (Tab. 6); viés do root data',
     'dataset raiz + reconstrução de dados do cliente (inversão de gradiente)', 'N',
     'fixa (parâmetros fixos afinados à mão, ClipMed, FLTrust+NC; Tab. 8)',
     'agente vence; ex.: backdoor DBA 0,28 vs 0,99; sem variância', 'S',
     'IPM, LMP, BFL, DBA (não adaptativos); RL e BRL (adaptativos, Tab. 3)', 'S (atacantes RL e BRL treinados contra a defesa)',
     'MNIST, CIFAR-10', '100 clientes, 10% por rodada; % de maliciosos por ataque', 'FedAvg, Trimmed Mean, FLTrust, ClipMed, Krum, CRFL, NeuroClip, Prun',
     'sementes fixas, 1 execução, sem variância', 'N',
     'Único do lote com ataque adaptativo real e comparação com política fixa afinada. Reconstruir dados de clientes é um custo de privacidade relevante para a QP5'],
]
write('extracao_principal.csv', F91, EXTR)

# ---------------------------------------------------------------- §10
QA = [  # id, QA1..QA9 (S/P/N), justificativa
    ('V2-4727', 'N', 'N', 'N', 'N', 'P', 'P', 'N', 'N', 'N',
     'QA1 não determinável (dado da recompensa não descrito); QA5 só conexão aleatória; sem sementes, código ou orçamento'),
    ('V2-4728', 'P', 'S', 'N', 'N', 'P', 'P', 'P', 'N', 'N',
     'QA1 usa rótulos privilegiados; QA5 só aleatória; QA7 ε inconsistente com 50 rodadas; sem estáticos'),
    ('V2-4789', 'S', 'N', 'N', 'S', 'S', 'P', 'P', 'P', 'P',
     'QA5 braços fixos; QA6 ataques personalizados; QA8 Mediana e Krum, sem FLTrust; QA9 furtivo parcial'),
    ('V2-4812', 'S', 'N', 'N', 'N', 'S', 'P', 'S', 'S', 'S',
     'QA2 execução única; QA5 Tab. 6 e 8; QA8 FLTrust + Trimmed Mean; QA9 atacantes RL adaptativos'),
]
val = {'S': 1, 'P': 0.5, 'N': 0}
rows = []
for r in QA:
    sc = r[1:10]
    rows.append((r[0],) + sc + (sum(val[x] for x in sc),) + ('',) * 10 + (r[10],))
write('qualidade.csv',
      ['id'] + [f'qa{i}_r1' for i in range(1, 10)] + ['total_r1'] + [f'qa{i}_r2' for i in range(1, 10)] + ['total_r2', 'justificativa_r1'],
      rows)

# ---------------------------------------------------------------- §8.9
SNOW = [
    # referencia, origem, direcao, status_base, decisao_titulo, motivo
    ('Wan W. et al. MAB-RFL: A multi-armed bandit based robust federated learning framework. JPDC 156:14-24, 2021',
     'V2-4789', 'trás', 'V2-4339 (Scopus; é o artigo do IJCAI 2022 "Shielding Federated Learning")', '-',
     'Citação do FedStrategist provavelmente trocada (JPDC); o MAB-RFL é o V2-4339, já lido no lote 2 (I)'),
    ('Rjoub G. et al. Trust-driven reinforcement selection strategy for federated learning on IoT devices. Computing, 2022',
     'V2-4778', 'trás', 'NÃO ENCONTRADO', 'D', 'RL de seleção baseada em confiança; verificar se há adversário'),
    ('Rjoub G. et al. Trust-augmented deep reinforcement learning for federated learning client selection. Information Systems Frontiers, 2022',
     'V2-4778', 'trás', 'NÃO ENCONTRADO', 'D', 'DRL de seleção por confiança; verificar se há adversário'),
    ('Zhang W. et al. R2Fed: Resilient Reinforcement Federated Learning for Industrial Applications. IEEE TII, 2023',
     'V2-4778', 'trás', 'V2-0945 / V2-3990 (E-EC4 por regra)', 'D',
     'Erro da regra: RL pondera modelos de clientes e é avaliado contra ataques (não é RL federado). Reclassificar para D e ler. '
     'V2-0945 e V2-3990 são duplicatas (o "$^{2}$" quebrou a deduplicação)'),
    ('Pan Y. et al. Privacy-preserving Byzantine-robust FL via DRL in vehicular networks (DRL-PBFL). IEEE TVT, 2025',
     'V2-4840', 'trás', 'V2-0918 (I; já na lista)', '-', 'Já na leitura'),
    ('Hu C. et al. Adapting Aggregation Rule for Robust FL under Dynamic Attacks (SARA). SEAMS 2025',
     'V2-4789', 'trás', 'V2-0111 (I; já na lista)', '-', 'Já na leitura'),
    ('FedAA: a reinforcement learning perspective on adaptive aggregation (2025)',
     'V2-4818', 'trás', 'V2-1254 (I; QGS Q2)', '-', 'Já na leitura'),
    ('Li H. et al. Learning to attack FL: model-based RL attack framework. NeurIPS 2022',
     'V2-4778 / V2-4812', 'trás', 'V2-1304 (E-EC1)', '-', 'Atacante RL; exclusão mantida'),
    ('Li H. et al. Learning to backdoor federated learning, 2023', 'V2-4812', 'trás', 'V2-4805 (E-EC1)', '-', 'Exclusão mantida'),
    ('Wang H. et al. Optimizing FL on non-IID data with RL (FAVOR). INFOCOM 2020', 'V2-4778', 'trás', 'V2-0878', 'E-EC3', 'Eficiência/não-IID, sem adversário'),
    ('Sun Y. et al. A fair federated learning framework with reinforcement learning (PG-FFL). IJCNN 2022', 'V2-4778', 'trás', 'NÃO ENCONTRADO', 'E-EC3', 'Justiça, sem adversário'),
    ('Cho Y.J. et al. UCB-CS: bandit-based communication-efficient client selection. ICASSP 2023', 'V2-4789', 'trás', 'NÃO ENCONTRADO', 'E-EC3', 'Eficiência de comunicação'),
    ('Sinha A. et al. FedCostAware: cost-aware FL on the cloud, 2025', 'V2-4789', 'trás', 'NÃO ENCONTRADO', 'E-IC2', 'Custo de nuvem, sem defesa'),
    ('Anwar A., Raychowdhury A. Multi-task federated reinforcement learning with adversaries, 2021', 'V2-4728', 'trás', 'NÃO ENCONTRADO', 'E-EC4', 'RL federado'),
    ('Xu X., Lyu L. A reputation mechanism is all you need: collaborative fairness and adversarial robustness in FL, 2021',
     'V2-4728', 'trás', 'NÃO ENCONTRADO', 'E-IC3', 'Reputação sem RL (candidato à ficha §9.2 se contar como adaptativo não-RL)'),
    ('Yan Z. et al. Reinforcement learning guided geometric median for robust FL (RL-GM). "IEEE Trans. on Machine Learning" 18(4), 2024',
     'V2-4818', 'trás', 'NÃO ENCONTRADO', 'não localizável', 'Periódico inexistente; referência provavelmente espúria (reforça a baixa qualidade do OptiGradTrust)'),
    ('Nie X. et al. Mobility-aware cooperative caching in IoVs based on secure asynchronous federated and DRL. IEEE IoTJ 2025',
     'V2-4840', 'trás', 'V2-0822 (E-IC3)', '-', 'Exclusão mantida'),
    ('Li T. et al. A First Order Meta Stackelberg Method for Robust Federated Learning (arXiv 2306.13800; ICML-W 2023) e relatório técnico 2306.13273',
     'V2-4812', 'trás (versão)', 'NÃO ENCONTRADO', 'E-EC7', 'Versões anteriores do Meta-SG; manter 2410.17431. Confirmar os IDs'),
    ('Rodríguez-Barroso N. et al. Survey on FL threats: taxonomy, experimental study and challenges. Information Fusion, 2023',
     'V2-4812 / V2-4764', 'trás', 'NÃO ENCONTRADO', 'Q7-D', 'Survey com estudo experimental de defesas'),
    ('Bellachia A.A. et al. SoK: Understanding backdoor attacks & defenses in FL. Expert Systems with Applications, 2026',
     'V2-4735', 'trás', 'NÃO ENCONTRADO', 'Q7-D', 'SoK de backdoor; verificar se discute prática de avaliação'),
    ('Sharma G. et al. SoK: Systematizing attack studies in FL - from sparseness to completeness. AsiaCCS 2023',
     'V2-4839', 'trás', 'NÃO ENCONTRADO', 'Q7-D', 'SoK de ataques; tangencial'),
    ('Khan M.A. et al. On the pitfalls of security evaluation of robust FL. IEEE SPW 2023', 'vários', 'trás', 'V2-0870 (Q7-I)', '-', 'Já na leitura'),
    ('Shejwalkar V. et al. Back to the drawing board. IEEE S&P 2022', 'vários', 'trás', 'V2-0252 (Q7-I)', '-', 'Já na leitura'),
    ('Almutairi S., Barnawi A. Model poisoning attacks in FL for autonomous vehicles: a benchmark study. Results in Eng. 2024',
     'V2-4840', 'trás', 'V2-1403 (Q7-I)', '-', 'Já na leitura'),
    ('Federated Client Selection under Partial Visibility: A POMDP Approach with Spatio-Temporal Attention (arXiv 2605.11752)',
     'V2-4728', 'frente', 'NÃO ENCONTRADO', 'E-EC3', 'RL de seleção por heterogeneidade, sem adversário'),
    ('FedDive: escaping local minima through divergence-rewarded exploration in FL (KAIS 2025, 10.1007/s10115-025-02623-y)',
     'V2-4789', 'frente', 'NÃO ENCONTRADO', 'D', 'Sem resumo no Semantic Scholar; conferir se há RL e adversário'),
    ('Secure-CHG: robust and fair FL via hybrid defense and contribution-aware trust (arXiv 2606.31066)',
     'V2-4812', 'frente', 'NÃO ENCONTRADO', 'E-IC3', 'Defesa híbrida sem RL'),
    ('FedSecure-Chain: robust and verifiable FL against poisoning in e-health (Front. Public Health 2026)',
     'V2-4789', 'frente', 'V2-1605', '-', 'Já triado'),
]
write('snowball_arxiv.csv', ['referencia', 'citado_em_ou_cita', 'direcao', 'status_base', 'decisao_titulo', 'motivo'], SNOW)
