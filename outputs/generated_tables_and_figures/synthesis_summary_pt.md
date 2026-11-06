# Resultado da revisão sistemática: defesas de FL com RL/bandits e o que o aprendizado contribui

**Protocolo:** `slr_protocolo_v1.1.md` (com os adendos A1–A17 do §15.3). **Busca:** 2026-09-28. **Revisores:** revisor 1 (autor) em todas as etapas; revisor 2 na calibração e numa amostra cega de 20% da etapa 1 (A12–A13) e na conferência da etapa 2, da QP2 e de 20% da qualidade (A16).  
**Arquivos-base:** `triagem_v2/` → `registros.csv`, `triagem_final.csv`, `etapa2_arxiv.csv`, `etapa2_lote2.csv`, `extracao_principal.csv`, `qualidade.csv`, `extracao_adaptativo_nao_rl.csv`, `extracao_qp7.csv`, `revisao_extracao.tsv`, `revisor2/consenso_etapa2.csv`; log em `triagem/log_buscas.csv`.

## 1. Fluxo PRISMA 2020 (§11.4)

| etapa | S1 (síntese principal) | QP7 |
|---|---|---|
| Registros identificados (brutos, todas as bases e strings) | 6.580 (IEEE 1.202; ACM 268; Scopus 4.875; arXiv 235) | (mesma base) |
| Duplicatas removidas | 1.717 | |
| Registros únicos triados na etapa 1 | 4.863 | 4.863 |
| Excluídos na etapa 1 | ver `prisma_v2.md` (E-IC1 2.910; E-EC4 244; E-IC2 222; E-EC3 221; E-IC3 119; E-EC5 92; E-PER 67; E-EC1 20; E-IC4 6; E-EC6 3) | Q7-E 786 |
| Para a ficha §9.2 já na etapa 1 (E-EC2) | 26 | |
| Texto completo buscado (via busca) | 124 | 40 |
| Não recuperados | 4 (sem acesso CAPES) | 2 (1 sem acesso; 1 tese → E-IC5) |
| Texto completo avaliado (via busca) | 120 | 38 |
| Excluídos na etapa 2 | 45: E-IC3 18, E-IC2 8, E-EC7 6, E-EC2 4, E-EC3 2, E-EC4 2, E-IC4 2, E-IC1 1, E-EC6 1, E-EC1 1 (E-EC2 → §9.2) | 13 (Q7-E) |
| **Incluídos via busca** | **75** | **25** |
| Snowballing: avaliados / não recuperados | 5 / 1 (FedDive) | 5 / 1 (Zhang et al. 2024) |
| **Incluídos via snowballing** | **2** (R2Fed, FedCHO) | **4** |
| Leituras canônicas (§13, inclusão direta) | — | **5** |
| **Total incluído** | **77** | **34** |

Versões anteriores excluídas por EC7 (mantida a publicada): OptiGradTrust (V2-4818 → V2-2103), FedDRL (V2-4778 → V2-2891), rDP (V2-4729 → V2-0530), DeSMP (V2-0423 → V2-0530), RAFRL (V2-1002 → V2-1001), DRL-trust IWCMC (V2-1038 → V2-1102). Ficha §9.2 (adaptativos não-RL lidos no texto completo): 7.

## 2. Mapeamento (QP1 e QP4)

**77 estudos**; 73 revisados por pares e 4 preprints. Por ano: 2021: 2, 2022: 3, 2023: 7, 2024: 15, 2025: 22, 2026: 27, 2027: 1. A área é recente: 2/3 dos estudos são de 2025–2026.

| eixo | distribuição |
|---|---|
| algoritmo | DQN/DDQN 18; DDPG/TD3/SAC 16; bandit 15; PG/ator-crítico 13; Q-learning tabular 6; outro 5; MARL 4 |
| granularidade | selecao/cliente 45; peso/cliente 19; parametro 10; regra/rodada 3 |
| memória entre rodadas | S 49; N 27; ? 1 (reputação, confiança acumulada, posteriores, LSTM/ESN) |
| domínio | geral/benchmark 31; IoT/IoMT 17; outro 14; veicular 10; saúde 4; finanças 1 |
| modo de aprendizado | online 68; com pré-treino/offline 9 |

**Leitura:** a forma dominante é **seleção de clientes por agente** (45/77), seguida de **pesos por cliente** (19). A "escolha da regra de agregação por rodada", que motiva o artigo de auditoria (AdaAggRL no QGS, SARA, FedStrategist, DTAG-FL; o TARS saiu por IC4, A22), é minoritária (3). Em quase todos os estudos o agente é acoplado a um **sinal de detecção próprio** (reputação, cosseno/distância, anomalia por autoencoder, Shapley, acurácia em validação); em 49 há memória explícita entre rodadas. Por isso, na maioria, o que o agente aprende é **como usar um escore que já separa bons e maus clientes**, e é exatamente essa separação que um limiar fixo sobre o mesmo escore também explora.

**Ablações por eixo (QP4)** — contagem de estudos que isolam cada componente (texto de `ablacoes` e `comparacao_nao_aprendida`):

- aprendizado (alguma política não aprendida ou remoção do agente): **45**;
- sinal: **11** (V2-4728, V2-1231, V2-0634, V2-3555, V2-2188, V2-2103, V2-0495, V2-3243, V2-1483, V2-4812, SB-03);
- memória: **0** dedicadas; 2 indiretas, que removem a confiança acumulada junto com outras coisas (V2-3555, V2-2188);
- granularidade: **0**. Nenhum estudo compara, com o mesmo sinal, decidir uma regra por rodada contra decidir pesos por cliente.

## 3. QP2 (central): comparação com políticas não aprendidas

| natureza da comparação | nº de estudos |
|---|---|
| nenhuma | 32 |
| aleatória | 19 |
| parcial/ablação | 4 |
| fixa | 9 |
| heurística (mesmo sinal) | 6 |
| heurística (outro sinal) | 6 |
| oráculo | 1 |

Tabela de todos os estudos com alguma comparação não aprendida (ordem: fixa, mesmo sinal, outro sinal, aleatória, parcial, oráculo):

| id | estudo | ano | comparação | resultado | discutido? |
|---|---|---|---|---|---|
| V2-0111 | Adapting Aggregation Rule for Robust Federat… | 2025 | fixa (cada regra isolada: Krum, TrimmedMean, Median) + oráculo (melho… | empata com a melhor regra fixa: comparável à Median no ataque periódico (MNIST e CIFAR-10) e ao Krum no ataque de fingimento no MNIST; supera o Krum … | S |
| V2-0160 | Agentic AI-Driven Federated Unlearning for S… | 2026 | fixa (política estática) + ablação "sem agente" | agente reduz ASR vs estática; ASR 0,24 vs FedEraser 0,58 | S |
| V2-0350 | Cooperative Multi-Agent Reinforcement Learni… | 2026 | fixa (Ditto com λ = 0,5 fixo; local-only, λ = 0; FedAvg); treino cent… | Tab. 1: o local-only (λ = 0 fixo) supera o pFedMARL em F1 nos três cenários (QS L 0,84 × 0,77; LS L 0,92 × 0,87; CS L 0,98 × 0,96) e iguala o MSE; Ta… | S |
| V2-1130 | TrustFed: A Reliable Federated Learning Fram… | 2025 | fixa (MAO e PAO: auditar todos com um só método) + aleatória | CJR > 0,9 (HiAudit/DRL-ASS) × 0,55-0,60 (MAO, auditoria fixa só do modelo); PAO (auditoria fixa de parâmetros) mantém RE alto e constante; aleatória … | S |
| V2-1179 | A Secure and Fair Client Selection Based on … | 2024 | fixa (φ=1 e φ=0) | empate: sob ataque fraco, DDPG × φ = 1 fixo é 0,941 × 0,923 e 0,960 × 0,944 com k = 5, mas 0,949 × 0,938 e 0,966 × 0,955 com k = 10 (+1,1 p.p.); sob … | S |
| V2-1327 | Preventing harm to the rare in combating the… | 2024 | fixa (peso fixo 1/6 no mesmo framework de filtragem e votação) | sob envenenamento, fixo ≈ DRL (MNIST 89,70 vs 90,79/90,60; CIFAR 69,05 vs 70,70/71,29); o ganho do DRL está nos rótulos raros (2,67 vs 66-74) | S |
| V2-2573 | DTAG-FL: A Digital-Twin, Attention-Graph, an… | 2026 | fixa (regras fixas em "mundos paralelos") | DTAG-FL supera regras fixas; o PPO alterna regras | S |
| V2-4789 | FedStrategist: A Meta-Learning Framework for… | 2025 | fixa (cada braço sozinho) | α=0,1: 28,73 vs Mediana 27,38; ataque furtivo: 38,82 vs FedAvg 39,43 (fixa vence); α=10: 44,31 vs Mediana 44,39 (texto diz Krum, tabela diz Mediana);… | S |
| V2-4812 | Meta Stackelberg Game: Robust Federated Lear… | 2024 | fixa (parâmetros fixos afinados à mão, ClipMed, FLTrust+NC; Tab. 8) | agente vence; ex.: backdoor DBA 0,28 vs 0,99; sem variância | S |
| SB-03 | FedCHO: Closed-Loop Hierarchical Orchestrati… | 2026 | heurística com o mesmo sinal (similarity-weighted = ramo heurístico i… | DRAP 61,64±1,14 vs similarity 58,47±0,98 vs trust 55,83 (CIFAR-10, α=0,05, 25%) | S |
| V2-0351 | Cooperative Physical Layer Authentication Wi… | 2023 | heurística com o mesmo sinal (seleção direta: combinação de maior rep… | vitória estreita contra a seleção direta (taxa de erro, Fig. 9, L = 6, iterações 35–45: K = 8 ~0,03 × ~0,04; K = 10 ~0,035 × ~0,07; K = 15 ~0,06 × ~0… | S |
| V2-0973 | Reputation-Aware Multi-Agent DRL for Secure … | 2023 | heurística com o mesmo sinal (limiar estático de reputação = 0,5) | acurácia 0,96 vs 0,92 (estático) vs 0,91 (FedAvg) | S |
| V2-1102 | Toward Secure Federated Learning for IoT Usi… | 2022 | heurística com o mesmo sinal (SLM com limiar estático 0,5) | vitória estreita: o DDPG supera o SLM com limiar estático em todos os regimes (k = 5: 0,89 × 0,86; k = 10: 0,68 × 0,62; Fig. 4, cinco taxas de envene… | S |
| V2-2103 | Byzantine robust federated learning for hete… | 2026 | heurística com o mesmo sinal (regra fixa: pesos iguais 1/6 nos 6 sina… | acurácia final igual nas três condições (RL 64,32; sem RL 64,32; regra 64,35); F1 de detecção pós-ataque RL 61,7 vs regra 36,4, mas sem RL (só atençã… | S |
| V2-4540 | Towards a distributed nodes selection mechan… | 2024 | heurística com o mesmo sinal (método por escore) | empate: o escore iguala ou supera o híbrido na acurácia (Figs. 9–11, rodadas finais; escalabilidade ~93 × ~95; robustez, 60% desonestos, ~88 × ~87,5;… | S |
| V2-0542 | FairRoP: Robust Client Selection Scheme for … | 2026 | heurística com outro sinal (Pow-d: perda local) + aleatória (Random) | FairRoP > Random em justiça e robustez; Pow-d colapsa quando atacantes inflam a perda | S |
| V2-0835 | Multi-Job Hierarchical Federated Learning fo… | 2025 | heurística com outro sinal (gulosa: 30% de UAVs com maior capacidade … | DQN atinge o alvo em 22/42/46 rodadas, mais rápido que aleatória e gulosa; tempo total −56,6% vs aleatória e −29,1% vs gulosa | S |
| V2-1140 | Two-Stage Client Selection for Federated Lea… | 2024 | heurística com outro sinal (Pow-d: perda local) + aleatória (amostrag… | converge mais rápido com 50-80% de free-riders | S |
| V2-1199 | An Enhanced Combinatorial Contextual Neural … | 2024 | heurística com outro sinal (Pow-d: perda local) + aleatória (FedAvg) | SRS ~99 vs Random ~59; Pow-d chega a SRS 0% no ataque Tipo 1 (escolhe só maliciosos) | S |
| V2-3215 | InfRA-FL: Information-Driven Robust Federate… | 2026 | heurística com outro sinal (Power-of-Choice: perda local) + aleatória… | CIFAR-10, 20%: 65,22 vs FedAvg 50,87 vs Pow-d 50,21; convergência no MNIST 10-13 vs 39-45 rodadas (sem RL: 45) | S |
| V2-4059 | Reinforcement Learning-Driven Adaptive Aggre… | 2025 | heurística com outro sinal (AMA: pesos estáticos sobre confiança, qua… | 96,5% vs AMA 95,2% sem ataque; 20% de envenenamento: 93,2% vs AMA 72,0%; os autores atribuem a robustez ao f_i | S |
| V2-0391 | Deep Learning based Moving Target Defence fo… | 2025 | aleatória (RND-MTD bloqueia 2 ou 4 aleatórios) | MTD-FL > RND-MTD em acurácia e exclusão | S |
| V2-0550 | Fed-Reputed: Reputation-Aware Client Selecti… | 2026 | aleatória (RS) | +37,86% vs RS (MNIST, 40% mal.) | S |
| V2-0634 | FedSAP: Secure Federated Learning in SDN-IoT… | 2024 | aleatória (FedAvg com seleção aleatória de nós) + ablação sem PSA | 20% mal.: 91% vs 85%; 50%: 84% vs 69% (local 52%); sem PSA 73% | S |
| V2-0688 | General Backdoor-Resilient Federated Learnin… | 2026 | aleatória (Random KD: professores aleatórios, ablação do MAB) | ASR igual com e sem MAB; CA +2,8 a 3,9 p.p. com MAB só em Non-IID | S |
| V2-0837 | Multi-Model based Federated Learning Against… | 2024 | aleatória (MM-FL-RND); a estrutura FL-GRU 28/32 mantida sem mutação n… | sob ataque, a estrutura fixa cai de 0,92 para 0,15 (época 6); aleatória +0,09; DRL ~0,85-0,92 | S |
| V2-0940 | Quality-aware Client Selection and Resource … | 2024 | aleatória (Random; a referência "Fixed" é canal fixo com seleção alea… | seleciona 1,35%/3,25% de atacados vs ~50% (Random, Fixed) | S |
| V2-1012 | Robust Peer-to-Peer Federated Learning With … | 2026 | aleatória | P2P-FedDRL > Random e CBE3 nos 6 ataques | S |
| V2-1126 | TrustBandit: Optimizing Client Selection for… | 2024 | aleatória (Random CS) | seleciona clientes confiáveis em 94,2% vs aleatória | S |
| V2-1261 | FedDRLPD: Deep reinforcement Learning-Based … | 2026 | aleatória (ablação que troca o módulo DRL por seleção aleatória) | a seleção aleatória degrada o desempenho (Figs. 14-15, 10% e 30% de ataque) | S |
| V2-1275 | Federated Unlearning With Reinforcement Lear… | 2025 | oráculo (retreino do zero) + sem ação defensiva (sem desaprendizado; … | DQN ≈ retreino do zero em acurácia pós-desaprendizado e ASR, com custo menor (14 s vs 22 s); > aleatório e > sem desaprendizado | S |
| V2-1363 | Toward Smart Security Enhancement of Federat… | 2021 | aleatória (VBA-only: mesma verificação, seleção aleatória) | VBA-only já mantém acurácia >97%; o DRL aumenta a utilidade (custo), não a robustez | S |
| V2-1450 | A DQN-Based Multi-Objective Participant Sele… | 2023 | aleatória (FL-Random) + seleção de todos os nós (FL-Greedy) | acurácia estabiliza em 0,98 (DQN) vs 0,96 (Random, Greedy); latência −18%/−35% | S |
| V2-1483 | A hierarchical RL-driven federated framework… | 2026 | aleatória (ablação "sem HRL") | ToN-IoT: H-FAR completo 94,60±0,72% vs "sem HRL" (seleção aleatória) 92,60±0,80% (+2,0 p.p.; 5 sementes) | S |
| V2-2475 | Defending dynamic data poisoning with accura… | 2027 | aleatória | CIFAR-10: Random 0,7978 vs UCB-acc 0,8481; UCB-CS e UCB-CS-acc selecionam quase tantos maliciosos quanto a seleção aleatória (Avg MC), como os própri… | S |
| V2-3789 | Optimization of trusted wireless sensing mod… | 2024 | aleatória (FedAvg) | supera FedAvg e DQN sob ataques | S |
| V2-4233 | S-HSFL: A Game-Theoretic Enhanced Secure-Hyb… | 2026 | aleatória (HSFL original: o servidor seleciona os UEs ao acaso, sem a… | AlexNet Non-IID: 79,46% vs 24,52% | S |
| V2-4266 | Secure Dynamic Scheduling for Federated Lear… | 2024 | aleatória (seleção uniforme de N dispositivos); o secure-UCB "ideal" … | UCB-SCP > Random e CS-UCB; ≈ secure-UCB ideal (baseline aprendido, limite superior) | S |
| V2-4727 | A Secure and Private Distributed Bayesian Fe… | 2026 | aleatória (conexão aleatória) | agente supera conexão aleatória; sem Δ contra heurística de limiar com o mesmo sinal; sem significância | S |
| V2-4728 | Adaptive Federated Learning Defences via Tru… | 2025 | aleatória (+ Linear-Q e PG, aprendidos) | DQN 61,48±4,09 vs aleatório 16,28±3,60 de acurácia; ASR aleatório 36 vs DQN 41 (DQN pior em ASR); baselines perto do acaso; regra de confiança sem DQ… | S |
| V2-1105 | Toward Trustworthy IIoT: A Reinforcement Lea… | 2026 | P (ablação "sem MARL") | "habilitar o MARL melhora a ACC e reduz a ASR" (Figs. 7b e 8b, sem números no texto) | S |
| V2-3243 | Intelligent Aggregation Federation: A Learni… | 2026 | P (ablação w/o RFAS: o texto só diz "systematically removing a specif… | AUC 0,7765 (completo) vs 0,7051 (sem RFAS); 40% mal.: 0,7248 vs Flame 0,6915 | S |
| V2-3331 | LBSFL: a lightweight robust federated learni… | 2026 | P (ablação "Shapley": "Full Shapley value computation without the Ban… | LBSFL 5-6% acima do Shapley completo e 2-3% acima da variante sem truncamento (Non-IID); tempo 45-65% menor | S |
| V2-3555 | Mobility-Aware Federated Learning for Energy… | 2026 | P (ablação que troca o PPO por seleção heurística, sinal não especifi… | robustez 30% mal.: 86,7±1,2 vs 78,9±2,0 sem PPO | S |
| V2-0383 | DearFSAC: A DRL-based Robust Design for Powe… | 2022 | oráculo (regra que conhece os modelos sem defeito) | DearFSAC ≈ oráculo (dN 0,1: 2,89% vs 2,75%; 0,3: 2,73 vs 2,34; M 90%: 2,55 vs 3,21) | S |

**Contagem de votos (descritiva, sem meta-análise, §12.2):** entre os 22 estudos com comparação fixa, heurística ou oráculo, o agente
- **empata ou perde** para política fixa ou de mesmo sinal em **7**: V2-4540 (o escore por reputação iguala ou supera o híbrido nos três regimes, Figs. 9–11, e o DRL puro perde nos três; execução única), V2-1179 (φ fixo a 1,1 p.p. do DDPG com k = 10 sob ataque; sem ataque, DDPG ≈ φ = 0), V2-1327 (peso fixo a ~1 p.p. do DRL sob envenenamento), V2-4789 (braço fixo empata ou vence; no ataque furtivo, FedAvg 39,43 × agente 38,82), V2-0350 (o local-only, λ = 0 fixo, supera o pFedMARL em F1 nos três cenários), V2-0111/SARA (comparável à melhor regra fixa: Median no ataque periódico, Krum no de fingimento no MNIST; A27), V2-2103 (regra de pesos iguais sobre os mesmos 6 sinais: acurácia final igual, 64,35 × 64,32, 3 sementes; o RL só melhora o F1 de detecção, e a variante sem RL faz o mesmo);
- **iguala o oráculo** em 3 (o oráculo fica fora de Π0 e não define a categoria quando há referência admissível, A27): V2-0383 (≈ regra que conhece os modelos sem defeito), V2-1275 (≈ retreino do zero, a custo menor), V2-0111/SARA (escolhe a regra ótima em 27/30 rodadas);
- **vence por margem pequena** (≤ ~6 p.p., sem teste estatístico) em V2-0973 (0,96 × 0,92), V2-1102 (limiar estático: 0,89 × 0,86 com k = 5 e 0,68 × 0,62 com k = 10), SB-03/FedCHO (61,6 × 58,5), V2-0351 (seleção direta por reputação: taxa de erro ~0,03–0,06 × ~0,04–0,12, de 1 a 6 p.p.);
- **vence claramente** uma política fixa que já é uma defesa em V2-4812 (Meta-SG, parâmetros afinados; execução única),V2-2573 (execução única, 12 rodadas), V2-0160 e V2-1130 (auditoria fixa: CJR > 0,9 × 0,55-0,60, sem variância);
- **vence heurísticas de outro sinal** em 6 (V2-0542, V2-1140, V2-1199, V2-3215: Pow-d, que colapsa quando o atacante infla a perda; V2-0835: gulosa por CPU; V2-4059: AMA, que não recebe o indicador de falha do RL).
- Contra a **seleção aleatória** (19 estudos), o agente supera a aleatória em ao menos uma métrica relatada em 17, mas a vantagem nem sempre vem do aprendizado. Em 2 a métrica principal não melhora: em V2-1363 a acurácia passa de 97% com e sem o agente, porque a robustez vem da verificação e o DRL só reduz custo; em V2-0688 o ASR é o mesmo com e sem o bandit (a defesa vem da destilação, como os autores reconhecem). Há ressalvas em outros: V2-2475 relata que as variantes UCB-CS escolhem quase tantos maliciosos quanto a aleatória; em V2-4728 o DQN tem ASR pior que o aleatório (41 × 36).

Contra uma política do **mesmo sinal**, o agente não vence claramente em nenhum dos 6 estudos: empata em 2 (V2-2103, V2-4540) e vence por margem pequena em 4. Só dois desses estudos usam várias sementes (SB-03 e V2-2103), e nenhum aplica teste estatístico a essa comparação. Onde a comparação existe com uma política fixa razoável (V2-1179, 1327, 2103, 4789, 4540), o resultado é empate, mas **nenhum conclui que o aprendizado é dispensável** (§9, Portão N).

## 4. QP3: orçamento de aprendizado

- Aprendizado **online durante o FL** em 68/77; pré-treino/offline em 9 (ex.: Meta-SG, rDP, RA-RL, V2-1103, V2-3243, V2-1327 pré-treinado).
- Orçamento **calculável** (QA7 = S) em 22; parcial em 47; não reportado em 8.
- **Nenhum estudo compara agente e política não aprendida em horizontes diferentes** (critério do adendo A14). Dois variam o nº de rodadas só para o próprio método (V2-1483, T de 50 a 200; SB-03, T de 50 a 500); os demais mostram curvas de convergência, sensibilidade de γ ou limites teóricos de regret.
- Orçamentos efetivos ínfimos aparecem com frequência: DTAG-FL (~12 passos de PPO), TD3-agg V2-3494 (20 rodadas), RL-FL V2-1025 (20 rodadas), OptiGradTrust (25–30 rodadas; nos experimentos de revisão o RL fica congelado), Trust-Aware DQN (ε decai em 5.000 passos com só 50 rodadas), FedStrategist (50–75 atualizações do LinUCB). No outro extremo, Meta-SG (~10⁴ passos de TD3 no pré-treino) e rDP (~60.000 episódios offline sobre perdas pré-medidas).
- Implicação: em muitos estudos o agente mal sai da inicialização/exploração no horizonte avaliado. (Nota interna, fora do artigo: compatível com a observação do §1.2 de política que não se afasta da inicialização.)

## 5. QP5: custo e exposição de privacidade do sinal

| exigência do sinal | nº |
|---|---|
| dados no servidor | 28 |
| só updates | 27 |
| conjunto de teste no servidor | 17 |
| monitoramento do dispositivo | 3 |
| reconstrução de dados do cliente | 2 |

- **Reconstrução de dados do cliente**: AdaAggRL (inversão de gradiente + MMD) e Meta-SG (inversão + cGAN/difusão).
- **Dados no servidor** (root, validação, "entrevista", auxiliar, proxy ou teste): 45 estudos; em 17 deles o dado declarado é o **conjunto de teste** ou foi retirado dele.
- **Monitoramento do dispositivo**: tráfego de rede (V2-0391), auditoria de parâmetros e amostras (V2-1130), atributos sociais (V2-0634).
- **Custo** reportado com números em 41/77 (quase sempre tempo por rodada ou overhead relativo); poucos reportam o custo do treino do agente em si.

## 6. QP6: qualidade da avaliação (QA1–QA9)

Pontuação S = 1, P = 0,5, N = 0 (§10). QA1–QA5 e QA7–QA9 derivados por regra dos campos da extração (adendo A10); QA6 manual.

- Média **2.97**/9; mediana 3.0; máximo 8.5 (V2-2103); 8 estudos com ≥ 5.
| critério | S | P | N |
|---|---|---|---|
| QA1 sem teste na recompensa/seleção | 38 | 20 | 19 |
| QA2 ≥ 3 sementes com variância | 13 | 12 | 52 |
| QA3 teste estatístico ou IC | 7 | 0 | 70 |
| QA4 código disponível | 9 | 3 | 65 |
| QA5 comparação não aprendida | 15 | 30 | 32 |
| QA6 ataques fiéis à definição | 2 | 72 | 3 |
| QA7 orçamento calculável | 22 | 47 | 8 |
| QA8 baselines estáticos fortes | 10 | 16 | 51 |
| QA9 ataque adaptativo | 5 | 15 | 57 |

**Por que a qualidade é baixa:** a literatura é dominada por venues aplicados (IoT, veicular, blockchain) que avaliam um cenário contra FedAvg, com uma execução, sem código e sem ataque que conheça a defesa. A nota não reflete falta de informação na extração: depois da segunda passada, "?" só resta onde o texto não diz em que dados a recompensa é calculada; esses casos e os que usam amostras do pool de teste ficam com QA1 = P (20 estudos).

Mapa QA por estudo:

| id | estudo | ano | alg. | gran. | QA1 | QA2 | QA3 | QA4 | QA5 | QA6 | QA7 | QA8 | QA9 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V2-2103 | Byzantine robust federated learning for… | 2026 | DQN/DDQN | peso/cliente | S | S | S | S | S | P | S | S | S | 8.5 |
| V2-3243 | Intelligent Aggregation Federation: A L… | 2026 | PG/ator-crítico | peso/cliente | S | S | S | N | P | P | S | S | N | 6.0 |
| V2-4789 | FedStrategist: A Meta-Learning Framewor… | 2025 | bandit | regra/rodada | S | N | N | S | S | P | P | P | P | 5.0 |
| V2-4812 | Meta Stackelberg Game: Robust Federated… | 2024 | DDPG/TD3/SAC | parametro | S | N | N | N | S | P | P | S | S | 5.0 |
| V2-0688 | General Backdoor-Resilient Federated Le… | 2026 | bandit | selecao/cliente | S | N | N | N | P | S | P | S | S | 5.0 |
| V2-1231 | Defending against sophisticated poisoni… | 2025 | DDPG/TD3/SAC | peso/cliente | S | N | N | S | N | P | P | S | S | 5.0 |
| V2-1483 | A hierarchical RL-driven federated fram… | 2026 | DQN/DDQN | selecao/cliente | S | S | S | N | P | P | P | P | N | 5.0 |
| V2-2188 | Communication-Security Co-Design for Fe… | 2026 | PG/ator-crítico | peso/cliente | S | P | S | N | N | P | P | S | P | 5.0 |
| V2-0350 | Cooperative Multi-Agent Reinforcement L… | 2026 | MARL | peso/cliente | S | N | N | S | S | P | S | N | N | 4.5 |
| V2-4059 | Reinforcement Learning-Driven Adaptive … | 2025 | Q-learning tabular | peso/cliente | P | S | S | N | P | P | S | N | N | 4.5 |
| V2-1057 | SharBipole: Secure and Scalable Shardin… | 2026 | outro | parametro | S | S | N | N | N | P | P | S | P | 4.5 |
| V2-1105 | Toward Trustworthy IIoT: A Reinforcemen… | 2026 | MARL | selecao/cliente | S | S | S | N | P | P | P | N | N | 4.5 |
| SB-03 | FedCHO: Closed-Loop Hierarchical Orches… | 2026 | DDPG/TD3/SAC | peso/cliente | S | P | N | S | S | P | P | N | N | 4.5 |
| V2-4728 | Adaptive Federated Learning Defences vi… | 2025 | DQN/DDQN | peso/cliente | S | S | N | N | P | P | S | N | N | 4.0 |
| V2-0160 | Agentic AI-Driven Federated Unlearning … | 2026 | Q-learning tabular | parametro | P | N | N | S | S | P | P | N | P | 4.0 |
| V2-3215 | InfRA-FL: Information-Driven Robust Fed… | 2026 | PG/ator-crítico | selecao/cliente | P | S | N | N | P | P | S | P | N | 4.0 |
| V2-0922 | Privacy-Preserving Federated Learning W… | 2025 | Q-learning tabular | peso/cliente | P | S | S | P | N | P | P | N | N | 4.0 |
| V2-1041 | SecureDFL: A Secure Distributed Federat… | 2026 | PG/ator-crítico | parametro | S | S | N | N | N | P | S | N | P | 4.0 |
| V2-1130 | TrustFed: A Reliable Federated Learning… | 2025 | outro | selecao/cliente | S | P | N | N | S | P | S | N | N | 4.0 |
| V2-0351 | Cooperative Physical Layer Authenticati… | 2023 | Q-learning tabular | selecao/cliente | S | N | N | N | S | P | S | N | N | 3.5 |
| V2-3555 | Mobility-Aware Federated Learning for E… | 2026 | PG/ator-crítico | selecao/cliente | S | S | N | N | P | P | P | N | N | 3.5 |
| V2-0542 | FairRoP: Robust Client Selection Scheme… | 2026 | bandit | selecao/cliente | S | P | N | N | P | P | P | P | N | 3.5 |
| V2-1254 | FedAA: a reinforcement learning perspec… | 2025 | DDPG/TD3/SAC | peso/cliente | S | P | N | S | N | P | P | N | N | 3.5 |
| V2-2573 | DTAG-FL: A Digital-Twin, Attention-Grap… | 2026 | PG/ator-crítico | regra/rodada | P | N | N | N | S | P | P | P | P | 3.5 |
| V2-4339 | Shielding Federated Learning: Robust Ag… | 2022 | bandit | selecao/cliente | S | N | N | N | N | S | N | P | S | 3.5 |
| V2-4540 | Towards a distributed nodes selection m… | 2024 | PG/ator-crítico | selecao/cliente | P | N | N | S | S | P | P | N | N | 3.5 |
| V2-0918 | Privacy-Preserving Byzantine-Robust Fed… | 2025 | DDPG/TD3/SAC | peso/cliente | S | N | N | N | N | P | P | S | P | 3.5 |
| V2-0987 | Resisting Poisoning Attacks in Federate… | 2025 | PG/ator-crítico | peso/cliente | P | N | N | P | N | P | P | S | P | 3.5 |
| V2-1126 | TrustBandit: Optimizing Client Selectio… | 2024 | bandit | selecao/cliente | S | S | N | N | P | P | P | N | N | 3.5 |
| V2-0837 | Multi-Model based Federated Learning Ag… | 2024 | DQN/DDQN | parametro | S | P | N | N | P | P | P | N | N | 3.0 |
| V2-1327 | Preventing harm to the rare in combatin… | 2024 | DQN/DDQN | peso/cliente | P | P | N | N | S | P | N | P | N | 3.0 |
| V2-0111 | Adapting Aggregation Rule for Robust Fe… | 2025 | bandit | regra/rodada | N | N | N | N | S | P | P | P | P | 3.0 |
| V2-0391 | Deep Learning based Moving Target Defen… | 2025 | outro | selecao/cliente | S | P | N | N | P | P | P | N | N | 3.0 |
| V2-0530 | Exploiting Gaussian Noise Variance for … | 2025 | Q-learning tabular | parametro | P | N | N | N | N | P | S | P | P | 3.0 |
| V2-0634 | FedSAP: Secure Federated Learning in SD… | 2024 | DDPG/TD3/SAC | selecao/cliente | S | N | N | N | P | P | S | N | N | 3.0 |
| V2-1199 | An Enhanced Combinatorial Contextual Ne… | 2024 | bandit | selecao/cliente | P | S | N | N | P | P | P | N | N | 3.0 |
| V2-1229 | Decentralized Federated Learning toward… | 2025 | bandit | selecao/cliente | S | P | N | N | N | P | P | N | P | 3.0 |
| V2-3331 | LBSFL: a lightweight robust federated l… | 2026 | bandit | selecao/cliente | S | P | N | N | P | P | P | N | N | 3.0 |
| V2-1102 | Toward Secure Federated Learning for Io… | 2022 | DDPG/TD3/SAC | parametro | N | P | N | N | S | P | S | N | N | 3.0 |
| V2-1178 | A robust federated learning framework f… | 2026 | PG/ator-crítico | peso/cliente | S | N | N | N | N | P | P | P | N | 2.5 |
| V2-4233 | S-HSFL: A Game-Theoretic Enhanced Secur… | 2026 | bandit | selecao/cliente | N | N | N | S | P | P | P | N | N | 2.5 |
| V2-0383 | DearFSAC: A DRL-based Robust Design for… | 2022 | DDPG/TD3/SAC | peso/cliente | S | N | N | N | P | P | P | N | N | 2.5 |
| V2-0506 | Enhancing Federated Learning in IoV: Ro… | 2026 | DQN/DDQN | selecao/cliente | S | N | N | N | N | P | S | N | N | 2.5 |
| V2-1179 | A Secure and Fair Client Selection Base… | 2024 | DDPG/TD3/SAC | parametro | N | N | N | N | S | P | S | N | N | 2.5 |
| V2-4266 | Secure Dynamic Scheduling for Federated… | 2024 | bandit | selecao/cliente | S | N | N | N | P | P | P | N | N | 2.5 |
| V2-0973 | Reputation-Aware Multi-Agent DRL for Se… | 2023 | MARL | parametro | N | N | N | N | S | P | S | N | N | 2.5 |
| V2-1001 | Risk-Aware Reinforcement Learning-Based… | 2024 | outro | selecao/cliente | N | P | N | N | N | P | S | N | P | 2.5 |
| V2-1140 | Two-Stage Client Selection for Federate… | 2024 | bandit | selecao/cliente | S | N | N | N | P | P | P | N | N | 2.5 |
| V2-4727 | A Secure and Private Distributed Bayesi… | 2026 | PG/ator-crítico | peso/cliente | S | N | N | N | P | P | N | N | N | 2.0 |
| V2-3175 | Improved Federated Learning Incentive M… | 2025 | DDPG/TD3/SAC | selecao/cliente | P | N | N | N | N | P | P | P | N | 2.0 |
| V2-3830 | Participant Selection for Efficient and… | 2025 | DQN/DDQN | selecao/cliente | N | N | N | N | N | P | S | P | N | 2.0 |
| V2-0495 | Endogenous Security-Aware Device Schedu… | 2023 | DQN/DDQN | selecao/cliente | S | N | N | N | N | P | P | N | N | 2.0 |
| V2-0835 | Multi-Job Hierarchical Federated Learni… | 2025 | DQN/DDQN | selecao/cliente | N | N | N | N | P | P | S | N | N | 2.0 |
| V2-1185 | Adaptive aggregation and robust client … | 2026 | bandit | selecao/cliente | N | N | N | N | N | P | P | P | P | 2.0 |
| V2-1294 | Human Immune System Inspired Security f… | 2025 | DQN/DDQN | selecao/cliente | P | N | N | N | N | P | P | P | N | 2.0 |
| V2-1450 | A DQN-Based Multi-Objective Participant… | 2023 | DQN/DDQN | selecao/cliente | N | N | N | N | P | P | S | N | N | 2.0 |
| V2-2475 | Defending dynamic data poisoning with a… | 2027 | bandit | selecao/cliente | P | N | N | N | P | P | P | N | N | 2.0 |
| V2-2891 | FEDDRL: TRUSTWORTHY FEDERATED LEARNING … | 2024 | DDPG/TD3/SAC | selecao/cliente | S | N | N | N | N | N | P | N | P | 2.0 |
| V2-3265 | Interpretable reputation driven asynchr… | 2026 | DDPG/TD3/SAC | selecao/cliente | N | N | N | N | N | P | P | S | N | 2.0 |
| V2-3494 | Malicious Node Detection and Robust Fed… | 2025 | DDPG/TD3/SAC | peso/cliente | P | N | N | N | N | P | P | P | N | 2.0 |
| V2-3789 | Optimization of trusted wireless sensin… | 2024 | DQN/DDQN | selecao/cliente | P | N | N | N | P | P | P | N | N | 2.0 |
| V2-1012 | Robust Peer-to-Peer Federated Learning … | 2026 | DQN/DDQN | selecao/cliente | N | N | N | N | P | P | S | N | N | 2.0 |
| V2-1030 | Secure and Efficient Federated Learning… | 2025 | MARL | selecao/cliente | S | N | N | N | N | P | N | N | P | 2.0 |
| V2-1103 | Toward Securing Federated Learning Agai… | 2023 | DQN/DDQN | selecao/cliente | P | N | N | N | N | P | S | N | N | 2.0 |
| V2-1275 | Federated Unlearning With Reinforcement… | 2025 | DQN/DDQN | selecao/cliente | N | N | N | N | P | P | N | P | N | 1.5 |
| V2-2890 | FedDrive-Sec: A blockchain-assisted fed… | 2026 | outro | peso/cliente | P | N | N | N | N | P | P | N | N | 1.5 |
| V2-0065 | A Privacy Preserving and Byzantine Robu… | 2024 | PG/ator-crítico | selecao/cliente | S | N | N | N | N | P | N | N | N | 1.5 |
| V2-0550 | Fed-Reputed: Reputation-Aware Client Se… | 2026 | DQN/DDQN | selecao/cliente | N | N | N | N | P | P | P | N | N | 1.5 |
| V2-1261 | FedDRLPD: Deep reinforcement Learning-B… | 2026 | DQN/DDQN | selecao/cliente | N | N | N | N | P | P | P | N | N | 1.5 |
| V2-1363 | Toward Smart Security Enhancement of Fe… | 2021 | DQN/DDQN | selecao/cliente | N | N | N | N | P | P | P | N | N | 1.5 |
| V2-0940 | Quality-aware Client Selection and Reso… | 2024 | bandit | selecao/cliente | N | N | N | N | P | P | P | N | N | 1.5 |
| V2-0946 | RA-RL: Reputation-Aware Edge Device Sel… | 2021 | PG/ator-crítico | selecao/cliente | P | N | N | N | N | P | P | N | N | 1.5 |
| V2-1025 | SCFM-FedRL: a Secure and Drift-Aware Fe… | 2026 | Q-learning tabular | selecao/cliente | P | N | N | N | N | P | P | N | N | 1.5 |
| V2-0945 | R$^{2}$Fed: Resilient Reinforcement Fed… | 2023 | DDPG/TD3/SAC | peso/cliente | S | N | N | N | N | N | P | N | N | 1.5 |
| V2-0590 | Federated Learning-Based Secure Computi… | 2025 | DDPG/TD3/SAC | selecao/cliente | N | N | N | N | N | N | S | N | N | 1 |
| V2-0368 | D2MIF: A Malicious Model Detection Mech… | 2023 | DDPG/TD3/SAC | parametro | P | N | N | N | N | P | N | N | N | 1.0 |
| V2-1042 | SecureGraphFL: A Privacy-Preserving and… | 2025 | PG/ator-crítico | selecao/cliente | N | N | N | P | N | P | N | N | N | 1.0 |

## 7. QP7: auditorias e baselines simples (síntese narrativa)

**Corpus:** 29 estudos Q7-I (25 pela busca, 4 pelo snowballing) + 5 leituras canônicas do §13. Ficha por estudo em `extracao_qp7.csv` (consenso com o autor, adendo A15). Esses trabalhos **não fazem parte da população principal**: não entram nas contagens das QP1–QP6 e servem só como fundamentação externa.

**Composição:** 5 leituras canônicas; 28 trabalhos sobre FL (23 em FL horizontal, 3 em FL vertical, 1 em FL descentralizado e 1 em FL personalizado); e 1 fora de FL (V2-3771, MARL com agentes bizantinos, citado só como exemplo metodológico). Entre os 28 trabalhos sobre FL, 25 mostram um baseline simples igualando ou superando um método mais sofisticado, e 2 aplicam teste estatístico (V2-4831, V2-0116).

**Em RL em geral (§13):** Henderson et al. (2018) mostram que a variância entre sementes e detalhes de implementação mudam conclusões em deep RL; Agarwal et al. (2021) mostram que com poucas execuções as estimativas pontuais enganam e defendem intervalos e IQM; Mania, Guy e Recht (2018) e Rajeswaran et al. (2017) mostram que busca aleatória simples e políticas lineares igualam deep RL em benchmarks de controle. Fora de FL, **V2-3771** (MARL resiliente para controle de formação, 20 sementes pareadas por célula, correção de Holm) mostra esse rigor aplicado a um método aprendido sob falhas bizantinas: sem ataque, a mediana (MAPPO-CWMed) tem a menor taxa de violações, e após Holm nenhuma vantagem do RS-MARL se sustenta. Não trata de defesa de agregação em FL e não sustenta conclusões sobre o corpus principal.

**Em FL robusto:** as auditorias convergem em cinco armadilhas: (i) datasets fáceis (≈ 30% só MNIST) e ataques simplistas (≈ 40%) (Decoding FL Defenses); (ii) não-IID quebra agregações robustas e defesas de backdoor (Li et al. TBD; Breaking the Illusion; BackDFL; Comprehensive Evaluation); (iii) adversários adaptativos quebram defesas de tipo único (Hammer & Anvil; survey de adversários adaptativos); (iv) bugs e métricas incompletas (BackFed; TFLlib; DPArena; aeronáutico); (v) em cenários de produção, **defesas simples bastam** (Back to the Drawing Board) e escolhas simples, como taxa de aprendizado do servidor baixa ou compartilhamento parcial do modelo, já dão robustez (BackFed; pFL/Simple-Tuning).

**Baselines simples relevantes para o Portão N:** ABSA (V2-0116), que troca entre agregação leve e robusta por detecção de anomalia **sem aprendizado**, fica a cerca de 1 p.p. da melhor defesa estática (Multi-Krum: 83,1 × 84,1 com 30% de maliciosos), com 38% menos computação e teste estatístico. Por não aprender, não pertence à população principal; é o análogo não aprendido de SARA, FedStrategist e DTAG-FL.

**Lacuna:** nenhum dos 28 trabalhos sobre FL avalia experimentalmente defesas por RL/bandit em FL. Só citam ou catalogam: Decoding FL Defenses (V2-4764) inclui o GAAvernor na auditoria de 50 defesas e mostra que ele cai nas mesmas armadilhas; a SoK veicular (V2-4840) cataloga o DRL-PBFL; V2-1365 cita o FairFL (MARL de equidade). O survey de adversários adaptativos (ePrint 2025/510) não cita nenhuma defesa por RL.

## 8. Agenda de lacunas

1. **Isolamento do aprendizado:** 32/77 sem nenhuma comparação não aprendida; 19 só contra aleatória; 6 contra política do mesmo sinal, nenhuma com teste estatístico.
2. **Horizonte:** nenhum estudo mede o ganho do agente sobre a política não aprendida em função do nº de rodadas; orçamentos efetivos frequentemente ínfimos.
3. **Ataques que conhecem o agente:** 5/77 com ataque adaptativo real (Meta-SG, AdaAggRL com RL-attack, BR-DFL, OptiGradTrust white-box, MAB-RFL com divisão dos maliciosos contra o ISA); nenhum ataque mira a política do agente (envenenamento da recompensa ou do estado), exceto a discussão teórica do InfRA-FL.
4. **Rigor estatístico:** 13/77 com ≥ 3 sementes e variância; 7/77 com teste estatístico ou IC.
5. **Vazamento:** 19/77 usam o conjunto de teste na recompensa, no estado, na seleção ou na verificação; 20/77 não dizem em que dados a recompensa é calculada ou usam amostras do pool de teste; 2 usam rótulos de malicioso na recompensa (V2-4728, V2-2103).
6. **Privacidade do sinal:** 45/77 exigem dados no servidor (17 deles o próprio conjunto de teste) e 2 reconstroem dados do cliente; raramente discutido como custo.
7. **Reprodutibilidade:** código em 9/77.
8. **Granularidade e memória:** nenhum estudo separa o efeito da granularidade (regra × peso por cliente) nem o da memória do efeito do aprendizado.

## 9. Decisões internas (fora do artigo)

### Portão N: **parcialmente mostrado**

Critério (§2): "já mostrado" exige um estudo em que política não aprendida com o **mesmo sinal** iguala ou supera o agente **e** isso é apresentado como achado. Há 7 empates contra o mesmo sinal ou a ação fixa (V2-1179, V2-1327, V2-4789, V2-0350, V2-2103, V2-4540, V2-0111; V2-0383 empata contra oráculo). Em 2 os autores não reconhecem o empate: V2-1327 atribui o ganho aos pesos maiores no rótulo especial, e V2-4789 não comenta a Mediana nem o FedAvg sob ataque furtivo. Em 4 reconhecem, mas enquadram a igualdade como virtude do agente: V2-1179 ("essentially similar" ao φ = 1 fixo, porque o agente acha sozinho a melhor fixa de cada regime), V2-0350 (o local-only fixo supera no local, lido como troca entre personalização e generalização), V2-2103 (acurácia "identical with and without RL", com o RL reposicionado como consistência da detecção; mesmo sinal, 3 sementes) e V2-4540. O mais próximo é V2-4540: o escore por reputação, sobre o mesmo sinal, iguala ou supera o híbrido e o DRL puro em acurácia (Figs. 9–11), e os autores atribuem a robustez ao próprio escore; mas defendem o híbrido pela adaptabilidade e pela imprevisibilidade, sem testar ataque adaptativo, com execução única, só MNIST e 30 rodadas. Nenhum conclui que o aprendizado é dispensável. Em V2-0688 os autores reconhecem que a defesa vem da destilação e não do bandit, mas a comparação é com seleção aleatória, não com o mesmo sinal. → **A novidade do artigo de auditoria se mantém.** Citar e diferenciar esses estudos; a contribuição é tornar o teste sistemático (mesmo sinal, várias sementes, estatística, horizonte, ataque adaptativo) e generalizá-lo entre métodos.

### Portão R: requisitos e baselines obrigatórios para o GRADF-v2

**Requisitos (lacunas a cobrir):** ataques adaptativos que conhecem a defesa e o agente (incluindo manipulação do sinal e on-off); não-IID forte (Dirichlet ≤ 0,1); avaliação com ≥ 5 sementes, IC e teste; sem uso de teste na recompensa; custo por rodada e exposição de privacidade declarados; análise de horizonte.

**Baselines obrigatórios:**
- não aprendidos no **mesmo espaço de ação e mesmo sinal**: ação fixa por regra/peso, limiar fixo sobre o sinal, seleção aleatória;
- adaptativos não-RL: **ABSA** (V2-0116), **FedLAW** (SB-04, ICLR 2026), SAGE, BRITE-FL e FLIDS (ficha §9.2);
- estáticos fortes: FedAvg, Median, Trimmed Mean, Krum/Multi-Krum, **FLTrust**, **FLAME**, Bulyan/RFA;
- por RL/bandit, como concorrentes: **SARA**, **FedStrategist** (regra por rodada; o TARS, V2-1120, saiu por IC4 e só se cita como trabalho relacionado); **AdaAggRL**, **FedAA** (pesos); **MAB-RFL** (seleção);
- ataques: LIE, Min-Max/Min-Sum (AGR-tailored), IPM, LMP, RL-attack (Li et al. 2022), on-off/pretense, backdoor (DBA, scaling).

## 10. Limitações a declarar

- Triagem da etapa 1 com dois revisores numa amostra de 20% (κ = 0,737; concordância 98,6%; PABAK 0,973; adendo A13). Extração da S1 (QP1–QP6) feita com assistência de IA (adendo A10) e conciliada com o fichamento independente do autor em 77 dos 78 estudos então incluídos (adendo A14); o V2-1120 saiu depois por IC4 (adendo A22).
- Conferência do revisor 2 na etapa 2 (A16): concordância antes do consenso baixa — inclusão/exclusão κ = 0,35 (65,4%; PABAK 0,31; n = 52), categoria da QP2 κ = 0,14 (n = 52), qualidade κ = 0,15 (16 × 9) — em parte porque a conferência foi feita sem o texto completo; o consenso manteve todas as decisões do revisor 1. QP7 conciliada com o fichamento do autor (A15); qualidade não codificada em dobro além da amostra de 20%.
- Protocolo não pré-registrado (A2); Web of Science não consultado; ACM sem busca em Keywords (A5).
- 5 estudos da S1/QP7 sem acesso pela CAPES, 1 tese e 2 do snowballing não recuperados.
- Campos "?" mantidos onde o texto não informa (sobretudo o dado da recompensa); nada foi inferido (§14).
