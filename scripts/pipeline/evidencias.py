"""Segunda passada da extração (§9.1): busca exaustiva no texto integral (sem referências) de evidências
por campo, para distinguir 'não reportado' de 'não localizado'. Saída: um bloco por estudo."""
import csv, re, sys
from pathlib import Path
B = Path(__file__).resolve().parent.parent / 'triagem_v2'
m = {r['id']: r for r in csv.DictReader(open(B / 'mapa_pdfs.csv', encoding='utf-8-sig'))}
ARXIV = {'V2-4727': '2602.20003v1', 'V2-4728': '2510.01261v1', 'V2-4789': '2507.14322v2', 'V2-4812': '2410.17431v1'}
F = {
 'recompensa': r'reward\w*\s+(function\s+)?(is|was|are|=|:|defined|computed|calculated|consists|combin|based)|r_?t\s*=|\bR\(s',
 'dado': r'\b(validation|root|test|held-out|auxiliary|clean|reserved|trusted|benchmark)\s+(data\s*set|dataset|set|data)\b',
 'orcamento': r'\b(learning rate|episodes?|replay (buffer|memory)|batch size|discount factor|\bγ\s*=|epsilon|ε\s*[=-]|exploration|training steps|iterations|communication rounds|global rounds|rounds)\b',
 'sementes': r'\b(random seeds?|seeds?\b|independent (runs|trials|experiments)|repeated|runs\b|averaged over|average of \d+|mean (and|±)|standard deviation|std\b|confidence interval|t-test|p-value|p\s*<|wilcoxon|anova|statistically significant)',
 'codigo': r'(github|gitlab|zenodo|code (is|will be) (publicly )?available|source code|open[- ]source|available at https?)',
 'custo': r'\b(overhead|running time|execution time|computation(al)? (time|cost|complexity)|seconds|ms\b|per round|time cost|wall-clock|GPU|complexity)',
 'clientes': r'\b(\d+\s*(clients|devices|participants|workers|vehicles|nodes|users)|malicious (clients|nodes|devices|ratio|proportion)|non-iid|dirichlet|iid)\b',
 'adaptativo': r'\b(adaptive (attack|adversar\w*)|full[- ]knowledge|white-box|aware of the defen|knows the (defen|aggregat)|tailored|on-off|pretense|evade|evasion|stealth)',
 'naoaprendida': r'\b(random (selection|policy|strategy|client|baseline|scheduling|unlearning)|fixed (weight|threshold|policy|rule|action)|static (threshold|policy|rule|weight)|greedy|heuristic|without (the )?(rl|drl|agent|marl|ppo|dqn|ddpg|td3|bandit)|w/o|ablation|rule-based)',
}
def sents(t):
    return re.split(r'(?<=[.!?])\s+(?=[A-Z(])', t)
def doc(i):
    if i in ARXIV:
        p = B / 'arXiv_txt' / (ARXIV[i] + '.txt')
    else:
        r = m[i]; p = B / 'txt' / r['pasta'] / (r['arquivo'] + '.txt')
    t = p.read_text(encoding='utf-8', errors='ignore')
    t = re.sub(r'\s+', ' ', re.sub(r'-\n(?=[a-z])', '', t))
    ref = max(t.rfind('References'), t.rfind('REFERENCES'), t.rfind('R EFERENCES'))
    return t[:ref] if ref > len(t) * 0.55 else t
for i in sys.argv[1:]:
    ss = sents(doc(i))
    print(f'##### {i}')
    for k, p in F.items():
        rx = re.compile(p, re.I); out = []; seen = set()
        for s in ss:
            if 25 < len(s) < 500 and rx.search(s):
                key = s[:50]
                if key not in seen: seen.add(key); out.append(s)
        lim = 5 if k in ('recompensa', 'naoaprendida', 'sementes') else 3
        print(f'-- {k} ({len(out)}):')
        for s in out[:lim]: print('   *', s[:300])
