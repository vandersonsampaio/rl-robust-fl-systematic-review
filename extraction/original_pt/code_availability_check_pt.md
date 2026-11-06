# Conferência do código (QA4, adendo A24)

**Data:** 22/10/2026. **Motivo:** Q18 da revisão do paper. O QA4 passa a pontuar acessibilidade e suficiência, e não o local de hospedagem.

**Regra.** S: código acessível sem intermediação (repositório público ou suplemento do periódico) com a implementação do agente e do experimento (ataques e configuração ou scripts). P: código acessível mas incompleto, ou declarado disponível sem acesso direto (mediante pedido, sem link ou link quebrado). N: sem código declarado.

**Procedimento.** Para cada estudo que declarava código, o link do artigo foi aberto (API do GitHub, Zenodo, DOI) e a árvore de arquivos foi lida. A presença do agente e dos ataques foi verificada pelos nomes dos arquivos e por busca de termos (attack, poison, malicious, byzantine, adversarial) no código. Os experimentos não foram reexecutados.

| estudo | link | agente | ataques | config./scripts | antes | depois |
|---|---|---|---|---|---|---|
| V2-4789 | github.com/rafidhaque/FedStrategist; Zenodo 16068113 | src/bandit.py | src/attacks.py | src/main.py | S | S |
| V2-0160 | github.com/pranav21684/AGENTIC-AI-UNLEARNING (redirecionado) | Agentic_behavior.ipynb | Mainmethod.ipynb | notebooks | S | S |
| V2-4233 | github.com/Echolic/HFSL | secure_selector.py | experiment_hsvfl.py, experiment_sign.py | experiment*.py | S | S |
| V2-0350 | github.com/NexuFed/pFedMARL | src/reinforcement_learning | clientes adversários em src/components/client.py e nos .yaml | .config, scripts/icassp_runs.sh | S | S |
| V2-1231 | github.com/TAP-LLM/AdaAggRL | main.py | attack_utilities.py | requirements, exp_environments | S | S |
| V2-1254 | github.com/Gp1g/FedAA | DDPG/ | --attack same_value, sign_flip, gaussian | main.py | S | S |
| V2-2103 | github.com/mohammadkarami79/OptiGradTrust | models/rl_actor_critic.py | attacks/attack_utils.py | config/*.py | S | S |
| V2-4540 | github.com/PFEWorkspace/code | scratch/subdir/DRL/agent | scratch/subdir/FL_tasks.py | config.json, run.py | S | S |
| SB-03 | github.com/ZiangLyu/FedCHO | main.py (actor-critic) | main.py | main.py | S | S |
| V2-1042 | github.com/cry-C/SecureGraphFL | AC.py | não encontrados | service.py | S | P |
| V2-0987 | github.com/Aquarids/Flmpid-pub | — | — | — (repositório inexistente) | S | P |
| V2-0922 | sem link ("open-sourced") | — | — | — | P | P |
| V2-0688 | suplemento IEEE (10.1109/TIFS.2025.3630065) | — | — | o artigo não declara código no suplemento | P | N |
| V2-1057 | suplemento IEEE (10.1109/TIFS.2026.3691662) | — | — | o suplemento contém apêndices (figuras e provas) | P | N |

O conteúdo dos suplementos IEEE não pôde ser aberto daqui (o Xplore exige sessão). Se algum deles contiver o código completo, o estudo passa a S.
