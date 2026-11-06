# Casos-limite da QP2: decisões do R1

**Uso restrito ao R1.** Não enviar ao R2 antes da classificação cega. Complementa `livro_codigos_v2.md`.


Estes casos foram discutidos na conciliação. Servem para a reunião de consenso e para a análise de sensibilidade (`sensibilidade_qp2_qa.md`).

| estudo | dúvida | decisão do R1 |
|---|---|---|
| V2-1102, V2-0973 | limiar estático de 0,5: ação fixa ou heurística do mesmo sinal? | mesmo sinal |
| V2-3243 | trimmed mean fixo sobre os mesmos sinais: ação fixa ou mesmo sinal? | ação fixa |
| V2-4059 | AMA usa pesos estáticos sobre três dos quatro sinais do agente | outro sinal |
| V2-0835 | seleção gulosa pela capacidade: mesmo sinal ("míope") ou outro sinal? | outro sinal |
| V2-0542, V2-1140, V2-1199, V2-3215 | Power-of-Choice | outro sinal |
| V2-3494 | FedAvg sem o filtro que precede o agente | nenhuma |
| V2-1042, V2-1185, V2-0918, V2-1231 | agregadores robustos externos | nenhuma |
| V2-3175 | treino centralizado | nenhuma |
| V2-4789 | FedAvg 39,43 × agente 38,82 (Tab. 2) | ação fixa; empate ou derrota conforme o regime |
| V2-2103 | acurácia igual nas três condições (Tab. 14); F1 sem RL ≈ com RL | mesmo sinal; empate em acurácia |

