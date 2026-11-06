# Code availability check (QA4, amendment A24)

English account of `original_pt/code_availability_check_pt.md` (October 22, 2026). Under amendment A24, QA4 scores whether code is accessible and sufficient, not where it is hosted.

**Rule.** S: code accessible without intermediation (public repository or journal supplement) that contains the agent and the experiment (attacks, and configuration or scripts). P: code accessible but incomplete, or declared available without direct access (on request, no link, or a broken link). N: no code declared.

**Procedure.** For each study that declared code, the link given in the article was opened (GitHub API, Zenodo, DOI) and the file tree was read. The presence of the agent and of the attacks was checked by file names and by searching the code for attack terms (attack, poison, malicious, byzantine, adversarial). The experiments were not run.

| study | link | agent | attacks | configuration or scripts | before | after |
|---|---|---|---|---|---|---|
| V2-4789 | github.com/rafidhaque/FedStrategist; Zenodo 16068113 | src/bandit.py | src/attacks.py | src/main.py | S | S |
| V2-0160 | github.com/pranav21684/AGENTIC-AI-UNLEARNING (redirected) | Agentic_behavior.ipynb | Mainmethod.ipynb | notebooks | S | S |
| V2-4233 | github.com/Echolic/HFSL | secure_selector.py | experiment_hsvfl.py, experiment_sign.py | experiment*.py | S | S |
| V2-0350 | github.com/NexuFed/pFedMARL | src/reinforcement_learning | adversarial clients in src/components/client.py and the .yaml files | .config, scripts/icassp_runs.sh | S | S |
| V2-1231 | github.com/TAP-LLM/AdaAggRL | main.py | attack_utilities.py | requirements, exp_environments | S | S |
| V2-1254 | github.com/Gp1g/FedAA | DDPG/ | --attack same_value, sign_flip, gaussian | main.py | S | S |
| V2-2103 | github.com/mohammadkarami79/OptiGradTrust | models/rl_actor_critic.py | attacks/attack_utils.py | config/*.py | S | S |
| V2-4540 | github.com/PFEWorkspace/code | scratch/subdir/DRL/agent | scratch/subdir/FL_tasks.py | config.json, run.py | S | S |
| SB-03 | github.com/ZiangLyu/FedCHO | main.py (actor-critic) | main.py | main.py | S | S |
| V2-1042 | github.com/cry-C/SecureGraphFL | AC.py | not found | service.py | S | P |
| V2-0987 | github.com/Aquarids/Flmpid-pub | – | – | – (repository does not exist) | S | P |
| V2-0922 | no link ("open-sourced") | – | – | – | P | P |
| V2-0688 | IEEE supplement (10.1109/TIFS.2025.3630065) | – | – | the article does not declare code in the supplement | P | N |
| V2-1057 | IEEE supplement (10.1109/TIFS.2026.3691662) | – | – | the supplement holds appendices (figures and proofs) | P | N |

**Limitation.** The content of the IEEE supplements of V2-0688 and V2-1057 could not be opened, because IEEE Xplore requires an institutional session. Both studies are scored N on the basis of what the article and the supplement listing declare. If either supplement contains the complete code, that study would move to S, which changes the QA4 distribution (9 S, 3 P, 65 N) by one study each.
