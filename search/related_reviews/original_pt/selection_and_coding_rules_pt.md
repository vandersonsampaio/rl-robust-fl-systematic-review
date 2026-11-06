# Busca complementar por revisões anteriores: regras e seleção da Tabela 2 (Q19)

**Escopo.** Busca feita em 15 e 16/10/2026 (ACM DL, IEEE Xplore, Scopus, arXiv; desde 2017), só para posicionar a revisão na seção de trabalhos relacionados. Nenhum registro dela entrou no corpus principal, cuja busca terminou em 28/09/2026.

**String.** ("federated learning") AND (byzantine OR poisoning OR backdoor OR "malicious client*" OR "robust aggregation") AND (survey OR review OR "systematization of knowledge" OR SoK). Não há termos de RL, para recuperar revisões que tratam dessas defesas só no corpo do texto.

**Registros.** `SLR_Related/revisoes_consolidado.csv` (404 registros únicos, um por linha, com a decisão na coluna `triagem`; consolidado por `scripts/busca_revisoes.py`).

## Regra de 404 para 45

| decisão | n | regra |
|---|---|---|
| `ja_na_S1` | 90 | o registro já estava nos 4.054 triados na S1 (mesmo DOI ou título normalizado); a decisão da S1 está em `s1_decisao` |
| `revisao_central` | 45 | revisão, survey ou SoK com a segurança de FL contra clientes adversários como tema central (título e resumo) |
| `fora` | 269 | não é revisão, ou a segurança de FL contra clientes adversários não é o tema central |

Nas 45 centrais, a coluna `rl_objeto` registra a leitura das menções a RL no texto completo: `cataloga` (descreve uma defesa por RL), `sugere_como_direcao` (sugere RL como direção futura, sem analisar) ou `N`. Em 22/10/2026 o R-232 passou de `sugere_como_direcao` para `N`: o RL aparece só como técnica de ataque.

## Regra de seleção da Tabela 2

Entra na tabela o trabalho, identificado nas buscas (principal ou complementar), no snowballing da RQ7 ou na leitura das referências, que atende a pelo menos um critério:

1. cataloga defesas por RL ou bandits, ou as sugere como direção futura;
2. faz experimentos ou audita práticas de avaliação;
3. é um dos dois surveys amplos escolhidos para representar o grupo que organiza a literatura por ataque ou família de defesa. Essa escolha é um julgamento dos autores; as demais revisões centrais desse grupo estão no CSV com `rl_objeto = N`.

| entrada | origem | critério | justificativa |
|---|---|---|---|
| Rodríguez-Barroso et al., 2023 (SB-07) | snowballing (RQ7) | 2 | survey com experimento |
| Sharma et al., 2023 (SB-09) | snowballing (RQ7) | 2 | SoK com experimento |
| Ali et al., 2023 (V2-0091) | busca principal | 1 | survey de DL que inclui RL em segurança |
| Lyu et al., 2024 (R-293) | busca complementar | 3 | survey amplo de privacidade e robustez em FL |
| Wan et al., 2024 (R-003) | busca complementar | 3 | survey amplo de envenenamento e backdoor em FL sem fio |
| Yang et al., 2024 (R-394) | busca complementar | 1 | cataloga uma defesa por RL (GAAvernor) |
| Szeląg et al., 2025 | RQ7 (C-Szelag) | 2 | survey com experimento de adversários adaptativos |
| Ahmad et al., 2025 (V2-2725; R-376) | busca principal | 1 | sugere RL como direção futura |
| Khan et al., 2025 (V2-4764) | busca principal | 1, 2 | SoK e auditoria de práticas de avaliação; cita RL |
| Zhang et al., 2025 (V2-4839) | busca principal | 2 | SoK com benchmark |
| Junior et al., 2025 (V2-0101) | busca principal | 1, 2 | revisão sistemática da praticidade das defesas; cita RL |
| Soulb et al., 2025 (R-304) | busca complementar | 2 | revisão com estudos de caso (IC 95%, testes pareados); acrescentada em 22/10/2026 |
| Zakaria e Khalid, 2025 (R-385) | busca complementar | 1 | sugere um agente de defesa por RL como tendência; acrescentada em 22/10/2026 |
| Bajgai et al., 2026 (V2-0566) | busca principal | 1 | survey de FL e RL em segurança |
| Li et al., 2025 (R-355) | busca complementar | 1 | cataloga o R2Fed como mecanismo de resiliência por RL e sugere agregação com RL; antes codificado N pelo resumo, lido no texto completo em 22/10/2026 (Q22) |
| Chacko e Kalaivani, 2026 (R-222) | busca complementar | 1 | sugere RL profundo para a avaliação de confiança; acrescentada em 22/10/2026 |
| Bellachia et al., 2026 (SB-08) | snowballing (RQ7) | 2 | revisão sistemática com benchmark |
| Shahsavari et al., 2026 (V2-4840) | busca principal | 1, 2 | SoK e auditoria; cita RL |

**Conferência das demais 45.** R-232 (RL só como ataque), R-403 (RL citado como área de aplicação do FL) e R-384 (revisão sistemática sem experimento nem auditoria) não atendem a nenhum critério.

## Codificação das colunas da Tabela 2 (Q22)

Cada célula registra se o aspecto é objeto da análise do trabalho (✓), se é tratado parcialmente (◐) ou se não é tratado (✗). A codificação é do R1, a partir do texto completo.

| coluna | ✓ | ◐ | ✗ |
|---|---|---|---|
| RL/bandits | analisa defesas por RL ou bandits como objeto | cataloga defesas por RL, sugere RL como direção futura sem analisar, ou trata RL fora da defesa de agregação | não menciona RL como defesa |
| Robustez em FL | a robustez de FL é o tema central | a robustez de FL é um entre vários paradigmas ou aplicações cobertos | não trata |
| Clientes adversários | o adversário é um cliente que envia atualizações maliciosas e é o foco | clientes adversários são uma entre várias ameaças ou fontes de falha | não trata |
| Contribuição incremental do aprendizado | pergunta se o desempenho de uma defesa decorre do componente aprendido | discute a pergunta sem analisá-la | não trata |
| Baselines por componente controlado | classifica os baselines pelos componentes que mantêm constantes | compara com baselines simples sem classificá-los por componente | não trata |
| Sementes, inferência, teste e orçamento | analisa os quatro aspectos em conjunto na literatura revisada | audita como a literatura avalia defesas, ou recomenda explicitamente uma das quatro práticas, sem analisar as quatro | não audita as práticas de avaliação da literatura (rodar experimentos próprios com sementes ou testes não conta) |

Nenhuma entrada tem ✓ ou ◐ nas colunas de contribuição incremental e de baselines por componente: nenhuma tem defesas por RL ou bandits como objeto, e por isso nenhuma pode perguntar se o desempenho decorre do aprendizado.

| entrada | RL/bandits | robustez | adversários | qualidade | evidência das marcas ◐ e ✓ |
|---|---|---|---|---|---|
| Rodríguez-Barroso et al., 2023 (SB-07) | ✗ | ✓ | ✓ | ✗ | survey de ameaças em FL com experimento próprio (25 execuções em parte dos testes); não audita a literatura |
| Sharma et al., 2023 (SB-09) | ✗ | ✓ | ✓ | ◐ | SoK que modela a completude dos estudos de ataque (auditoria das práticas de avaliação) |
| Ali et al., 2023 (V2-0091) | ◐ | ◐ | ✓ | ✗ | survey de ataques em DL; FL e DRL são dois dos paradigmas cobertos |
| Lyu et al., 2024 (R-293) | ✗ | ✓ | ✓ | ✗ | survey de privacidade e robustez em FL |
| Wan et al., 2024 (R-003) | ✗ | ✓ | ✓ | ✗ | survey de envenenamento e backdoor em FL sem fio; RL citado fora da defesa |
| Yang et al., 2024 (R-394) | ◐ | ✓ | ✓ | ✗ | cataloga o GAAvernor (defesa por RL) sem analisá-lo |
| Szeląg et al., 2025 | ✗ | ✓ | ✓ | ✗ | survey de adversários adaptativos com experimento (teste t pareado); não audita a literatura nem cita defesas por RL |
| Ahmad et al., 2025 (V2-2725) | ◐ | ✓ | ✓ | ✗ | revisão sistemática de agregação resiliente a bizantinos; sugere RL como direção futura |
| Khan et al., 2025 (V2-4764) | ◐ | ✓ | ✓ | ◐ | auditoria de 50 defesas (30% só MNIST, 40% ataques simplistas); cataloga o GAAvernor sem avaliá-lo |
| Zhang et al., 2025 (V2-4839) | ✗ | ✓ | ✓ | ✗ | benchmark de 17 defesas × 15 ataques; não audita como a literatura avalia |
| Junior et al., 2025 (V2-0101) | ◐ | ✓ | ✓ | ◐ | revisão sistemática da praticidade das defesas em IoT (examina as condições de avaliação); cita RL |
| Soulb et al., 2025 (R-304) | ✗ | ✓ | ◐ | ◐ | revisão com estudos de caso; adversários são uma de três fontes de fragilidade (com não-IID e rótulos ruidosos); recomenda relatar IC e significância |
| Zakaria e Khalid, 2025 (R-385) | ◐ | ✓ | ✓ | ✗ | revisão sistemática; sugere um agente de defesa por RL como tendência |
| Li et al., 2025 (R-355) | ◐ | ✓ | ✓ | ✗ | cataloga o R2Fed como mecanismo de resiliência por RL e sugere agregação com RL |
| Bajgai et al., 2026 (V2-0566) | ◐ | ◐ | ◐ | ✗ | survey de FL e RL para ciberdefesa; o RL não é examinado como componente de uma defesa de agregação |
| Chacko e Kalaivani, 2026 (R-222) | ◐ | ✓ | ✓ | ✗ | survey de FL com confiança adaptativa em saúde; sugere RL profundo para a avaliação de confiança |
| Bellachia et al., 2026 (SB-08) | ✗ | ✓ | ✓ | ✗ | revisão sistemática com benchmark de backdoor; não audita como a literatura avalia |
| Shahsavari et al., 2026 (V2-4840) | ◐ | ◐ | ◐ | ◐ | SoK de FL para detecção de intrusão veicular; audita mais de 60 trabalhos (IID artificial, avaliação adversarial fraca); cataloga o DRL-PBFL |

## As 45 revisões centrais

Todas as 45 foram lidas no texto completo (32 até 16/10/2026; 13 em 22/10/2026, das quais 7 pelo arXiv e 6 obtidas pelo autor). A coluna `rl_objeto` do CSV registra a leitura: nenhuma tem defesas por RL ou bandits como objeto; 2 catalogam uma defesa por RL (R-355, R-394), 2 sugerem RL como direção futura (R-222, R-385), e as demais 41 não mencionam RL como defesa. O R-376 (Ahmad, V2-2725) também sugere RL, mas está entre os registros já triados na S1, e não entre as 45.

| rid | ano | título | rl_objeto | na Tabela 2 |
|---|---|---|---|---|
| R-001 | 2025 | Backdoor attacks and defense mechanisms in federated learning: A survey | N | não |
| R-002 | 2024 | A survey on privacy-preserving federated learning against poisoning attacks | N | não |
| R-003 | 2024 | Data and Model Poisoning Backdoor Attacks on Wireless Federated Learning, and the Defense Mechanisms: A Compre | N | sim |
| R-004 | 2024 | Backdoor attacks and defenses in federated learning: Survey, challenges and future research directions | N | não |
| R-005 | 2022 | Defense Strategies Toward Model Poisoning Attacks in Federated Learning: A Survey | N | não |
| R-015 | 2025 | Securing the collective intelligence: a comprehensive review of federated learning security attacks and defens | N | não |
| R-031 | 2026 | On the security and privacy of federated learning: A survey with attacks, defenses, frameworks, applications,  | N | não |
| R-032 | 2022 | Federated learning attack surface: taxonomy, cyber defences, challenges, and future directions | N | não |
| R-042 | 2023 | Backdoor Attacks and Defenses in Federated Learning: State-of-the-Art, Taxonomy, and Future Directions | N | não |
| R-101 | 2022 | A contemplative perspective on federated machine learning: Taxonomy, threats &amp; vulnerability assessment an | N | não |
| R-128 | 2024 | A survey on vulnerability of federated learning: A learning algorithm perspective | N | não |
| R-133 | 2021 | A survey on security and privacy of federated learning | N | não |
| R-154 | 2021 | Achieving security and privacy in federated learning systems: Survey, research challenges and future direction | N | não |
| R-159 | 2025 | Federated Learning for Urban Sensing Systems: A Comprehensive Survey on Attacks, Defences, Incentive Mechanism | N | não |
| R-174 | 2024 | Research Progress on Security and Privacy of Federated Learning: A Survey | N | não |
| R-222 | 2026 | Adaptive Trust-Aware Federated Learning for Detecting Malicious Clients in Healthcare Networks:A Survey | sugere_como_direcao | sim |
| R-223 | 2025 | State-of-the-Art Defense Schemes Against Byzantine Attack in Federated Learning | N | não |
| R-229 | 2026 | Detecting Malicious Clients in Federated Learning | N | não |
| R-231 | 2026 | A Comprehensive Review of Attacks and Defense Mechanisms in Federated Learning for Autonomous Driving and VANE | N | não |
| R-232 | 2023 | Poisoning Attacks in Federated Learning: A Survey | N | não |
| R-233 | 2026 | Beyond Data Silos: A Comprehensive Survey on Privacy-Preserving and Secure Federated Learning | N | não |
| R-239 | 2025 | Poisoning Attacks and Defenses Techniques for Federated Learning: A Survey | N | não |
| R-241 | 2025 | Securing Federated Learning in IoT: A Survey of Attacks, Defenses, and Frameworks | N | não |
| R-245 | 2025 | Poisoning Attacks Against Federated Recommender Systems and the Defenses: A Survey | N | não |
| R-250 | 2023 | Federated learning: Applications, Security hazards and Defense measures | N | não |
| R-279 | 2021 | A survey on security and privacy threats to federated learning | N | não |
| R-283 | 2024 | A Review on Federated Learning with a Focus on Security and Privacy | N | não |
| R-284 | 2026 | Defense Against Adversarial Attacks in Federated Learning: A Research for Secure Biomedical Innovation | N | não |
| R-293 | 2024 | Privacy and Robustness in Federated Learning: Attacks and Defenses | N | sim |
| R-298 | 2026 | Trustworthy Distributed Machine Learning in Cloud-Edge-IoT Systems: A Heterogeneity-Aware Survey of Security,  | N | não |
| R-304 | 2025 | Evaluating the Robustness in Federated Learning for Medical Imaging | N | sim |
| R-355 | 2025 | Towards Resilient Federated Learning in CyberEdge Networks: Recent Advances and Future Trends | cataloga | sim |
| R-364 | 2023 | A Survey on Federated Learning Poisoning Attacks and Defenses | N | não |
| R-366 | 2023 | Poisoning Attacks and Defenses in Federated Learning: A Survey | N | não |
| R-371 | 2020 | Threats to Federated Learning: A Survey | N | não |
| R-377 | 2026 | Framing Adversarial Federated Learning Threats through MITRE ATLAS | N | não |
| R-378 | 2025 | Byzantine fault tolerance in distributed machine learning: a survey | N | não |
| R-384 | 2023 | Navigating the Void: Uncovering Research Gaps in the Detection of Data Poisoning Attacks in Federated Learning | N | não |
| R-385 | 2025 | A Review of Federated Learning Attacks: Threat Models and Defence Strategies | sugere_como_direcao | sim |
| R-388 | 2022 | Privacy and Security in Federated Learning: A Survey | N | não |
| R-391 | 2025 | Privacy-Preserving Federated Learning in Healthcare, E-Commerce, and Finance: A Taxonomy of Security Threats a | N | não |
| R-393 | 2024 | Challenges and Countermeasures of Federated Learning Data Poisoning Attack Situation Prediction | N | não |
| R-394 | 2024 | Robust and privacy-preserving collaborative training: a comprehensive survey | cataloga | sim |
| R-402 | 2025 | A survey of security threats in federated learning | N | não |
| R-403 | 2022 | Threats, attacks and defenses to federated learning: issues, taxonomy and perspectives | N | não |
