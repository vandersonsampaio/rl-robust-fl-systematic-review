# Reclassificação cega do R2: QP2

**Data:** 2026-10-21
**Fonte:** `planilha_cega_R2_QP2.xlsx`, aba QP2, com 52 estudos (todos os que tinham comparação não aprendida no R1 antes do A20).
**Números:** `concordancia_qp2_R2v2.md` e `.csv`, gerados por `scripts/concordancia_qp2_R2v2.py`. O R1 é a extração antes do consenso (`extracao_principal_R1_antes_A20.csv`). O subtipo "não defender" do R2 conta como ação fixa, como no livro que ele recebeu.

## Resultado

| campo | concordância | κ |
|---|---|---|
| categoria (7 categorias, 51 estudos sem "?") | 58,8% | **0,49** |
| referência forte × fraca | 68,6% | 0,39 |
| rodada anterior (A16), mesmos 52 | 34,6% | 0,14 |
| resultado, mesma categoria (9 estudos) | 44,4% | 0,20 |
| discutido como achado | 21,6% | 0,00 |

O κ da categoria passa de fraco para moderado. O resultado tem poucos pares, e a divergência vem de duas regras que o livro deixa em aberto: texto dos autores × números no critério de empate, e a escolha da métrica principal. No "discutido", a diferença é sistemática: o R1 deu 7 S, 4 P e 40 N, e o R2 deu 44 S, 1 P e 6 N.

## Decisões do autor

1. **V2-4540 (21/10/2026).** A categoria continua sendo mesmo sinal, e o discutido continua S, como deram os dois revisores. O resultado passa de vitória clara para **empate**, como deu o R2. Nas Figs. 9–11, com valores das rodadas finais lidos no gráfico, o escore iguala ou supera o híbrido:
   - escalabilidade: ~93 × ~95;
   - robustez, com 60% de desonestos: ~88 × ~87,5;
   - disponibilidade, com 60% de dropout: ~91,5 × ~87.

   O DRL puro perde para o escore nos três regimes. O "híbrido > escore" do R1 vinha do texto dos autores, e não das figuras.

   Efeitos:
   - as comparações mais próximas passam a ter 7 empates, e não mais 6;
   - o V2-4540 entra no cenário O2 da sensibilidade, que trata como vitória os empates em que alguma métrica favorece o agente;
   - no Portão N, o V2-4540 passa a ser o caso mais próximo de "já mostrado". Os autores atribuem a robustez ao escore, mas defendem o híbrido pela adaptabilidade e pela imprevisibilidade, sem testar ataque adaptativo, com execução única, só MNIST e 30 rodadas.

   A conclusão "parcialmente mostrado" se mantém, e as conclusões A–E da sensibilidade também, nos cenários do R1.

2. **Texto dos autores × números no empate (21/10/2026, A21).** O §2.4 do livro tinha duas regras em conflito: a regra geral 2 do §1 (vale o número, e não a conclusão dos autores) e a cláusula "os autores descrevem os resultados como semelhantes". Decisão: os números prevalecem. A descrição dos autores só decide quando não há números legíveis ou quando a diferença está dentro do erro de leitura da figura. É a mesma lógica do V2-4540, onde o texto dos autores não criou vitória. O `livro_codigos_v2.md` foi revisto, e a cópia do R2 fica como estava. A leitura contrária continua coberta pelo cenário O1, que trata as vitórias estreitas como empate.
   - **V2-1102** passa de empate para **vitória estreita**, como deu o R2. O DDPG supera o limiar estático em todos os regimes:
     - k = 5: 0,89 × 0,86;
     - k = 10: 0,68 × 0,62;
     - Fig. 4: ~+6 a 8 p.p., em média de 15 execuções sem variância.

     O "almost similar" vale só para k = 5. A marca de evidência do Portão N foi retirada.
   - **V2-1179** continua **empate**, agora pelos números, e o R2 tinha dado vitória estreita. Sob ataque fraco, o DDPG supera o φ = 1 fixo por 1,6 a 1,8 p.p. com k = 5, mas só por 1,1 p.p. com k = 10. Sob ataque forte, não há valores. Sem ataque, o DDPG iguala o φ = 0 fixo. A categoria "aleatória" dada pelo R2 parece um deslize, porque a descrição que ele mesmo escreveu é "fixar φ = 1".

   Efeitos:
   - as comparações mais próximas ficam com 6 empates, e não mais 7;
   - contra o mesmo sinal, ficam 2 empates (V2-2103 e V2-4540);
   - o V2-1102 sai da lista de empates do Portão N e entra em "vence por margem pequena";
   - as conclusões A–E se mantêm nos cenários do R1.

3. **V2-0351 (21/10/2026).** O "vitória clara" do R1 (+6,6 a 9,5 p.p.) era contra a seleção **aleatória**. Pelo §2.4, porém, o resultado se mede contra a referência mais forte, que é a seleção direta: a combinação de maior reputação histórica, sem refazer a busca por Q-learning (Sec. IV-C, Fig. 9). A referência usa o mesmo sinal do agente, e os autores a chamam de "control group".
   - **Resultado: vitória estreita**, como deu o R2. A taxa de erro foi lida no zoom da Fig. 9, com L = 6, nas iterações 35–45 e em execução única:
     - K = 8: ~0,03 × ~0,04;
     - K = 10: ~0,035 × ~0,07;
     - K = 15: ~0,06 × ~0,12.

     O agente vence nos três regimes por 1 a 6 p.p.
   - **Discutido: S**, como deu o R2. Os autores chamam a adaptativa de "the strategy we advocate", e o resultado "illustrates the importance of relearning".
   - O texto da categoria foi alinhado com o A20: "todos os colaboradores" agora aparece como "sem defesa".

   Efeito: contra o mesmo sinal, o agente **não vence claramente em nenhum dos 7 estudos**. Empata em 2 (V2-2103 e V2-4540) e vence por margem pequena em 5. As comparações mais próximas continuam com 6 empates, e o cenário O1 passa a 12. As conclusões A–E se mantêm. O `main.tex` ("wins clearly in the other two") precisa ser corrigido na atualização do paper.

4. **Métrica principal (21/10/2026, A21).** O livro dizia "na métrica principal" sem defini-la. A regra registrada no §2.4 é a seguinte. A métrica principal é a utilidade do modelo global sob ataque, no conjunto de teste completo, com duas exceções:
   - no ataque dirigido, vale a métrica do efeito do ataque, como a ASR ou a acurácia na classe atacada;
   - sem comparação em utilidade, vale a métrica da decisão do agente.

   Custo, tempo e convergência são secundários, salvo quando são o único resultado comparado. É a ordem que o R1 já seguia, e nenhum resultado muda:
   - **V2-2103** continua **empate**: a acurácia é 64,32 × 64,35 (Tab. 14). O Det-F1 (61,7 × 36,4), escolhido pelo R2, fica em nota, porque o ganho vem da atenção, e não do RL (sem RL, 61,1).
   - **V2-1327** continua **empate**, pela exceção do ataque dirigido, porque o ataque troca os rótulos para um valor único. A acurácia no rótulo envenenado é de +0,9 a +2,2 p.p. contra o peso fixo (Tab. 2). A acurácia em todos os rótulos, usada pelo R2, mostra +4 a 6 p.p., mas reflete o rótulo especial (66–74% × 2,7%), que é inclusão de dados raros, e não defesa.
   - **V2-3331** continua **vitória estreita**, com acurácia de +5 a 6% sobre o Shapley completo. O 5734 ms usado pelo R2 vem do experimento de taxa de amostragem (Fig. 10), e não da ablação. A ablação roda sem ataque. A categoria segue em aberto.
   - **V2-1130 (controle)** continua **vitória clara**. Contra a auditoria fixa (MAO e PAO), só há CJR e RE, então vale a métrica da decisão. A acurácia só é comparada com "sem auditoria", que conta como nenhuma.

   Dos 5 desacordos de resultado com a mesma categoria, 3 eram escolha de métrica (V2-2103, V2-1327 e V2-3331). Os outros 2 eram o V2-4540 e o V2-0351, já resolvidos a favor do R2.

5. **Discutido como achado (21/10/2026, A21).** O §2.5 juntava duas perguntas, e cada revisor respondeu a uma. O R2 leu o texto ao pé da letra: os autores comentam o resultado da comparação e tiram dele uma conclusão, em qualquer direção. O R1 deu S só quando os autores tratavam a comparação como achado sobre o papel do aprendizado, que é o critério do Portão N no protocolo ("e apresenta isso como achado"). Daí o κ = 0,00, com R1 7/4/40 e R2 44/1/6 em S/P/N. O κ é reportado como está, com essa explicação.

   Decisão: o §2.5 fica com a leitura literal, e a pergunta do Portão N passa a ser registrada à parte, só nos empates e nas derrotas contra o mesmo sinal ou a ação fixa. O livro do R1 foi revisto, e a cópia do R2 fica como estava.
   - **Código do R2 adotado** em 23 estudos em que os dois revisores falam da mesma referência. Nos outros, o R2 tinha comentado outra referência ou dado "nenhuma", e o código saiu da leitura do PDF para a referência do R1. Deram S: V2-0111, 0350, 0542, 0634, 0835, 1130, 1199, 1450, 2188, 2573, 3215 e 4266. O V2-4812 continua S: o ajuste manual do limiar é discutido na Sec. IV, e o N do R2 vinha da categoria "nenhuma". O V2-1120 fica P, porque a comparação aparece só nas tabelas e no resumo.
   - **Sem comparação, o código é N.** Os 4 estudos que passaram a "nenhuma" pelo A20 (V2-0945, 1030, 1178 e 3265) ficam com N, e o V2-1041 passa de "S (lacuna admitida)" para N, com a lacuna registrada no próprio campo.
   - **Resultado:** dos 47 estudos com comparação, 46 têm S e 1 tem P. A coluna deixa de separar os estudos e **sai da tabela da QP2** na atualização do paper (decisão do autor, 21/10/2026). No lugar dela, uma frase no texto diz que quase todos os estudos comentam a comparação.

   Portão N, nos 6 empates contra o mesmo sinal ou a ação fixa:
   - **não reconhecem o empate:** V2-1327, que atribui o ganho aos pesos maiores no rótulo especial, e V2-4789, que não comenta a Mediana nem a vitória do FedAvg sob ataque furtivo;
   - **reconhecem, mas enquadram como virtude do agente:**
     - V2-1179: "essentially similar" ao φ = 1 fixo, e o agente acha sozinho a melhor fixa de cada regime;
     - V2-0350: o local-only fixo supera no local, lido como troca entre personalização e generalização;
     - V2-2103: "identical with and without RL", com o RL reposicionado como consistência da detecção;
     - V2-4540: a robustez vem do escore, mas o híbrido é defendido pela adaptabilidade.

   Nenhum conclui que o aprendizado é dispensável, e o Portão N continua "parcialmente mostrado".

   Achado lateral: o V2-1120 (TARS) diz que os números das Tabs. II–V são "consistent with cited literature or derived by careful synthesis of referenced figures". Isso põe em dúvida se os resultados vêm de experimento próprio, e é para avaliar na qualidade e na inclusão (o autor concorda em reavaliar; ver decisão 6).

6. **V2-1120 excluído por IC4 (21/10/2026, A22).** Os autores declaram que os números das Tabs. II–V são "consistent with cited literature or derived by careful synthesis of referenced figures" e "validated against published references", inclusive na linha do TARS. Faltam os hiperparâmetros do agente, o número de execuções, o modelo e o framework. Os valores atribuídos ao SARA (85,9 e 81,2% de seleção da regra ótima) não batem com o V2-0111 (28/30 e 27/30). Sem avaliação empírica verificável, e com uma comparação que não é controlada, o estudo sai da S1 na etapa 2 (`etapa2_lote2_decisoes.tsv`). A ficha fica nos dados, e `etapa2_lote2.py` deixa de levar à síntese os estudos não incluídos.
   - S1: 78 → 77 estudos (75 pela busca, 2 pelo snowballing).
   - QP2: com comparação 47 → 46; referência forte 28 → 27; comparações mais próximas 17 → 16, com uma vitória estreita a menos. Empates (6) e mesmo sinal (7) não mudam.
   - As conclusões A–E da sensibilidade se mantêm, com os limiares agora calculados sobre o total.
   - A concordância desta reclassificação continua com o V2-1120, porque mede a codificação antes do consenso.

7. **Categorias divergentes (21/10/2026, A21).** Revi as 24 divergências de categoria que restavam entre o R1 atual e o R2.
   - **O R2 tem razão em 4**, lidas no PDF:
     - **V2-2188 → nenhuma.** O SAFE-GF-NOMA é um método de outro artigo: agrupa por potência contra colisões e agrega com FedAvg depois da decodificação, sem ação defensiva contra envenenamento.
     - **V2-4266 → aleatória.** O secure-UCB "ideal" é o próprio CS-UCB aprendido numa rede sem atacantes, ou seja, um baseline aprendido, e não um oráculo.
     - **V2-3243 → ablação parcial.** O texto só diz "systematically removing a specific module". O Trimmed Mean é o fallback das 20 rodadas de aquecimento, e não a variante da ablação. O "Trimmed Mean fixo" do R1 era inferência.
     - **V2-3331 → ablação parcial.** A variante é "Full Shapley value computation without the Bandit strategy", sem dizer que seleção substitui o bandit.
   - **O R1 se mantém nas outras 20**, pelo livro de códigos:
     - Pow-d como outro sinal (V2-0542, 1199, 3215): é exemplo explícito do §2.2, e o próprio R2 o usou no V2-1140.
     - Seleção pela capacidade de computação (V2-0835): é outro exemplo explícito do §2.2. A referência do R2 (Only Min-Time e Only Min-Energy) é do módulo de alocação de recursos, e não da seleção.
     - Regra fixa quando o agente escolhe a regra, e parâmetro fixo quando o agente ajusta o parâmetro: V2-2573, 4812 e 0350 são fixa. No V2-0111, a melhor regra *a posteriori* é oráculo.
     - Os "não defender" do R2 viram nenhuma pelo A20: V2-0945, 1030, 1178 e 3265. No V2-0391, 1450 e 4727, a referência mais forte do R1 é aleatória.
     - O V2-0940 também fica aleatória pelo A20: o "Fixed" é canal fixo com seleção aleatória, sem ação defensiva.
     - O V2-0634 é aleatória, porque FedAvg com seleção aleatória de nós está no espaço de ação. O R2 deu aleatória no V2-3789, que tem o mesmo desenho.
     - V2-1179: deslize do R2, cuja descrição é "fixar φ = 1".
     - V2-1130: o R2 deu "?"; a auditoria de todos com um só método é exemplo de ação fixa no §2.1.
     - V2-1120: excluído (decisão 6).

   **Efeito:**
   - QP2: sem comparação 31 → 32; com comparação 46 → 45; referência forte 27 → 23; mesmo sinal 7 → 6; comparações mais próximas 16 → 14. Os empates (6) não mudam.
   - Contra o mesmo sinal, o agente empata em 2 e vence por margem pequena em 4. Sai a vitória clara do V2-3243 contra fixa.
   - As conclusões A–E se mantêm em todos os cenários, inclusive no novo cenário R2, que passou a usar esta reclassificação. A conclusão D, que caía na rodada antiga, agora vale.
   - O cenário F2 (V2-3243 como mesmo sinal) passa a cobrir a leitura anterior do R1.
   - Referência pós-consenso, sem valor reportado: 35/51, κ = 0,61.
   - Com as decisões 6 e 7, o discutido fica S nos 45 estudos com comparação, porque o V2-1120 (P) saiu e o V2-2188 virou nenhuma.
