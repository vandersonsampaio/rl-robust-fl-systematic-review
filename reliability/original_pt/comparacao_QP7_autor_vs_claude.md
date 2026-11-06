# Comparação QP7: fichamento do autor × análise do Claude

**Data:** 2026-10-13

**Fontes:**
- `selecionados/Fechamento_QP7 - PDF/`: 37 fichamentos do autor, com as perguntas P1–P6 sugeridas;
- análise do Claude:
  - `triagem_v2/etapa2_arxiv.csv` e `etapa2_lote2_q7.tsv` (motivos de inclusão);
  - `notas_etapa2_*.md`;
  - §7 de `slr_resultado.md` e RQ7 de `paper_slr/main.tex`.

**Cobertura:** 37 de 37 (32 da busca e do snowballing + 5 leituras canônicas). Os textos foram casados com os ids sem ambiguidade.

Na QP7 a análise do Claude era narrativa, com uma frase de motivo por estudo e o uso de cada um na síntese. Por isso a comparação é por **afirmação da síntese**, e não campo a campo como na S1.

---

## 1. Onde estamos de acordo

| afirmação da síntese | leitura do autor | situação |
|---|---|---|
| Nenhuma auditoria de FL avalia **empiricamente** defesas por RL ou bandit | P5 = "não" nos 32 estudos de FL | **confirmada**, com a ressalva da §2.1 |
| As canônicas mostram que baselines simples igualam deep RL (Mania, Rajeswaran) e que poucas sementes enganam (Henderson, Agarwal) | idem, com detalhes (ARS ≥ TRPO/PPO/SAC/DDPG; RBF > TRPO em 5/6; DQN+Adam ≈ C51; DER > CURL/SUNRISE) | confirmada |
| (i) datasets fáceis e ataques simplistas (V2-4764, V2-0870) | idem; ambos cobrem as 5 armadilhas | confirmada |
| (ii) o não-IID quebra as defesas (V2-4731, V2-0297, V2-4735, V2-0016) | idem | confirmada |
| (iii) o adversário adaptativo quebra defesas de tipo único (V2-4797, V2-0988, Szeląg) | idem; Szeląg: o RMC derruba o Trimmed Mean para 50% e o Krum para 65,3% (teste t) | confirmada |
| (iv) bugs e métricas incompletas (V2-4739, V2-4859, V2-2562, V2-4831) | idem (BackFed: bugs de fidelidade e vazamento de avaliação; V2-4831: RMSE limpo normal com ASR de 94,9%) | confirmada |
| ABSA (V2-0116): análogo não aprendido das regras por rodada | idem, mais preciso: o ganho é de **custo** (−38%); em acurácia, o Multi-Krum fica a 1 p.p. (83,1 × 84,1 com 30%) e o FedAvg vence sem ataque | confirmada; **ajustar a redação** |

## 2. Onde divergimos

### 2.1 Defesas por RL citadas nas auditorias (afeta uma frase do paper)

O paper diz: *"None of the 32 audit studies … evaluates RL- or bandit-based FL defenses."* O autor mostra que três auditorias **citam ou catalogam** defesas por RL, embora nenhuma as avalie experimentalmente:

- **V2-0870 / V2-4764 (Khan et al.):**
  - auditam 50 defesas da literatura, entre elas o **Justinian's GAAvernor** (USENIX Security 2020), uma agregação de gradientes por RL;
  - concluem que ele cai nas mesmas armadilhas: avaliado sobre FedSGD, com dados IID e ataques ingênuos.
- **SB-06:** compila da literatura o resultado do AdaAggRL (tolera até 90% de maliciosos, com acurácia menor).
- **V2-4840:** cataloga o DRL-PBFL e diz que sua viabilidade prática não foi validada.

**Proposta de consenso:** reescrever a frase como *"nenhuma avalia experimentalmente; as três que as citam (V2-0870/4764, SB-06, V2-4840) só catalogam, e a única auditada (GAAvernor) apresenta as mesmas armadilhas"*. Esta versão **reforça** o argumento em vez de enfraquecê-lo.

### 2.2 GAAvernor (V2-1301): estudo primário que ficou fora da S1

- **Como ficou fora:** o registro V2-1301 entrou só pela S2a (fluxo QP7) e foi excluído como Q7-E ("sem termos de auditoria"). **Nunca foi avaliado para a S1.** O resumo fala em *distributed learning* com *workers* bizantinos, não em *federated*, e por isso a string da S1 não o recuperou.
- **Por que importa:** é a defesa por RL mais antiga e mais citada da área. Três estudos incluídos a citam (V2-0391, V2-0837, V2-0918), e a auditoria V2-0870/4764 a trata como defesa de FL.
- **Decisão do autor:** pelo IC1 ("o sistema é de aprendizado federado"), cabem duas leituras:
  - **(a) Incluir via snowballing como SB-10** (recomendado). O cenário de servidor de parâmetros com *workers* bizantinos é o mesmo das defesas clássicas de FL (Krum, Bulyan, Median também foram propostas para *distributed learning*), e a omissão seria apontada por revisores. Exige o PDF, uma ficha §9.1 e a regeneração da síntese (79 estudos).
  - **(b) Excluir por IC1** e registrar a decisão e o motivo no PRISMA e nas ameaças à validade.

### 2.3 "Defesas simples bastam" é o achado dominante, não um entre cinco

Na síntese, a armadilha (v) aparece com 3 estudos (V2-0252, V2-4739, V2-1338). O fichamento mostra que **28 dos 32 estudos de FL** trazem algum caso em que o simples iguala ou supera o sofisticado.

**Padrão A, sob ataque:** regras simples ≥ defesas complexas.

| estudo | caso |
|---|---|
| V2-0274 (Blades) | Média + *client momentum* > todas as defesas sob ALIE (85,9 × DnC 83,6) |
| V2-4839 | Median e Krum > FoolsGold e DeepSight, com 1.600× a 1,7·10⁶× menos custo |
| SB-09 | *norm clipping* > Krum |
| V2-0252 | *norm-bounding* ≈ Multi-Krum e TM |
| SB-07, SB-08 | Median/TM ≥ Bulyan, RLR e DeepSight (DeepSight: ASR 68% sob não-IID) |
| V2-4735 | Trim > defesas específicas de DFL |
| V2-1403 | TM ≈ Bulyan a 1/10 do tempo; amostragem aleatória como defesa natural |
| V2-0953 | MKrum e TM > FRL |
| V2-0988 | MKrum e Bulyan > FedREDefense |
| V2-0870 / V2-4764 | treinar do zero > FedRecover |
| V2-4797 | Krum + CSFT ≈ agregadores complexos |
| V2-1338 | Simple-Tuning e FedRep > pFL sofisticado |
| V2-4857 | regularização genérica > defesas específicas de VFL |
| V2-4668 | DP simples > autoencoders aprendidos |
| V2-0896 | *two-norm* restaura a acurácia |
| V2-2916 | *norm clipping* e *weak DP* neutralizam backdoors |
| V2-4840 | regras de frequência ≈ redes profundas (dataset trivial) |
| **V2-3771** | **MAPPO + mediana: melhor sem ataque; depois da correção de Holm, nenhuma vantagem do RS-MARL resiste no nível da família de testes** |

**Padrão B, sem ataque:** as defesas robustas têm custo, e o FedAvg ou a média simples vencem.

- V2-2053, V2-0016, SB-05, V2-4731, V2-0116.
- V2-1365, no viés: Multi-Krum 20,5% × FedAvg 5,4%.
- V2-4859: em condições reais, o FedAvg já atenua a maioria dos ataques.
- V2-4739: o FedAvg preserva a acurácia, e as defesas chegam a ser 388× mais lentas.

**Padrão C, do lado do atacante:** ataques simples ≥ ataques otimizados.

- V2-4739 (estático ≈ Neurotoxin, > DBA);
- V2-4839 (Gaussian e Sign-flip > ALIE e MinMax);
- V2-4859 (EdgeCase > DBA e Neurotoxin);
- V2-4857 (LFBA > BAEVFL);
- V2-1403 (MinSum quebra as 4 defesas).

**Contraexemplos**, que devem ser citados para equilíbrio:
- V2-2562: no ViT, TM, Median e clipping caem para ~54%, e o FoolsGold mantém 84,7%;
- V2-4831: agregadores por coordenada colapsam (RMSE 84), e o Krum recupera;
- V2-0297: sob não-IID severo, simples e sofisticados falham igualmente;
- V2-0016: FedAvg ≫ defesas só **sem** ataque.

**Proposta de consenso:** reestruturar a RQ7 do paper e o §7 da síntese em torno de três achados:
1. defesas simples igualam as sofisticadas na maioria dos benchmarks (padrão A, com contraexemplos);
2. a robustez tem custo sem ataque (padrão B);
3. ataques sofisticados são superestimados (padrão C).

As armadilhas (i)–(iv) continuam como explicação de **por que** os resultados publicados divergem. O V2-3771 sobe de "auditoria rigorosa com resultado dependente de regime" para **a evidência mais direta da QP7**: a única auditoria com estatística corrigida de um método aprendido sob ataque bizantino, em que um baseline simples (mediana) não é superado de forma significativa.

### 2.4 Rigor estatístico das próprias auditorias (não estava na síntese)

O item P6 do autor permite uma afirmação nova: **mesmo as auditorias raramente usam inferência estatística.**
- Entre os 32 estudos de FL, só **3** aplicam teste de hipótese: V2-4831 (Wilcoxon), V2-3771 (Wilcoxon + Holm) e V2-0116 (p, d de Cohen).
- Cerca de 10 relatam várias sementes com variância: V2-0896, V2-0016, V2-0274, V2-4831, V2-4668, V2-4857, V2-4735, V2-4797, V2-1403 e V2-1338, alguns sem desvio.
- Os demais não informam sementes.

Isso reforça o item "Report uncertainty" da agenda.

### 2.5 Pontos menores

| estudo | divergência | proposta |
|---|---|---|
| V2-3771 | o autor registra "MAPPO-CWMed ≥ em 25 de 30 células"; o texto extraído diz 19/30 (RS-MARL × Safe-MAPPO) e não mostra o 25/30 | autor confere a Tabela; no paper usar a frase verificada ("sem ataque, MAPPO-CWMed é o melhor; após Holm, nenhuma vantagem família a família") |
| V2-0988 | o autor classifica como **pesquisa original** (propõe ataque PADS e defesa DRF), não auditoria | manter (o critério A7 aceita "avaliações" e o artigo demonstra uma armadilha: participação estática superestima robustez), mas descrever como estudo original que expõe a armadilha. O ano é 2026 (TDSC); o "2020" no nome do arquivo do autor está errado |
| V2-0953, V2-0116, V2-1365 | o autor também os vê como avaliação + método novo ou workshop | manter; descrever o tipo corretamente |
| SB-06 | o autor: estudo comparativo **só de literatura**, sem experimentos | manter no bloco "SoKs"; o critério A7 exige estudo experimental para surveys. **Conferir:** se não tem experimento próprio, pelo A7 seria Q7-E |
| V2-2562 | o meu motivo dizia que a robustez aparente "não se sustenta"; o autor mostra que o FoolsGold se sustenta no ViT | descrever como contraexemplo do padrão A |

## 3. Decisões pendentes do autor

1. **GAAvernor (V2-1301):** incluir na S1 via snowballing (recomendado; exige o PDF) ou excluir por IC1, com registro.
2. **SB-06:** confirmar se há experimento próprio. Se não houver, sai da QP7 pelo A7 (36 estudos).
3. **V2-3771:** conferir o "25/30".
4. **Aplicar as propostas da §2:**
   - reescrever a RQ7 do paper e do capítulo e o §7 da síntese em torno dos padrões A/B/C;
   - corrigir a frase sobre "nenhuma avalia RL";
   - acrescentar o rigor das auditorias.

## Consenso aplicado (2026-10-13)

| estudo | decisão |
|---|---|
| V2-1301 (GAAvernor) | excluído da S1 por IC1 (aprendizado distribuído, não federado) |
| SB-06 | excluído da QP7 (A7: sem experimento próprio) |
| V2-0870 | excluído da QP7 (EC7: versão anterior de V2-4764) |
| V2-0988 | excluído da QP7 (A7: pesquisa original) |
| V2-3771 | registrado com os valores verificados no texto (sem o "25/30") |
| V2-0116 | adotada a leitura do autor (ganho de custo; Multi-Krum a 1 p.p.) |
| V2-2562 | registrado como contraexemplo |
| V2-4764 | corrigido: cataloga o GAAvernor e mostra as mesmas armadilhas |
| V2-4840, V2-1365 | registrado: citam defesa por RL, sem avaliá-la |
| armadilhas | adotada a classificação do autor (várias por estudo) |

**Onde ficou registrado:**
- `triagem_v2/etapa2_lote2_q7.tsv`: decisões e motivos;
- `triagem_v2/extracao_qp7.csv`: ficha por estudo, gerada por `scripts/extracao_qp7.py`;
- protocolo: adendo A15;
- `slr_resultado.md`: contagens da QP7 e frase sobre RL.

A QP7 passa a ter 34 estudos. O paper e o capítulo **não** foram alterados.
